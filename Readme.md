# NSE Corporate Filings Data Pipeline

A comprehensive Python pipeline to fetch, download, convert, and extract financial data from NSE (National Stock Exchange) corporate filings.

## Overview

This pipeline automates the process of:
1. **Fetching** corporate filing data from NSE API
2. **Downloading** XBRL files from filing links  
3. **Converting** XBRL files to Excel format
4. **Extracting** specific financial metrics to CSV

## Quick Start

### Prerequisites

```bash
pip install requests openpyxl
```

### Basic Usage

1. **Prepare symbols list**:
   ```bash
   # Edit symbols.txt with your stock symbols (one per line)
   echo "RELIANCE" > symbols.txt
   echo "TCS" >> symbols.txt
   ```

2. **Run the complete pipeline**:
   ```bash
   python fetcher.py      # Step 1: Fetch JSON data
   python downloader.py   # Step 2: Download XBRL files  
   python converter.py    # Step 3: Convert to Excel
   python extractor.py    # Step 4: Extract to CSV
   ```

## Detailed Usage

### Step 1: Fetch Corporate Filing Data

```bash
python fetcher.py
```

**What it does:**
- Reads stock symbols from `symbols.txt`
- Fetches corporate filing data from NSE API
- Saves raw JSON responses to `JSON/{symbol}.json`

**Output:**
```
JSON/
├── reliance.json
├── tcs.json
└── infy.json
```

### Step 2: Download XBRL Files

```bash
python downloader.py
```

**What it does:**
- Reads JSON files from `JSON/` folder
- Downloads XBRL files with valid links
- Organizes files by symbol in `DATA/{symbol}/XBRL/`

**Output:**
```
DATA/
├── reliance/XBRL/
│   ├── 16Jan2025_1940_INDAS_117292.xml
│   └── 17Oct2024_1944_INDAS_112850.xml
└── tcs/XBRL/
    ├── 09Jan2025_2136_INDAS_117180.xml
    └── 10Oct2024_1858_INDAS_112732.xml
```

### Step 3: Convert XBRL to Excel

```bash
python converter.py
```

**What it does:**
- Uploads XBRL files to EC2 converter service
- Downloads converted Excel files
- Saves to `DATA/{symbol}/XLSX/`

**Requirements:**
- Internet connection to EC2 converter
- EC2 service must be running

**Output:**
```
DATA/
├── reliance/XLSX/
│   ├── 16Jan2025_1940_INDAS_117292.xlsx
│   └── 17Oct2024_1944_INDAS_112850.xlsx
└── tcs/XLSX/
    ├── 09Jan2025_2136_INDAS_117180.xlsx
    └── 10Oct2024_1858_INDAS_112732.xlsx
```

### Step 4: Extract Financial Data

```bash
python extractor.py
```

**What it does:**
- Extracts `PaidUpValueOfEquityShareCapital` and `FaceValueOfEquityShareCapital`
- Calculates `NumberOfShares` (PaidUp ÷ FaceValue)
- Sorts by date (newest first)
- Removes duplicates by filing date
- Saves to `DATA/{symbol}/CSV/`

**Output:**
```
DATA/
├── reliance/CSV/
│   └── reliance_extracted_data.csv
└── tcs/CSV/
    └── tcs_extracted_data.csv
```

**CSV Format:**
```csv
FilingDate,PaidUpValueOfEquityShareCapital,FaceValueOfEquityShareCapital,NumberOfShares
16Jan2025,6339000000,10,633900000
17Oct2024,6339000000,10,633900000
```

## File Structure

```
corporate-filingsNSE/
├── fetcher.py          # Step 1: Fetch NSE data
├── downloader.py       # Step 2: Download XBRL files
├── converter.py        # Step 3: Convert XBRL to Excel
├── extractor.py        # Step 4: Extract financial data
├── symbols.txt         # Input: Stock symbols list
├── JSON/              # Raw NSE API responses
├── DATA/              # Processed data by symbol
│   └── {symbol}/
│       ├── XBRL/      # Downloaded XBRL files
│       ├── XLSX/      # Converted Excel files
│       └── CSV/       # Extracted financial data
└── README.md
```

## Edge Cases & Troubleshooting

### Common Issues

1. **No XBRL links found**
   ```
   [SKIP] No valid XBRL links found for SYMBOL
   ```
   - **Cause:** Symbol has no recent filings with XBRL data
   - **Solution:** Check if symbol is actively traded

2. **EC2 converter timeout**
   ```
   [FAIL] Upload failed for file.xml: timeout
   ```
   - **Cause:** EC2 service overloaded or down
   - **Solution:** Retry after delay, check EC2 status

3. **Excel file not found in converter response**
   ```
   [INFO] Response content type: text/html
   ```
   - **Cause:** XBRL file format not supported by converter
   - **Solution:** Skip file, check XBRL validity

4. **Financial fields not found in Excel**
   ```
   [SKIP] Required fields not found in file.xlsx
   ```
   - **Cause:** Excel structure differs from expected format
   - **Solution:** Check Excel file manually, update field names

### --region Edge Cases Discovered During Development

5. **Field Name Variations Across Sectors**
   ```
   [FAIL] No data found in file.xlsx
   ```
   - **Cause:** Different sectors use different field naming conventions
   - **Banking Sector:** Uses `ProfitLossForThePeriod` and `BasicEarningsPerShareAfterExtraordinaryItems`
   - **Non-Banking Sector:** Uses `ProfitLossForPeriod` and `BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations`
   - **Solution:** Extractor now uses OR conditions to handle multiple field name variations

6. **XBRL Data Structure Format**
   ```
   Expected: Standard Excel format
   Actual: XBRL Instance Data format with columns: Sr.No. | Element Name | Period | Unit | Decimals | Fact Value
   ```
   - **Cause:** XBRL converted files use standardized instance data format
   - **Field Names:** Located in Column B (Element Name)
   - **Values:** Located in Column F (Fact Value)
   - **Solution:** Updated extractor to parse XBRL instance data format correctly

7. **Multiple EPS Field Variations**
   ```
   Banking: BasicEarningsPerShareAfterExtraordinaryItems
   Non-Banking: BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations
   Alternative: BasicEarningsPerShareBeforeExtraordinaryItems
   Continuing Ops: BasicEarningsLossPerShareFromContinuingOperations
   ```
   - **Cause:** Different accounting standards and reporting requirements
   - **Solution:** Extractor checks multiple EPS field patterns using OR conditions

8. **Consolidated vs Standalone Statements**
   ```
   Consolidated: ProfitOrLossAttributableToOwnersOfParent
   Standalone: ProfitLossForPeriod / ProfitLossForThePeriod
   ```
   - **Cause:** Companies report both consolidated and standalone financials
   - **Solution:** Extractor handles both statement types automatically

9. **Unicode and Encoding Issues**
   ```
   UnicodeEncodeError: 'charmap' codec can't encode character
   ```
   - **Cause:** Windows command prompt encoding limitations
   - **Solution:** Removed Unicode characters from output messages

10. **Excel Temporary Files**
    ```
    [ERROR] Permission denied: ~$filename.xlsx
    ```
    - **Cause:** Excel creates temporary files starting with ~$
    - **Solution:** Extractor skips files starting with ~$ automatically

### --end of region

### Data Quality

- **XBRL Availability:** Only filings from 2018+ typically have XBRL links
- **Field Names:** Financial field names may vary across companies
- **Date Formats:** Filing dates are automatically parsed and sorted
- **Duplicates:** Same-day filings are deduplicated automatically

### Performance Tips

1. **Batch Processing:** Process symbols in smaller batches for better monitoring
2. **Resume Capability:** All scripts skip existing files, allowing safe restarts
3. **Rate Limiting:** Built-in delays prevent server overload
4. **Memory Usage:** Large symbol lists may require more RAM

## Configuration

### Symbols File Format
```
# symbols.txt - one symbol per line
RELIANCE
TCS
INFY
HDFCBANK
```

### API Endpoints
- **NSE API:** `https://www.nseindia.com/api/corporates-financial-results`
- **EC2 Converter:** `http://ec2-3-221-41-38.compute-1.amazonaws.com/`

## Requirements

- Python 3.7+
- `requests` library
- `openpyxl` library  
- Internet connection
- Windows/Linux/macOS

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Credits

Developed by dvygo at Vayuman Capital (2025).