import os
import sqlite3
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.db import get_db_connection, DEFAULT_DB_PATH

app = FastAPI(
    title="DGCA Aviation Statistics API",
    description="API for querying monthly Indian aviation statistics and performance metrics",
    version="1.0.0"
)

# Global pipeline sync status
pipeline_status = {
    "status": "idle", # "idle", "running", "completed", "error"
    "logs": ["System ready."],
    "year": None
}

def run_sync_pipeline(year: int):
    global pipeline_status
    pipeline_status["status"] = "running"
    pipeline_status["year"] = year
    pipeline_status["logs"] = []
    
    def log(msg):
        print(msg)
        pipeline_status["logs"].append(msg)
        
    try:
        log(f"Starting pipeline run for year {year}...")
        log("Step 1: Scraping report links from DGCA website...")
        
        from src.scraper import run_scraper
        from src.parser import run_parser
        from src.db import init_db, insert_records
        
        log(f"Fetching and downloading report files for {year}...")
        meta_path = run_scraper(limit_years=[str(year)])
        log(f"Scraper completed. Local metadata: {meta_path}")
        
        log("Step 2: Extracting tables from PDF reports...")
        records = run_parser(metadata_path=meta_path)
        log(f"Parser completed. Extracted {len(records)} records.")
        
        log("Step 3: Syncing records to database...")
        init_db()
        if records:
            insert_records(records)
            log(f"Successfully synchronized {len(records)} traffic records to database.")
            pipeline_status["status"] = "completed"
        else:
            log("No traffic records extracted from the files.")
            pipeline_status["status"] = "error"
    except Exception as e:
        log(f"Pipeline sync failed: {str(e)}")
        pipeline_status["status"] = "error"

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_conn():
    conn = get_db_connection()
    conn.row_factory = dict_factory
    return conn

@app.get("/api/airlines")
def get_airlines():
    """Returns a list of all airlines available in the database, excluding total aggregates."""
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        # Exclude 'Total' summaries from standard list to prevent confusion
        cursor.execute("SELECT id, name FROM airlines WHERE name NOT LIKE 'Total %' ORDER BY name")
        airlines = cursor.fetchall()
        return airlines
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/api/years")
def get_years():
    """Returns all years available in the database."""
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DISTINCT year FROM monthly_traffic ORDER BY year DESC")
        years = [row['year'] for row in cursor.fetchall()]
        return years
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/api/traffic")
def get_traffic(
    airline_id: Optional[int] = Query(None, description="Filter by Airline ID"),
    year: Optional[int] = Query(None, description="Filter by Year"),
    month: Optional[str] = Query(None, description="Filter by Month (e.g. JAN, FEB)"),
    service_type: Optional[str] = Query(None, description="Filter by Service Type: 'Domestic' or 'International'"),
    scheduled: Optional[int] = Query(None, description="Filter by Scheduled (1) or Non-Scheduled (0)")
):
    """Retrieves granular monthly traffic data matching the filter criteria."""
    conn = get_db_conn()
    cursor = conn.cursor()
    
    query = """
        SELECT t.*, a.name as airline_name 
        FROM monthly_traffic t
        JOIN airlines a ON t.airline_id = a.id
        WHERE 1=1
    """
    params = []
    
    if airline_id is not None:
        query += " AND t.airline_id = ?"
        params.append(airline_id)
    if year is not None:
        query += " AND t.year = ?"
        params.append(year)
    if month is not None:
        query += " AND t.month = ?"
        params.append(month.upper())
    if service_type is not None:
        query += " AND t.service_type = ?"
        params.append(service_type)
    if scheduled is not None:
        query += " AND t.scheduled = ?"
        params.append(scheduled)
        
    query += " ORDER BY t.year DESC, a.name ASC"
    
    # Custom sorting for months since sqlite doesn't sort JAN, FEB, MAR naturally.
    # We can inject a month order mapping
    month_map = {
        'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
        'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
    }
    
    try:
        cursor.execute(query, params)
        records = cursor.fetchall()
        
        # Sort records by month order (year DESC, month ASC, airline name ASC)
        records.sort(key=lambda r: (-r['year'], month_map.get(r['month'], 13), r['airline_name']))
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/api/trends")
def get_trends(
    year: int = Query(..., description="The year to generate trends for"),
    service_type: Optional[str] = Query(None, description="Filter by 'Domestic' or 'International'")
):
    """Generates consolidated trend metrics, airline market shares, and monthly summaries for the UI dashboard."""
    conn = get_db_conn()
    cursor = conn.cursor()
    
    # 1. Base query filters
    where_clause = "WHERE t.year = ?"
    params = [year]
    
    if service_type:
        where_clause += " AND t.service_type = ?"
        params.append(service_type)
        
    # We exclude 'Total Domestic' and 'Total International' from the airline computations 
    # to avoid double counting, but we'll query them separately if needed.
    where_clause_airlines = where_clause + " AND a.name NOT LIKE 'Total %'"
    
    try:
        # A. Key Stats Summary
        stats_query = f"""
            SELECT 
                SUM(t.departures) as total_departures,
                ROUND(SUM(t.hours_flown), 1) as total_hours,
                SUM(t.passengers_carried) as total_passengers,
                ROUND(SUM(t.pax_kms_performed) / 100000.0, 2) as pax_kms_lakh, -- converted to Lakhs for better scale
                ROUND(SUM(t.cargo_total), 1) as total_cargo_tonnes,
                ROUND(SUM(t.pax_kms_performed) / NULLIF(SUM(t.available_seat_kms), 0) * 100.0, 2) as avg_load_factor
            FROM monthly_traffic t
            JOIN airlines a ON t.airline_id = a.id
            {where_clause_airlines}
        """
        cursor.execute(stats_query, params)
        summary = cursor.fetchone()
        
        # B. Monthly Passenger and Load Factor Trends
        monthly_query = f"""
            SELECT 
                t.month,
                SUM(t.passengers_carried) as passengers,
                ROUND(SUM(t.pax_kms_performed) / SUM(t.available_seat_kms) * 100.0, 2) as load_factor,
                SUM(t.cargo_total) as cargo
            FROM monthly_traffic t
            JOIN airlines a ON t.airline_id = a.id
            {where_clause_airlines}
            GROUP BY t.month
        """
        cursor.execute(monthly_query, params)
        monthly_raw = cursor.fetchall()
        
        # Sort monthly trends chronologically
        month_map = {
            'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
            'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
        }
        monthly_raw.sort(key=lambda r: month_map.get(r['month'], 13))
        
        # C. Airline Passenger Market Share
        share_query = f"""
            SELECT 
                a.name as airline_name,
                SUM(t.passengers_carried) as total_passengers,
                SUM(t.cargo_total) as total_cargo
            FROM monthly_traffic t
            JOIN airlines a ON t.airline_id = a.id
            {where_clause_airlines}
            GROUP BY a.id, a.name
            HAVING total_passengers > 0 OR total_cargo > 0
            ORDER BY total_passengers DESC
        """
        cursor.execute(share_query, params)
        shares = cursor.fetchall()
        
        # D. Monthly Breakdown by Airline (for details grid)
        breakdown_query = f"""
            SELECT 
                a.name as airline_name,
                SUM(t.departures) as departures,
                SUM(t.passengers_carried) as passengers,
                ROUND(SUM(t.pax_kms_performed) / SUM(t.available_seat_kms) * 100.0, 2) as load_factor,
                SUM(t.cargo_total) as cargo,
                ROUND(SUM(t.tkm_total) / SUM(t.available_tkm) * 100.0, 2) as weight_load_factor
            FROM monthly_traffic t
            JOIN airlines a ON t.airline_id = a.id
            {where_clause_airlines}
            GROUP BY a.id, a.name
            ORDER BY passengers DESC
        """
        cursor.execute(breakdown_query, params)
        airline_breakdown = cursor.fetchall()
        
        return {
            "summary": summary,
            "monthly_trends": monthly_raw,
            "market_share": shares,
            "airline_breakdown": airline_breakdown
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post("/api/sync")
def sync_data(year: int = Query(..., description="Year to sync"), background_tasks: BackgroundTasks = None):
    """Triggers the background crawling and parsing pipeline for the specified year."""
    global pipeline_status
    if pipeline_status["status"] == "running":
        raise HTTPException(status_code=400, detail="Pipeline is already running.")
    
    if background_tasks:
        background_tasks.add_task(run_sync_pipeline, year)
    else:
        # Fallback if background_tasks is not injected
        import threading
        t = threading.Thread(target=run_sync_pipeline, args=(year,))
        t.start()
        
    return {"message": f"Sync started for year {year}."}

@app.get("/api/sync/status")
def sync_status():
    """Returns the current pipeline running status and console logs."""
    global pipeline_status
    return pipeline_status

# Mount the frontend dashboard static directory
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="public")
else:
    print(f"[Warning] Static files directory '{frontend_dir}' does not exist yet. Please create it to serve the UI dashboard.")

