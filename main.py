import os
import sqlite3

DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "aviation_stats.db"
)

def get_db_connection(db_path=DEFAULT_DB_PATH):
    """Establishes and returns a connection to the SQLite database."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=DEFAULT_DB_PATH):
    """Initializes the SQLite database with required tables and schemas."""
    print(f"Initializing database at: {db_path}")
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # Create airlines table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS airlines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        code TEXT
    )
    """)
    
    # Create monthly_traffic table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monthly_traffic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        airline_id INTEGER NOT NULL,
        year INTEGER NOT NULL,
        month TEXT NOT NULL,
        service_type TEXT NOT NULL, -- 'Domestic' or 'International'
        scheduled INTEGER NOT NULL,  -- 1 for Scheduled, 0 for Non-Scheduled
        departures INTEGER DEFAULT 0,
        hours_flown REAL DEFAULT 0.0,
        kms_flown REAL DEFAULT 0.0,
        passengers_carried INTEGER DEFAULT 0,
        pax_kms_performed REAL DEFAULT 0.0,
        available_seat_kms REAL DEFAULT 0.0,
        pax_load_factor REAL DEFAULT 0.0,
        cargo_freight REAL DEFAULT 0.0,
        cargo_mail REAL DEFAULT 0.0,
        cargo_total REAL DEFAULT 0.0,
        tkm_passenger REAL DEFAULT 0.0,
        tkm_freight REAL DEFAULT 0.0,
        tkm_mail REAL DEFAULT 0.0,
        tkm_total REAL DEFAULT 0.0,
        available_tkm REAL DEFAULT 0.0,
        weight_load_factor REAL DEFAULT 0.0,
        FOREIGN KEY (airline_id) REFERENCES airlines (id),
        UNIQUE(airline_id, year, month, service_type, scheduled)
    )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialization complete.")

def insert_records(records, db_path=DEFAULT_DB_PATH):
    """Inserts a list of parsed traffic records into the database."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    airline_cache = {}
    inserted_count = 0
    
    try:
        for record in records:
            airline_name = record['airline']
            
            # Get or insert airline
            if airline_name not in airline_cache:
                cursor.execute("SELECT id FROM airlines WHERE name = ?", (airline_name,))
                row = cursor.fetchone()
                if row:
                    airline_cache[airline_name] = row['id']
                else:
                    cursor.execute("INSERT INTO airlines (name) VALUES (?)", (airline_name,))
                    airline_cache[airline_name] = cursor.lastrowid
                    
            airline_id = airline_cache[airline_name]
            
            # Insert traffic record (or replace if it already exists)
            cursor.execute("""
            INSERT OR REPLACE INTO monthly_traffic (
                airline_id, year, month, service_type, scheduled,
                departures, hours_flown, kms_flown, passengers_carried,
                pax_kms_performed, available_seat_kms, pax_load_factor,
                cargo_freight, cargo_mail, cargo_total, tkm_passenger,
                tkm_freight, tkm_mail, tkm_total, available_tkm, weight_load_factor
            ) VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?, ?
            )
            """, (
                airline_id, record['year'], record['month'], record['service_type'], 1 if record['scheduled'] else 0,
                record['departures'], record['hours_flown'], record['kms_flown'], record['passengers_carried'],
                record['pax_kms_performed'], record['available_seat_kms'], record['pax_load_factor'],
                record['cargo_freight'], record['cargo_mail'], record['cargo_total'], record['tkm_passenger'],
                record['tkm_freight'], record['tkm_mail'], record['tkm_total'], record['available_tkm'], record['weight_load_factor']
            ))
            inserted_count += 1
            
        conn.commit()
        print(f"Successfully ingested {inserted_count} records into the database.")
    except Exception as e:
        conn.rollback()
        print(f"[Error] Failed to ingest records: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
