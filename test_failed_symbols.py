import requests
import json
import os

def test_symbol_fetch(symbol):
    """Test fetching data for a specific symbol"""
    print(f"\n=== Testing {symbol} ===")
    
    url = f"https://www.nseindia.com/api/corporates-financial-results?index=equities&symbol={symbol}&period=Quarterly"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.nseindia.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    try:
        print(f"URL: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON Response Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                if isinstance(data, dict) and 'data' in data:
                    print(f"Data Records: {len(data['data']) if data['data'] else 0}")
                else:
                    print(f"Response Content: {str(data)[:200]}...")
                return True
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
                print(f"Response Text: {response.text[:500]}...")
                return False
        else:
            print(f"HTTP Error: {response.status_code}")
            print(f"Response Text: {response.text[:500]}...")
            return False
            
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return False

# Test the 3 failed symbols
failed_symbols = ['HDFCLIFE', 'SBILIFE', 'TATAMOTORS']

for symbol in failed_symbols:
    success = test_symbol_fetch(symbol)
    print(f"Result for {symbol}: {'SUCCESS' if success else 'FAILED'}")
    print("-" * 50)
