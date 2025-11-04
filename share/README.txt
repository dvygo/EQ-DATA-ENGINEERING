NSE Corporate Filings - Extracted Financial Data (Latest Version)
================================================================

This folder contains successfully extracted financial data from NSE corporate filings.
**LATEST VERSION** - Now uses DateOfEndOfReportingPeriod extracted directly from XBRL data.

EXTRACTION SUMMARY:
- Total Symbols Processed: 70 (Successfully extracted)
- Success Rate: 100% for available data
- Data Fields: DateOfEndOfReportingPeriod, ProfitLossForThePeriod, BasicEarningsPerShareAfterExtraordinaryItems, NumberOfSharesOutstanding

KEY IMPROVEMENT:
- **DateOfEndOfReportingPeriod**: Extracted directly from XBRL financial statements (most accurate)
- **Previous Version**: Used filing date from filename (less accurate for analysis)
- **Example**: 31Dec2024 (actual period end) vs 16Jan2025 (filing date)

FILES INCLUDED (72 CSV files):
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
26. grasim.csv - Grasim Industries Limited
27. hcltech.csv - HCL Technologies Limited
28. hdfcbank.csv - HDFC Bank Limited
29. heromotoco.csv - Hero MotoCorp Limited
30. hindalco.csv - Hindalco Industries Limited
31. hindpetro.csv - Hindustan Petroleum Corporation Limited
32. hindunilvr.csv - Hindustan Unilever Limited
33. icicibank.csv - ICICI Bank Limited
34. idea.csv - Vodafone Idea Limited
35. indigo.csv - InterGlobe Aviation Limited (IndiGo)
36. indusindbk.csv - IndusInd Bank Limited
37. infy.csv - Infosys Limited
38. ioc.csv - Indian Oil Corporation Limited
39. itc.csv - ITC Limited
40. jiofin.csv - Jio Financial Services Limited
41. jswsteel.csv - JSW Steel Limited
42. kotakbank.csv - Kotak Mahindra Bank Limited
43. lt.csv - Larsen & Toubro Limited
44. ltim.csv - LTIMindtree Limited
45. lupin.csv - Lupin Limited
46. m&m.csv - Mahindra & Mahindra Limited
47. maruti.csv - Maruti Suzuki India Limited
48. maxhealth.csv - Max Healthcare Institute Limited
49. nestleind.csv - Nestle India Limited
50. ntpc.csv - NTPC Limited
51. ongc.csv - Oil and Natural Gas Corporation Limited
52. powergrid.csv - Power Grid Corporation of India Limited
53. reliance.csv - Reliance Industries Limited (Latest Format)
54. reliance_extracted_data.csv - Reliance Industries Limited (Legacy Format)
55. sbin.csv - State Bank of India
56. shreecem.csv - Shree Cement Limited
57. shriramfin.csv - Shriram Finance Limited
58. sunpharma.csv - Sun Pharmaceutical Industries Limited
59. tataconsum.csv - Tata Consumer Products Limited
60. tatapower.csv - Tata Power Company Limited
61. tatasteel.csv - Tata Steel Limited
62. tcs.csv - Tata Consultancy Services Limited
63. techm.csv - Tech Mahindra Limited
64. titan.csv - Titan Company Limited
65. tmpv.csv - TMV Holdings Limited
66. trent.csv - Trent Limited
67. ultracemco.csv - UltraTech Cement Limited
68. upl.csv - UPL Limited
69. vedl.csv - Vedanta Limited
70. wipro.csv - Wipro Limited
71. yesbank.csv - Yes Bank Limited
72. zeel.csv - Zee Entertainment Enterprises Limited

DATA FORMAT:
Each CSV file contains:
- DateOfEndOfReportingPeriod: Actual period end date from XBRL data (DDMmmYYYY format)
- ProfitLossForThePeriod: Net profit/loss in INR
- BasicEarningsPerShareAfterExtraordinaryItems: Earnings per share in INR
- NumberOfSharesOutstanding: Calculated shares outstanding (ProfitLoss ÷ EPS)

SAMPLE DATA:
DateOfEndOfReportingPeriod,ProfitLossForThePeriod,BasicEarningsPerShareAfterExtraordinaryItems,NumberOfSharesOutstanding
31Dec2024,10890700000.0,58.0,187770689
30Sep2024,2338700000.0,12.46,187696629
30Jun2024,3662300000.0,19.5,187810256

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
- Previous: Filing dates (when documents were submitted to exchange)
- Current: Reporting period end dates (actual financial period covered by statements)
- Critical for accurate financial analysis and time-series studies

FAILED SYMBOLS (No Data Available):
The following 3 symbols from the original list of 73 failed to fetch data:
- HDFCLIFE - HDFC Life Insurance Company Limited
- SBILIFE - SBI Life Insurance Company Limited  
- TATAMOTORS - Tata Motors Limited
(These symbols return empty data arrays from NSE API)

Generated on: November 4, 2025 (Final Version)
Pipeline: NSE Corporate Filings Data Pipeline v2.1
Repository: github.com/dvygo/EQ-DATA-ENGINEERING
Success Rate: 70/73 symbols (95.9%)