NSE Corporate Filings - Extracted Financial Data (Updated)
=========================================================

This folder contains successfully extracted financial data from NSE corporate filings.
**UPDATED VERSION** - Now uses DateOfEndOfReportingPeriod instead of filing dates.

EXTRACTION SUMMARY:
- Total Symbols Processed: 28 (Updated from previous 21)
- Success Rate: 100%
- Data Fields: DateOfEndOfReportingPeriod, ProfitLossForThePeriod, BasicEarningsPerShareAfterExtraordinaryItems, NumberOfSharesOutstanding

KEY IMPROVEMENT:
- **DateOfEndOfReportingPeriod**: Now extracted directly from XBRL financial data (more accurate)
- **Previous Version**: Used filing date from filename (less accurate)
- **Example**: 31Dec2024 (actual period end) vs 16Jan2025 (filing date)

FILES INCLUDED (29 CSV files):
1. acc.csv - ACC Limited (Cement)
2. adanient.csv - Adani Enterprises Limited
3. adaniports.csv - Adani Ports and Special Economic Zone Limited
4. ambujacem.csv - Ambuja Cements Limited
5. apollohosp.csv - Apollo Hospitals Enterprise Limited
6. asianpaint.csv - Asian Paints Limited
7. auropharma.csv - Aurobindo Pharma Limited
8. axisbank.csv - Axis Bank Limited
9. bajaj-auto.csv - Bajaj Auto Limited
10. bajajfinsv.csv - Bajaj Finserv Limited
11. bajfinance.csv - Bajaj Finance Limited
12. bankbaroda.csv - Bank of Baroda
13. bel.csv - Bharat Electronics Limited
14. bhartiartl.csv - Bharti Airtel Limited
15. bhel.csv - Bharat Heavy Electricals Limited
16. boschltd.csv - Bosch Limited
17. bpcl.csv - Bharat Petroleum Corporation Limited
18. britannia.csv - Britannia Industries Limited
19. cipla.csv - Cipla Limited
20. coalindia.csv - Coal India Limited
21. divislab.csv - Divi's Laboratories Limited
22. drreddy.csv - Dr. Reddy's Laboratories Limited
23. eichermot.csv - Eicher Motors Limited
24. eternal.csv - Eternal Chemicals Limited
25. gail.csv - GAIL (India) Limited
26. infy.csv - Infosys Limited
27. reliance.csv - Reliance Industries Limited (Updated Format)
28. reliance_extracted_data.csv - Reliance Industries Limited (Legacy Format)
29. tcs.csv - Tata Consultancy Services Limited

DATA FORMAT:
Each CSV file contains:
- DateOfEndOfReportingPeriod: Actual period end date from XBRL data (DDMmmYYYY format)
- ProfitLossForThePeriod: Net profit/loss in INR
- BasicEarningsPerShareAfterExtraordinaryItems: Earnings per share in INR
- NumberOfSharesOutstanding: Calculated shares outstanding (ProfitLoss ÷ EPS)

SAMPLE DATA:
DateOfEndOfReportingPeriod,ProfitLossForThePeriod,BasicEarningsPerShareAfterExtraordinaryItems,NumberOfSharesOutstanding
31Dec2024,218040000000.0,13.7,15915328467
30Sep2024,77130000000.0,11.4,6765789473
30Jun2024,174480000000.0,22.37,7799731783

DATA COVERAGE:
- Time Period: 2018-2025 (varies by company)
- Frequency: Quarterly and Annual filings
- Currency: Indian Rupees (INR)
- Source: NSE XBRL filings converted to Excel format

TECHNICAL NOTES:
- Data extracted using OR conditions to handle sector-specific field variations
- Banking vs Non-Banking field naming conventions handled automatically
- Consolidated and Standalone statement formats supported
- Duplicate reporting period dates removed (latest filing kept)
- Data sorted in reverse chronological order (newest first)
- DateOfEndOfReportingPeriod extracted directly from XBRL instance data

ACCURACY IMPROVEMENT:
- Previous: Filing dates (when documents were submitted)
- Current: Reporting period end dates (actual financial period covered)
- More accurate for financial analysis and time-series data

Generated on: November 4, 2025 (Updated Version)
Pipeline: NSE Corporate Filings Data Pipeline v2.0
Repository: github.com/dvygo/EQ-DATA-ENGINEERING
