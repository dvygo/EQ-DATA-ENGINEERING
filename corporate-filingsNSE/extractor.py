import os
import csv
from datetime import datetime
import re
try:
    from openpyxl import load_workbook
except ImportError:
    print("openpyxl not installed. Installing...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'openpyxl'])
    from openpyxl import load_workbook

def create_csv_folder(symbol):
    """Create CSV folder for the symbol"""
    base_dir = os.path.dirname(__file__)
    csv_dir = os.path.join(base_dir, 'DATA', symbol.lower(), 'CSV')
    os.makedirs(csv_dir, exist_ok=True)
    return csv_dir

def extract_date_from_filename(filename):
    """Extract date from filename and convert to readable format"""
    # Extract date part from filename (e.g., "03Jun2020" from "03Jun2020_1145_...")
    date_match = re.match(r'(\d{2}[A-Za-z]{3}\d{4})', filename)
    if date_match:
        date_str = date_match.group(1)
        try:
            # Parse the date
            date_obj = datetime.strptime(date_str, '%d%b%Y')
            return date_obj.strftime('%d%b%Y')  # Return in same format
        except ValueError:
            return date_str
    return filename.split('_')[0]  # Fallback

def extract_fields_from_excel(excel_filepath):
    """Extract PaidUpValue and FaceValue fields from Excel file"""
    try:
        # Load Excel file using openpyxl
        workbook = load_workbook(excel_filepath, data_only=True)
        
        # Initialize values
        paid_up_value = None
        face_value = None
        
        # Search in all worksheets
        for sheet_name in workbook.sheetnames:
            worksheet = workbook[sheet_name]
            
            # Search through all cells
            for row in worksheet.iter_rows():
                for cell in row:
                    if cell.value is None:
                        continue
                    
                    cell_value = str(cell.value).strip()
                    
                    # Look for PaidUpValueOfEquityShareCapital
                    if 'PaidUpValueOfEquityShareCapital' in cell_value:
                        # Check adjacent cells for the value
                        row_num = cell.row
                        col_num = cell.column
                        
                        # Check cells to the right
                        for offset in range(1, 5):
                            try:
                                adjacent_cell = worksheet.cell(row=row_num, column=col_num + offset)
                                if adjacent_cell.value is not None:
                                    val = str(adjacent_cell.value).strip()
                                    if val.replace('.', '').replace(',', '').isdigit() or re.match(r'^\d+\.?\d*$', val):
                                        # Remove decimal places for paid up value to keep data clean
                                        paid_up_value = val.split('.')[0]
                                        break
                            except:
                                continue
                    
                    # Look for FaceValueOfEquityShareCapital
                    if 'FaceValueOfEquityShareCapital' in cell_value:
                        # Check adjacent cells for the value
                        row_num = cell.row
                        col_num = cell.column
                        
                        # Check cells to the right
                        for offset in range(1, 5):
                            try:
                                adjacent_cell = worksheet.cell(row=row_num, column=col_num + offset)
                                if adjacent_cell.value is not None:
                                    val = str(adjacent_cell.value).strip()
                                    if val.replace('.', '').replace(',', '').isdigit() or re.match(r'^\d+\.?\d*$', val):
                                        face_value = val
                                        break
                            except:
                                continue
                    
                    # Break if both values found
                    if paid_up_value and face_value:
                        break
                
                if paid_up_value and face_value:
                    break
            
            if paid_up_value and face_value:
                break
        
        workbook.close()
        return paid_up_value, face_value
        
    except Exception as e:
        print(f"[ERROR] Failed to process {os.path.basename(excel_filepath)}: {e}")
        return None, None

def extract_all_excel_files(symbol):
    """Extract fields from all Excel files for a symbol"""
    base_dir = os.path.dirname(__file__)
    xlsx_dir = os.path.join(base_dir, 'DATA', symbol.lower(), 'XLSX')
    
    # Check if XLSX directory exists
    if not os.path.exists(xlsx_dir):
        print(f"[ERROR] XLSX directory not found: {xlsx_dir}")
        return False
    
    # Create CSV directory
    csv_dir = create_csv_folder(symbol)
    
    # Get all Excel files
    excel_files = [f for f in os.listdir(xlsx_dir) if f.endswith('.xlsx')]
    
    if not excel_files:
        print(f"[ERROR] No Excel files found in {xlsx_dir}")
        return False
    
    print(f"Found {len(excel_files)} Excel files to process")
    
    # Prepare data for CSV
    extracted_data = []
    processed_count = 0
    failed_count = 0
    
    for excel_file in sorted(excel_files):  # Sort to maintain chronological order
        excel_filepath = os.path.join(xlsx_dir, excel_file)
        
        print(f"Processing: {excel_file}")
        
        # Extract date from filename
        filing_date = extract_date_from_filename(excel_file)
        
        # Extract fields
        paid_up_value, face_value = extract_fields_from_excel(excel_filepath)
        
        if paid_up_value is not None or face_value is not None:
            # Check if we already have data for this date
            existing_entry = None
            for i, entry in enumerate(extracted_data):
                if entry[0] == filing_date:
                    existing_entry = i
                    break
            
            # Calculate number of shares (PaidUp / FaceValue)
            number_of_shares = 'N/A'
            if paid_up_value and face_value and paid_up_value != 'N/A' and face_value != 'N/A':
                try:
                    paid_up_num = float(paid_up_value)
                    face_value_num = float(face_value)
                    if face_value_num != 0:
                        number_of_shares = int(paid_up_num / face_value_num)
                except (ValueError, ZeroDivisionError):
                    number_of_shares = 'N/A'
            
            new_entry = [
                filing_date,
                paid_up_value if paid_up_value else 'N/A',
                face_value if face_value else 'N/A',
                number_of_shares
            ]
            
            if existing_entry is not None:
                # Update existing entry if new data is more complete
                existing = extracted_data[existing_entry]
                if (paid_up_value and existing[1] == 'N/A') or (face_value and existing[2] == 'N/A'):
                    extracted_data[existing_entry] = new_entry
                    print(f"[UPDATE] Updated existing entry: Date={filing_date}, PaidUp={paid_up_value}, Face={face_value}, Shares={number_of_shares}")
                else:
                    print(f"[SKIP] Duplicate date found: Date={filing_date} (keeping existing data)")
            else:
                extracted_data.append(new_entry)
                processed_count += 1
                print(f"[OK] Extracted: Date={filing_date}, PaidUp={paid_up_value}, Face={face_value}, Shares={number_of_shares}")
        else:
            failed_count += 1
            print(f"[FAIL] No data found in {excel_file}")
    
    # Sort data by date in reverse chronological order (newest first)
    def parse_date_for_sorting(date_str):
        """Parse date string for sorting purposes"""
        try:
            return datetime.strptime(date_str, '%d%b%Y')
        except ValueError:
            # Fallback for any date parsing issues
            return datetime.min
    
    extracted_data.sort(key=lambda x: parse_date_for_sorting(x[0]), reverse=True)
    
    # Save to CSV
    csv_filename = f'{symbol.lower()}_extracted_data.csv'
    csv_filepath = os.path.join(csv_dir, csv_filename)
    
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['FilingDate', 'PaidUpValueOfEquityShareCapital', 'FaceValueOfEquityShareCapital', 'NumberOfShares'])
        
        # Write data (now sorted in reverse chronological order)
        writer.writerows(extracted_data)
    
    # Print summary
    print(f"\nExtraction Summary:")
    print(f"[OK] Successfully processed: {processed_count} files")
    print(f"[FAIL] Failed to extract: {failed_count} files")
    print(f"[INFO] CSV file saved to: {csv_filepath}")
    
    return processed_count > 0

def main():
    """Main function to extract data from Excel files"""
    symbol = "RELIANCE"
    print(f"Starting data extraction for {symbol}")
    print("=" * 50)
    
    success = extract_all_excel_files(symbol)
    
    if success:
        print(f"\n[SUCCESS] Data extraction completed for {symbol}")
    else:
        print(f"\n[FAILED] Data extraction failed for {symbol}")

if __name__ == "__main__":
    main()
