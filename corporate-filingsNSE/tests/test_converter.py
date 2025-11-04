import requests
import os

def test_single_upload():
    """Test uploading a single XBRL file to see the response"""
    
    # Get the first XBRL file
    xbrl_dir = "DATA/reliance/XBRL"
    xbrl_files = [f for f in os.listdir(xbrl_dir) if f.endswith('.xml')]
    
    if not xbrl_files:
        print("No XBRL files found")
        return
    
    test_file = os.path.join(xbrl_dir, xbrl_files[0])
    print(f"Testing with file: {xbrl_files[0]}")
    
    ec2_url = "http://ec2-3-221-41-38.compute-1.amazonaws.com/"
    
    try:
        with open(test_file, 'rb') as f:
            files = {'file': (xbrl_files[0], f, 'application/xml')}
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            print("Uploading file...")
            response = requests.post(ec2_url, files=files, headers=headers, timeout=60)
            
            print(f"Status Code: {response.status_code}")
            print(f"Content Type: {response.headers.get('content-type', 'Unknown')}")
            print(f"Content Length: {len(response.content)} bytes")
            print(f"Response Headers: {dict(response.headers)}")
            
            # Save response for inspection
            with open("test_response.html", 'wb') as f:
                f.write(response.content)
            
            print("Response saved to test_response.html")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_single_upload()
