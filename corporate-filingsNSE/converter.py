import requests
import os
import time
from pathlib import Path

def create_xlsx_folder(symbol):
    """Create XLSX folder for the symbol"""
    base_dir = os.path.dirname(__file__)
    xlsx_dir = os.path.join(base_dir, 'DATA', symbol.lower(), 'XLSX')
    os.makedirs(xlsx_dir, exist_ok=True)
    return xlsx_dir

def extract_viewstate_and_validation(html_content):
    """Extract ViewState and validation fields from ASP.NET page"""
    import re
    
    viewstate_match = re.search(r'name="__VIEWSTATE".*?value="([^"]*)"', html_content, re.DOTALL)
    viewstate_generator_match = re.search(r'name="__VIEWSTATEGENERATOR".*?value="([^"]*)"', html_content, re.DOTALL)
    event_validation_match = re.search(r'name="__EVENTVALIDATION".*?value="([^"]*)"', html_content, re.DOTALL)
    
    return {
        '__VIEWSTATE': viewstate_match.group(1) if viewstate_match else '',
        '__VIEWSTATEGENERATOR': viewstate_generator_match.group(1) if viewstate_generator_match else '',
        '__EVENTVALIDATION': event_validation_match.group(1) if event_validation_match else ''
    }

def upload_and_convert_xbrl(xbrl_filepath, ec2_url):
    """Upload XBRL file to EC2 converter and get converted Excel file"""
    try:
        filename = os.path.basename(xbrl_filepath)
        print(f"Converting: {filename}")
        
        session = requests.Session()
        
        # Step 1: Get the initial page to extract ViewState
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }
        
        initial_response = session.get(ec2_url, headers=headers)
        initial_response.raise_for_status()
        
        # Extract ViewState and other ASP.NET fields
        form_data = extract_viewstate_and_validation(initial_response.text)
        
        # Step 2: Upload the file with proper form data
        with open(xbrl_filepath, 'rb') as f:
            files = {
                'FileUploadControl': (filename, f, 'application/xml')
            }
            
            # Add ASP.NET form fields
            data = {
                '__EVENTTARGET': 'Button1',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': form_data['__VIEWSTATE'],
                '__VIEWSTATEGENERATOR': form_data['__VIEWSTATEGENERATOR'],
                '__EVENTVALIDATION': form_data['__EVENTVALIDATION'],
                'Button1': 'Validate'
            }
            
            # Submit the form
            response = session.post(ec2_url, files=files, data=data, headers=headers, timeout=120)
            response.raise_for_status()
            
            # Check for Excel file indicators
            if ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in response.headers.get('content-type', '').lower() or
                'application/octet-stream' in response.headers.get('content-type', '').lower() or
                'excel' in response.headers.get('content-type', '').lower() or
                response.headers.get('content-disposition', '').startswith('attachment')):
                return response.content
            
            # Check if response is large (likely an Excel file)
            if len(response.content) > 10000:  # Excel files are typically larger
                # Check if it starts with Excel file signature
                if response.content[:2] == b'PK':  # ZIP/Excel file signature
                    return response.content
            
            print(f"[INFO] Response content type: {response.headers.get('content-type', '')}")
            print(f"[INFO] Response length: {len(response.content)} bytes")
            
            return None
                
    except requests.RequestException as e:
        print(f"[FAIL] Upload failed for {filename}: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Error processing {filename}: {e}")
        return None

def save_excel_file(excel_data, xlsx_dir, original_filename):
    """Save Excel data to XLSX folder"""
    # Create Excel filename from original XBRL filename
    excel_filename = original_filename.replace('.xml', '.xlsx')
    excel_filepath = os.path.join(xlsx_dir, excel_filename)
    
    try:
        with open(excel_filepath, 'wb') as f:
            f.write(excel_data)
        
        print(f"[OK] Saved: {excel_filename} ({len(excel_data)} bytes)")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to save {excel_filename}: {e}")
        return False

def convert_symbol_xbrl_files(symbol):
    """Convert all XBRL files for a specific symbol to Excel"""
    base_dir = os.path.dirname(__file__)
    xbrl_dir = os.path.join(base_dir, 'DATA', symbol.lower(), 'XBRL')
    
    # Check if XBRL directory exists
    if not os.path.exists(xbrl_dir):
        print(f"[SKIP] No XBRL directory found for {symbol}: {xbrl_dir}")
        return False
    
    # Create XLSX directory
    xlsx_dir = create_xlsx_folder(symbol)
    print(f"Excel files will be saved to: {xlsx_dir}")
    
    # EC2 converter URL
    ec2_url = "http://ec2-3-221-41-38.compute-1.amazonaws.com/"
    
    # Get all XBRL files
    xbrl_files = [f for f in os.listdir(xbrl_dir) if f.endswith('.xml')]
    
    if not xbrl_files:
        print(f"[SKIP] No XBRL files found for {symbol} in {xbrl_dir}")
        return False
    
    print(f"Found {len(xbrl_files)} XBRL files to convert for {symbol}")
    
    # Convert each file
    converted_count = 0
    failed_count = 0
    skipped_count = 0
    
    for xbrl_file in xbrl_files:
        xbrl_filepath = os.path.join(xbrl_dir, xbrl_file)
        excel_filename = xbrl_file.replace('.xml', '.xlsx')
        excel_filepath = os.path.join(xlsx_dir, excel_filename)
        
        # Skip if Excel file already exists
        if os.path.exists(excel_filepath):
            print(f"[SKIP] {excel_filename} (already exists)")
            skipped_count += 1
            continue
        
        # Upload and convert
        excel_data = upload_and_convert_xbrl(xbrl_filepath, ec2_url)
        
        if excel_data:
            if save_excel_file(excel_data, xlsx_dir, xbrl_file):
                converted_count += 1
            else:
                failed_count += 1
        else:
            failed_count += 1
        
        # Add delay to be respectful to the server
        time.sleep(2)
    
    # Print summary for this symbol
    print(f"\nConversion Summary for {symbol}:")
    print(f"[OK] Successfully converted: {converted_count} files")
    print(f"[SKIP] Already existed: {skipped_count} files")
    print(f"[FAIL] Failed conversions: {failed_count} files")
    print(f"[INFO] Excel files saved to: {xlsx_dir}")
    
    return converted_count > 0

def get_available_symbols_with_xbrl():
    """Get list of symbols that have XBRL directories"""
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'DATA')
    
    if not os.path.exists(data_dir):
        print(f"[ERROR] DATA directory not found: {data_dir}")
        return []
    
    symbols = []
    for item in os.listdir(data_dir):
        symbol_dir = os.path.join(data_dir, item)
        xbrl_dir = os.path.join(symbol_dir, 'XBRL')
        
        # Check if it's a directory and has XBRL subdirectory
        if os.path.isdir(symbol_dir) and os.path.exists(xbrl_dir):
            symbols.append(item.upper())
    
    return sorted(symbols)

def convert_all_symbols():
    """Convert XBRL files to Excel for all available symbols"""
    print("Starting bulk XBRL to Excel conversion for all symbols...")
    print("=" * 70)
    
    # Get available symbols with XBRL directories
    symbols = get_available_symbols_with_xbrl()
    if not symbols:
        print("No symbols with XBRL directories found. Run downloader.py first.")
        return
    
    print(f"Found {len(symbols)} symbols with XBRL files to process")
    
    # Process each symbol
    total_successful = 0
    total_failed = 0
    
    for i, symbol in enumerate(symbols, 1):
        print(f"\n[{i}/{len(symbols)}] Processing {symbol}...")
        print("-" * 50)
        
        if convert_symbol_xbrl_files(symbol):
            total_successful += 1
        else:
            total_failed += 1
    
    # Print final summary
    print(f"\nFinal Conversion Summary:")
    print(f"=" * 70)
    print(f"[OK] Successfully processed: {total_successful} symbols")
    print(f"[FAIL] Failed to process: {total_failed} symbols")
    print(f"[INFO] Excel files organized in DATA/{{symbol}}/XLSX/ folders")

def main():
    """Main function to convert XBRL files to Excel for all symbols"""
    convert_all_symbols()

if __name__ == "__main__":
    main()