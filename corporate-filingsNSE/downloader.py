import requests
import json
import os
import time
from urllib.parse import urlparse
from pathlib import Path

def download_xbrl_file(url, filepath):
    """Download XBRL file from URL and save to filepath"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/xml, text/xml, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/"
    }
    
    try:
        print(f"Downloading: {os.path.basename(filepath)}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save the file
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"[OK] Downloaded: {os.path.basename(filepath)} ({len(response.content)} bytes)")
        return True
        
    except requests.RequestException as e:
        print(f"[FAIL] Failed to download {os.path.basename(filepath)}: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error saving {os.path.basename(filepath)}: {e}")
        return False

def get_filename_from_url(url):
    """Extract filename from XBRL URL"""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # If no extension, add .xml
    if not filename.endswith('.xml'):
        filename += '.xml'
    
    return filename

def is_valid_xbrl_link(xbrl_link):
    """Check if XBRL link is valid and not empty"""
    if not xbrl_link:
        return False
    
    # Check if it's just the base URL without actual file
    if xbrl_link.endswith('xbrl/-') or xbrl_link.endswith('xbrl/'):
        return False
    
    # Check if it contains a proper XML file
    if '.xml' not in xbrl_link.lower():
        return False
    
    return True

def create_symbol_directories(symbol):
    """Create DATA/{symbol}/XBRL directory structure"""
    base_dir = os.path.dirname(__file__)
    symbol_dir = os.path.join(base_dir, 'DATA', symbol.lower())
    xbrl_dir = os.path.join(symbol_dir, 'XBRL')
    
    # Create directories if they don't exist
    os.makedirs(xbrl_dir, exist_ok=True)
    return xbrl_dir

def read_json_and_download(symbol):
    """Read JSON file and download all XBRL files for a symbol"""
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, 'JSON', f'{symbol.lower()}.json')
    
    # Check if JSON file exists
    if not os.path.exists(json_path):
        print(f"[ERROR] JSON file not found: {json_path}")
        return False
    
    # Create XBRL directory for this symbol
    xbrl_dir = create_symbol_directories(symbol)
    print(f"XBRL files will be saved to: {xbrl_dir}")
    
    # Read JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to read JSON file for {symbol}: {e}")
        return False
    
    if not data:
        print(f"[ERROR] No data found in JSON file for {symbol}")
        return False
    
    # Download files
    downloaded_count = 0
    failed_count = 0
    skipped_count = 0
    
    for record in data:
        xbrl_url = record.get('xbrl', '').strip()
        filing_date = record.get('filingDate', '').strip()
        
        # Skip records with invalid XBRL links
        if not is_valid_xbrl_link(xbrl_url):
            continue
        
        # Generate filename
        filename = get_filename_from_url(xbrl_url)
        
        # Add filing date prefix for better organization
        if filing_date:
            # Clean filing date for filename (remove special characters)
            clean_date = filing_date.replace(':', '').replace(' ', '_').replace('-', '')
            filename = f"{clean_date}_{filename}"
        
        filepath = os.path.join(xbrl_dir, filename)
        
        # Skip if file already exists
        if os.path.exists(filepath):
            print(f"[SKIP] {filename} (already exists)")
            skipped_count += 1
            continue
        
        # Download the file
        if download_xbrl_file(xbrl_url, filepath):
            downloaded_count += 1
        else:
            failed_count += 1
        
        # Add small delay to be respectful to the server
        time.sleep(1)
    
    print(f"\nDownload Summary for {symbol}:")
    print(f"[OK] Successfully downloaded: {downloaded_count} files")
    print(f"[SKIP] Already existed: {skipped_count} files")
    print(f"[FAIL] Failed downloads: {failed_count} files")
    print(f"[INFO] Files saved to: {xbrl_dir}")
    
    return downloaded_count > 0

def get_available_symbols():
    """Get list of available symbols from JSON folder"""
    base_dir = os.path.dirname(__file__)
    json_dir = os.path.join(base_dir, 'JSON')
    
    if not os.path.exists(json_dir):
        print(f"[ERROR] JSON directory not found: {json_dir}")
        return []
    
    symbols = []
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            symbol = filename[:-5].upper()  # Remove .json and convert to uppercase
            symbols.append(symbol)
    
    return sorted(symbols)

def download_all_symbols():
    """Download XBRL files for all available symbols"""
    print("Starting bulk XBRL download for all symbols...")
    print("=" * 60)
    
    # Get available symbols
    symbols = get_available_symbols()
    if not symbols:
        print("No JSON files found. Run fetcher.py first.")
        return
    
    print(f"Found {len(symbols)} symbols to process")
    
    # Process each symbol
    total_successful = 0
    total_failed = 0
    
    for i, symbol in enumerate(symbols, 1):
        print(f"\n[{i}/{len(symbols)}] Processing {symbol}...")
        
        if read_json_and_download(symbol):
            total_successful += 1
        else:
            total_failed += 1
    
    # Print final summary
    print(f"\nFinal Summary:")
    print(f"[OK] Successfully processed: {total_successful} symbols")
    print(f"[FAIL] Failed to process: {total_failed} symbols")
    print(f"[INFO] XBRL files organized in DATA/{{symbol}}/XBRL/ folders")

def main():
    """Main function to download XBRL files for all symbols"""
    download_all_symbols()

if __name__ == "__main__":
    main()