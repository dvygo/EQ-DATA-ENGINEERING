import requests
import json
import os
import time
from datetime import datetime

def read_symbols_from_file():
    """Read symbols from test_symbols.txt file"""
    symbols = []
    symbols_file = os.path.join(os.path.dirname(__file__), 'test_symbols.txt')
    
    try:
        with open(symbols_file, 'r', encoding='utf-8') as f:
            for line in f:
                symbol = line.strip()
                if symbol:  # Skip empty lines
                    symbols.append(symbol)
        print(f"Loaded {len(symbols)} symbols from test_symbols.txt")
        return symbols
    except FileNotFoundError:
        print("Error: test_symbols.txt file not found")
        return []
    except Exception as e:
        print(f"Error reading symbols file: {e}")
        return []

def create_json_folder():
    """Create JSON folder if it doesn't exist"""
    json_dir = os.path.join(os.path.dirname(__file__), 'JSON')
    os.makedirs(json_dir, exist_ok=True)
    return json_dir

def fetch_symbol_data(symbol):
    """Fetch financial results data for a specific symbol from NSE API"""
    url = "https://www.nseindia.com/api/corporates-financial-results"
    params = {
        "index": "equities",
        "symbol": symbol, 
        "period": "Quarterly"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/"
    }
    
    try:
        print(f"Fetching data for {symbol}...")
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch data for {symbol}: {e}")
        return None

def save_json_data(symbol, data, json_dir):
    """Save JSON data for a symbol"""
    filename = f"{symbol.lower()}_data.json"
    filepath = os.path.join(json_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Saved JSON data for {symbol}: {filepath}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save JSON for {symbol}: {e}")
        return False

def main():
    """Test function to fetch data for test symbols"""
    print("Testing bulk symbol data fetching...")
    print("=" * 50)
    
    # Read symbols from file
    symbols = read_symbols_from_file()
    if not symbols:
        print("No symbols found. Exiting.")
        return
    
    # Create JSON directory
    json_dir = create_json_folder()
    print(f"JSON files will be saved to: {json_dir}")
    
    # Fetch data for each symbol
    successful_count = 0
    failed_count = 0
    
    for i, symbol in enumerate(symbols, 1):
        print(f"\n[{i}/{len(symbols)}] Processing {symbol}...")
        
        # Fetch data for symbol
        data = fetch_symbol_data(symbol)
        
        if data:
            # Save JSON data
            if save_json_data(symbol, data, json_dir):
                successful_count += 1
            else:
                failed_count += 1
        else:
            failed_count += 1
        
        # Add delay to be respectful to the server
        if i < len(symbols):  # Don't delay after the last symbol
            time.sleep(2)
    
    # Print summary
    print(f"\nFetching Summary:")
    print(f"[OK] Successfully fetched: {successful_count} symbols")
    print(f"[FAIL] Failed to fetch: {failed_count} symbols")
    print(f"[INFO] JSON files saved to: {json_dir}")

if __name__ == "__main__":
    main()
