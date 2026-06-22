import os
import re
import json
import pdfplumber
import pandas as pd

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

def clean_num(val):
    """Cleans a string representation of a number and converts it to float or int."""
    if not val:
        return 0.0
    val_str = str(val).replace(',', '').strip()
    if val_str == '' or val_str == '-' or val_str.upper() == 'NIL':
        return 0.0
    try:
        if '.' in val_str:
            return float(val_str)
        else:
            return int(val_str)
    except ValueError:
        return 0.0

def align_tokens(tokens):
    """Aligns row tokens to ensure we have exactly 17 elements (Month + 16 numeric columns)."""
    if not tokens:
        return None
        
    month = tokens[0].upper()
    if month not in MONTHS:
        return None
        
    if len(tokens) == 1:
        # Month name only, rest are zeros
        return [month] + [0.0] * 16
        
    if len(tokens) == 16:
        # Check if passenger load factor is missing (index 7)
        # Typically when passengers, pax_kms, and available_seat_kms are all 0
        if tokens[4] == '0' and tokens[5] == '0' and tokens[6] == '0':
            tokens.insert(7, '0.0')
            
    if len(tokens) == 17:
        return tokens
        
    # If it's still not 17, pad or truncate
    if len(tokens) < 17:
        print(f"[Warning] Under-tokenized row {tokens[0]}: {len(tokens)} tokens. Padding with zeros.")
        return tokens + [0.0] * (17 - len(tokens))
    else:
        print(f"[Warning] Over-tokenized row {tokens[0]}: {len(tokens)} tokens. Truncating.")
        return tokens[:17]

def parse_pdf_report(pdf_path, airline_name, year):
    """Parses a single PDF report and returns structured records."""
    records = []
    
    if not os.path.exists(pdf_path):
        print(f"[Error] PDF file not found: {pdf_path}")
        return records
        
    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
                
            text_upper = text.upper()
            
            # Determine Service Type and Scheduled status
            service_type = "Domestic"
            if "INTERNATIONAL" in text_upper:
                service_type = "International"
                
            scheduled = True
            if "NON- SCHEDULED" in text_upper or "NON-SCHEDULED" in text_upper:
                scheduled = False
                
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Clean None and extra whitespaces
                    cells = [str(c).strip() for c in row if c is not None and str(c).strip() != '']
                    row_str = " ".join(cells)
                    tokens = row_str.split()
                    
                    if not tokens:
                        continue
                        
                    month = tokens[0].upper()
                    if month in MONTHS:
                        aligned = align_tokens(tokens)
                        if aligned:
                            records.append({
                                'airline': airline_name,
                                'year': int(year),
                                'month': aligned[0],
                                'service_type': service_type,
                                'scheduled': scheduled,
                                'departures': int(clean_num(aligned[1])),
                                'hours_flown': float(clean_num(aligned[2])),
                                'kms_flown': float(clean_num(aligned[3])),
                                'passengers_carried': int(clean_num(aligned[4])),
                                'pax_kms_performed': float(clean_num(aligned[5])),
                                'available_seat_kms': float(clean_num(aligned[6])),
                                'pax_load_factor': float(clean_num(aligned[7])),
                                'cargo_freight': float(clean_num(aligned[8])),
                                'cargo_mail': float(clean_num(aligned[9])),
                                'cargo_total': float(clean_num(aligned[10])),
                                'tkm_passenger': float(clean_num(aligned[11])),
                                'tkm_freight': float(clean_num(aligned[12])),
                                'tkm_mail': float(clean_num(aligned[13])),
                                'tkm_total': float(clean_num(aligned[14])),
                                'available_tkm': float(clean_num(aligned[15])),
                                'weight_load_factor': float(clean_num(aligned[16]))
                            })
                            
    return records

def run_parser(metadata_path="data/raw/scraper_metadata.json"):
    """Orchestrates parsing of all downloaded reports in metadata."""
    print("Starting DGCA Report Parser...")
    
    if not os.path.exists(metadata_path):
        print(f"[Error] Scraper metadata file not found at: {metadata_path}")
        return []
        
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
        
    all_records = []
    
    for year, reps in metadata.items():
        for rep in reps:
            pdf_local = rep['pdf_local_path']
            # Make path absolute if it's relative
            if pdf_local and not os.path.isabs(pdf_local):
                # Resolve relative to project root (parent of src)
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                pdf_local = os.path.join(project_root, pdf_local)
                
            if pdf_local and os.path.exists(pdf_local):
                print(f"Parsing PDF for {rep['airline']} ({year})...")
                records = parse_pdf_report(pdf_local, rep['airline'], year)
                all_records.extend(records)
                print(f"  Extracted {len(records)} monthly records.")
            else:
                print(f"[Warning] PDF not downloaded or missing for {rep['airline']} ({year})")
                
    print(f"\nParsing complete. Extracted total {len(all_records)} records.")
    return all_records

if __name__ == "__main__":
    # Test run parser on local metadata
    records = run_parser()
    if records:
        print(f"First parsed record: {records[0]}")
