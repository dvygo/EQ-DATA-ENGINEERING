import os
from converter import upload_and_convert_xbrl, save_excel_file, create_xlsx_folder

def test_single_conversion():
    """Test converting a single XBRL file"""
    
    # Get the first XBRL file
    xbrl_dir = "DATA/reliance/XBRL"
    xbrl_files = [f for f in os.listdir(xbrl_dir) if f.endswith('.xml')]
    
    if not xbrl_files:
        print("No XBRL files found")
        return
    
    # Use a smaller file for testing
    test_file = None
    for f in xbrl_files:
        filepath = os.path.join(xbrl_dir, f)
        if os.path.getsize(filepath) < 50000:  # Less than 50KB
            test_file = filepath
            break
    
    if not test_file:
        test_file = os.path.join(xbrl_dir, xbrl_files[0])
    
    print(f"Testing with file: {os.path.basename(test_file)}")
    print(f"File size: {os.path.getsize(test_file)} bytes")
    
    # Create XLSX folder
    xlsx_dir = create_xlsx_folder("RELIANCE")
    
    # Test conversion
    ec2_url = "http://ec2-3-221-41-38.compute-1.amazonaws.com/"
    excel_data = upload_and_convert_xbrl(test_file, ec2_url)
    
    if excel_data:
        print(f"[SUCCESS] Received {len(excel_data)} bytes of data")
        
        # Save the file
        if save_excel_file(excel_data, xlsx_dir, os.path.basename(test_file)):
            print("[SUCCESS] File saved successfully")
        else:
            print("[FAIL] Failed to save file")
    else:
        print("[FAIL] No Excel data received")

if __name__ == "__main__":
    test_single_conversion()
