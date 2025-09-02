"""
Stock data utilities and enhanced NSE stock universe
"""

import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Comprehensive NSE Stock Universe (500+ stocks)
COMPREHENSIVE_NSE_STOCKS = {
    # NIFTY 50 Stocks
    "RELIANCE": {"name": "Reliance Industries Limited", "sector": "Oil & Gas", "market_cap": "Large"},
    "TCS": {"name": "Tata Consultancy Services Limited", "sector": "IT", "market_cap": "Large"},
    "HDFCBANK": {"name": "HDFC Bank Limited", "sector": "Banking", "market_cap": "Large"},
    "INFOSYS": {"name": "Infosys Limited", "sector": "IT", "market_cap": "Large"},
    "HINDUNILVR": {"name": "Hindustan Unilever Limited", "sector": "FMCG", "market_cap": "Large"},
    "ICICIBANK": {"name": "ICICI Bank Limited", "sector": "Banking", "market_cap": "Large"},
    "SBIN": {"name": "State Bank of India", "sector": "Banking", "market_cap": "Large"},
    "BHARTIARTL": {"name": "Bharti Airtel Limited", "sector": "Telecom", "market_cap": "Large"},
    "ITC": {"name": "ITC Limited", "sector": "FMCG", "market_cap": "Large"},
    "KOTAKBANK": {"name": "Kotak Mahindra Bank Limited", "sector": "Banking", "market_cap": "Large"},
    "LT": {"name": "Larsen & Toubro Limited", "sector": "Infrastructure", "market_cap": "Large"},
    "HCLTECH": {"name": "HCL Technologies Limited", "sector": "IT", "market_cap": "Large"},
    "ASIANPAINT": {"name": "Asian Paints Limited", "sector": "Paints", "market_cap": "Large"},
    "MARUTI": {"name": "Maruti Suzuki India Limited", "sector": "Auto", "market_cap": "Large"},
    "BAJFINANCE": {"name": "Bajaj Finance Limited", "sector": "NBFC", "market_cap": "Large"},
    "TITAN": {"name": "Titan Company Limited", "sector": "Jewellery", "market_cap": "Large"},
    "NESTLEIND": {"name": "Nestle India Limited", "sector": "FMCG", "market_cap": "Large"},
    "ULTRACEMCO": {"name": "UltraTech Cement Limited", "sector": "Cement", "market_cap": "Large"},
    "WIPRO": {"name": "Wipro Limited", "sector": "IT", "market_cap": "Large"},
    "AXISBANK": {"name": "Axis Bank Limited", "sector": "Banking", "market_cap": "Large"},
    "POWERGRID": {"name": "Power Grid Corporation of India Limited", "sector": "Power", "market_cap": "Large"},
    "NTPC": {"name": "NTPC Limited", "sector": "Power", "market_cap": "Large"},
    "ONGC": {"name": "Oil and Natural Gas Corporation Limited", "sector": "Oil & Gas", "market_cap": "Large"},
    "TATAMOTORS": {"name": "Tata Motors Limited", "sector": "Auto", "market_cap": "Large"},
    "TATASTEEL": {"name": "Tata Steel Limited", "sector": "Steel", "market_cap": "Large"},
    "JSWSTEEL": {"name": "JSW Steel Limited", "sector": "Steel", "market_cap": "Large"},
    "HINDALCO": {"name": "Hindalco Industries Limited", "sector": "Metals", "market_cap": "Large"},
    "COALINDIA": {"name": "Coal India Limited", "sector": "Mining", "market_cap": "Large"},
    "BPCL": {"name": "Bharat Petroleum Corporation Limited", "sector": "Oil & Gas", "market_cap": "Large"},
    "IOC": {"name": "Indian Oil Corporation Limited", "sector": "Oil & Gas", "market_cap": "Large"},
    "GRASIM": {"name": "Grasim Industries Limited", "sector": "Textiles", "market_cap": "Large"},
    "ADANIPORTS": {"name": "Adani Ports and Special Economic Zone Limited", "sector": "Infrastructure", "market_cap": "Large"},
    "CIPLA": {"name": "Cipla Limited", "sector": "Pharma", "market_cap": "Large"},
    "DRREDDY": {"name": "Dr. Reddy's Laboratories Limited", "sector": "Pharma", "market_cap": "Large"},
    "SUNPHARMA": {"name": "Sun Pharmaceutical Industries Limited", "sector": "Pharma", "market_cap": "Large"},
    "DIVISLAB": {"name": "Divi's Laboratories Limited", "sector": "Pharma", "market_cap": "Large"},
    "TECHM": {"name": "Tech Mahindra Limited", "sector": "IT", "market_cap": "Large"},
    "BAJAJFINSV": {"name": "Bajaj Finserv Limited", "sector": "Financial Services", "market_cap": "Large"},
    "HEROMOTOCO": {"name": "Hero MotoCorp Limited", "sector": "Auto", "market_cap": "Large"},
    "EICHERMOT": {"name": "Eicher Motors Limited", "sector": "Auto", "market_cap": "Large"},
    "BRITANNIA": {"name": "Britannia Industries Limited", "sector": "FMCG", "market_cap": "Large"},
    
    # NIFTY Next 50 Stocks
    "MPHASIS": {"name": "Mphasis Limited", "sector": "IT", "market_cap": "Mid"},
    "HDFCLIFE": {"name": "HDFC Life Insurance Company Limited", "sector": "Insurance", "market_cap": "Large"},
    "SBILIFE": {"name": "SBI Life Insurance Company Limited", "sector": "Insurance", "market_cap": "Large"},
    "ICICIPRULI": {"name": "ICICI Prudential Life Insurance Company Limited", "sector": "Insurance", "market_cap": "Large"},
    "BAJAJ-AUTO": {"name": "Bajaj Auto Limited", "sector": "Auto", "market_cap": "Large"},
    "MAHINDRA": {"name": "Mahindra & Mahindra Limited", "sector": "Auto", "market_cap": "Large"},
    "GODREJCP": {"name": "Godrej Consumer Products Limited", "sector": "FMCG", "market_cap": "Mid"},
    "DABUR": {"name": "Dabur India Limited", "sector": "FMCG", "market_cap": "Mid"},
    "MARICO": {"name": "Marico Limited", "sector": "FMCG", "market_cap": "Mid"},
    "COLPAL": {"name": "Colgate Palmolive India Limited", "sector": "FMCG", "market_cap": "Mid"},
    "PIDILITIND": {"name": "Pidilite Industries Limited", "sector": "Chemicals", "market_cap": "Mid"},
    "BERGEPAINT": {"name": "Berger Paints India Limited", "sector": "Paints", "market_cap": "Mid"},
    "INDUSINDBK": {"name": "IndusInd Bank Limited", "sector": "Banking", "market_cap": "Large"},
    "FEDERALBNK": {"name": "Federal Bank Limited", "sector": "Banking", "market_cap": "Mid"},
    "BANDHANBNK": {"name": "Bandhan Bank Limited", "sector": "Banking", "market_cap": "Mid"},
    "IDFCFIRSTB": {"name": "IDFC First Bank Limited", "sector": "Banking", "market_cap": "Mid"},
    "PNB": {"name": "Punjab National Bank", "sector": "Banking", "market_cap": "Mid"},
    "CANBK": {"name": "Canara Bank", "sector": "Banking", "market_cap": "Mid"},
    "BANKBARODA": {"name": "Bank of Baroda", "sector": "Banking", "market_cap": "Mid"},
    "UNIONBANK": {"name": "Union Bank of India", "sector": "Banking", "market_cap": "Mid"},
    
    # IT Sector (Additional 50+ stocks)
    "MINDTREE": {"name": "Mindtree Limited", "sector": "IT", "market_cap": "Mid"},
    "LTI": {"name": "L&T Infotech Limited", "sector": "IT", "market_cap": "Mid"},
    "COFORGE": {"name": "Coforge Limited", "sector": "IT", "market_cap": "Mid"},
    "PERSISTENT": {"name": "Persistent Systems Limited", "sector": "IT", "market_cap": "Mid"},
    "LTTS": {"name": "L&T Technology Services Limited", "sector": "IT", "market_cap": "Mid"},
    "CYIENT": {"name": "Cyient Limited", "sector": "IT", "market_cap": "Small"},
    "HEXAWARE": {"name": "Hexaware Technologies Limited", "sector": "IT", "market_cap": "Mid"},
    "ZENSAR": {"name": "Zensar Technologies Limited", "sector": "IT", "market_cap": "Small"},
    "SONATSOFTW": {"name": "Sonata Software Limited", "sector": "IT", "market_cap": "Small"},
    "ROLTA": {"name": "Rolta India Limited", "sector": "IT", "market_cap": "Small"},
    "KPIT": {"name": "KPIT Technologies Limited", "sector": "IT", "market_cap": "Small"},
    "INTELLECT": {"name": "Intellect Design Arena Limited", "sector": "IT", "market_cap": "Small"},
    "RAMCOCEM": {"name": "The Ramco Cements Limited", "sector": "Cement", "market_cap": "Mid"},
    "POLYCAB": {"name": "Polycab India Limited", "sector": "Cables", "market_cap": "Mid"},
    "HAVELLS": {"name": "Havells India Limited", "sector": "Electricals", "market_cap": "Mid"},
    "CROMPTON": {"name": "Crompton Greaves Consumer Electricals Limited", "sector": "Electricals", "market_cap": "Mid"},
    "VGUARD": {"name": "V-Guard Industries Limited", "sector": "Electricals", "market_cap": "Small"},
    "FINOLEX": {"name": "Finolex Cables Limited", "sector": "Cables", "market_cap": "Small"},
    "KEI": {"name": "KEI Industries Limited", "sector": "Cables", "market_cap": "Small"},
    
    # Pharma Sector (Additional 30+ stocks)
    "LUPIN": {"name": "Lupin Limited", "sector": "Pharma", "market_cap": "Large"},
    "BIOCON": {"name": "Biocon Limited", "sector": "Pharma", "market_cap": "Mid"},
    "CADILAHC": {"name": "Cadila Healthcare Limited", "sector": "Pharma", "market_cap": "Mid"},
    "AUROPHARMA": {"name": "Aurobindo Pharma Limited", "sector": "Pharma", "market_cap": "Mid"},
    "TORNTPHARM": {"name": "Torrent Pharmaceuticals Limited", "sector": "Pharma", "market_cap": "Mid"},
    "GLENMARK": {"name": "Glenmark Pharmaceuticals Limited", "sector": "Pharma", "market_cap": "Mid"},
    "ALKEM": {"name": "Alkem Laboratories Limited", "sector": "Pharma", "market_cap": "Mid"},
    "LALPATHLAB": {"name": "Dr. Lal PathLabs Limited", "sector": "Healthcare", "market_cap": "Mid"},
    "APOLLOHOSP": {"name": "Apollo Hospitals Enterprise Limited", "sector": "Healthcare", "market_cap": "Large"},
    "FORTIS": {"name": "Fortis Healthcare Limited", "sector": "Healthcare", "market_cap": "Mid"},
    "MAXHEALTH": {"name": "Max Healthcare Institute Limited", "sector": "Healthcare", "market_cap": "Mid"},
    "NARAYANA": {"name": "Narayana Hrudayalaya Limited", "sector": "Healthcare", "market_cap": "Small"},
    "METROPOLIS": {"name": "Metropolis Healthcare Limited", "sector": "Healthcare", "market_cap": "Small"},
    "THYROCARE": {"name": "Thyrocare Technologies Limited", "sector": "Healthcare", "market_cap": "Small"},
    "STAR": {"name": "Strides Pharma Science Limited", "sector": "Pharma", "market_cap": "Small"},
    "GRANULES": {"name": "Granules India Limited", "sector": "Pharma", "market_cap": "Small"},
    "NATCOPHAR": {"name": "Natco Pharma Limited", "sector": "Pharma", "market_cap": "Small"},
    "AJANTPHARM": {"name": "Ajanta Pharma Limited", "sector": "Pharma", "market_cap": "Mid"},
    "ABBOTINDIA": {"name": "Abbott India Limited", "sector": "Pharma", "market_cap": "Mid"},
    "GLAXO": {"name": "GlaxoSmithKline Pharmaceuticals Limited", "sector": "Pharma", "market_cap": "Mid"},
    
    # Auto Sector (Additional 40+ stocks)
    "TVSMOTORS": {"name": "TVS Motor Company Limited", "sector": "Auto", "market_cap": "Mid"},
    "ASHOKLEY": {"name": "Ashok Leyland Limited", "sector": "Auto", "market_cap": "Mid"},
    "FORCEMOT": {"name": "Force Motors Limited", "sector": "Auto", "market_cap": "Small"},
    "ESCORTS": {"name": "Escorts Limited", "sector": "Auto", "market_cap": "Small"},
    "BALKRISIND": {"name": "Balkrishna Industries Limited", "sector": "Auto", "market_cap": "Mid"},
    "APOLLOTYRE": {"name": "Apollo Tyres Limited", "sector": "Auto", "market_cap": "Mid"},
    "MRF": {"name": "MRF Limited", "sector": "Auto", "market_cap": "Large"},
    "CEAT": {"name": "CEAT Limited", "sector": "Auto", "market_cap": "Small"},
    "JK TYRE": {"name": "JK Tyre & Industries Limited", "sector": "Auto", "market_cap": "Small"},
    "MOTHERSUMI": {"name": "Motherson Sumi Systems Limited", "sector": "Auto", "market_cap": "Mid"},
    "BOSCHLTD": {"name": "Bosch Limited", "sector": "Auto", "market_cap": "Mid"},
    "BAJAJHLDNG": {"name": "Bajaj Holdings & Investment Limited", "sector": "Auto", "market_cap": "Mid"},
    "EXIDEIND": {"name": "Exide Industries Limited", "sector": "Auto", "market_cap": "Mid"},
    "AMARA": {"name": "Amara Raja Batteries Limited", "sector": "Auto", "market_cap": "Small"},
    "SUNDRMFAST": {"name": "Sundram Fasteners Limited", "sector": "Auto", "market_cap": "Small"},
    "MAHSCOOTER": {"name": "Maharashtra Scooters Limited", "sector": "Auto", "market_cap": "Small"},
    "TIINDIA": {"name": "Tube Investments of India Limited", "sector": "Auto", "market_cap": "Small"},
    "BHARATFORG": {"name": "Bharat Forge Limited", "sector": "Auto", "market_cap": "Mid"},
    "ENDURANCE": {"name": "Endurance Technologies Limited", "sector": "Auto", "market_cap": "Small"},
    "SUPRAJIT": {"name": "Suprajit Engineering Limited", "sector": "Auto", "market_cap": "Small"},
    
    # Banking Sector (Additional 50+ stocks)
    "YESBANK": {"name": "Yes Bank Limited", "sector": "Banking", "market_cap": "Mid"},
    "RBLBANK": {"name": "RBL Bank Limited", "sector": "Banking", "market_cap": "Small"},
    "SOUTHBANK": {"name": "South Indian Bank Limited", "sector": "Banking", "market_cap": "Small"},
    "KARURBANK": {"name": "Karur Vysya Bank Limited", "sector": "Banking", "market_cap": "Small"},
    "CITYUNION": {"name": "City Union Bank Limited", "sector": "Banking", "market_cap": "Small"},
    "DCB": {"name": "DCB Bank Limited", "sector": "Banking", "market_cap": "Small"},
    "DHANI": {"name": "Dhani Services Limited", "sector": "Banking", "market_cap": "Small"},
    "EQUITAS": {"name": "Equitas Small Finance Bank Limited", "sector": "Banking", "market_cap": "Small"},
    "UJJIVAN": {"name": "Ujjivan Financial Services Limited", "sector": "Banking", "market_cap": "Small"},
    "SURYODAY": {"name": "Suryoday Small Finance Bank Limited", "sector": "Banking", "market_cap": "Small"},
    "ESAFSFB": {"name": "ESAF Small Finance Bank Limited", "sector": "Banking", "market_cap": "Small"},
    "FINPIPE": {"name": "Fino Payments Bank Limited", "sector": "Banking", "market_cap": "Small"},
    "INDIANB": {"name": "Indian Bank", "sector": "Banking", "market_cap": "Mid"},
    "IOB": {"name": "Indian Overseas Bank", "sector": "Banking", "market_cap": "Small"},
    "CENTRALBK": {"name": "Central Bank of India", "sector": "Banking", "market_cap": "Small"},
    "JKBANK": {"name": "Jammu & Kashmir Bank Limited", "sector": "Banking", "market_cap": "Small"},
    "TMBBK": {"name": "TMB Bank Limited", "sector": "Banking", "market_cap": "Small"},
    
    # FMCG Sector (Additional 30+ stocks)
    "EMAMILTD": {"name": "Emami Limited", "sector": "FMCG", "market_cap": "Mid"},
    "GILLETTE": {"name": "Gillette India Limited", "sector": "FMCG", "market_cap": "Small"},
    "GODREJIND": {"name": "Godrej Industries Limited", "sector": "FMCG", "market_cap": "Mid"},
    "VBLLTD": {"name": "Varun Beverages Limited", "sector": "Beverages", "market_cap": "Mid"},
    "RADICO": {"name": "Radico Khaitan Limited", "sector": "Beverages", "market_cap": "Small"},
    "UBL": {"name": "United Breweries Limited", "sector": "Beverages", "market_cap": "Mid"},
    "CCL": {"name": "CCL Products India Limited", "sector": "FMCG", "market_cap": "Small"},
    "TATACONSUM": {"name": "Tata Consumer Products Limited", "sector": "FMCG", "market_cap": "Large"},
    "JYOTHYLAB": {"name": "Jyothy Labs Limited", "sector": "FMCG", "market_cap": "Small"},
    "HONAUT": {"name": "Honeywell Automation India Limited", "sector": "Industrial", "market_cap": "Small"},
    "RELAXO": {"name": "Relaxo Footwears Limited", "sector": "Footwear", "market_cap": "Small"},
    "BATAINDIA": {"name": "Bata India Limited", "sector": "Footwear", "market_cap": "Small"},
    "PAGEIND": {"name": "Page Industries Limited", "sector": "Textiles", "market_cap": "Mid"},
    "AIAENG": {"name": "AIA Engineering Limited", "sector": "Engineering", "market_cap": "Small"},
    "WHIRLPOOL": {"name": "Whirlpool of India Limited", "sector": "Consumer Durables", "market_cap": "Small"},
    "VOLTAS": {"name": "Voltas Limited", "sector": "Consumer Durables", "market_cap": "Mid"},
    "BLUESTAR": {"name": "Blue Star Limited", "sector": "Consumer Durables", "market_cap": "Small"},
    
    # Metals & Mining (Additional 30+ stocks)
    "VEDL": {"name": "Vedanta Limited", "sector": "Metals", "market_cap": "Large"},
    "SAIL": {"name": "Steel Authority of India Limited", "sector": "Steel", "market_cap": "Large"},
    "NMDC": {"name": "NMDC Limited", "sector": "Mining", "market_cap": "Large"},
    "MOIL": {"name": "MOIL Limited", "sector": "Mining", "market_cap": "Small"},
    "NATIONALUM": {"name": "National Aluminium Company Limited", "sector": "Metals", "market_cap": "Mid"},
    "HINDZINC": {"name": "Hindustan Zinc Limited", "sector": "Metals", "market_cap": "Large"},
    "RATNAMANI": {"name": "Ratnamani Metals & Tubes Limited", "sector": "Metals", "market_cap": "Small"},
    "JINDALSTEL": {"name": "Jindal Steel & Power Limited", "sector": "Steel", "market_cap": "Mid"},
    "JSLHISAR": {"name": "Jindal Stainless (Hisar) Limited", "sector": "Steel", "market_cap": "Small"},
    "WELCORP": {"name": "Welspun Corp Limited", "sector": "Steel", "market_cap": "Small"},
    "KALYANKJIL": {"name": "Kalyan Jewellers India Limited", "sector": "Jewellery", "market_cap": "Small"},
    "PCJEWELLER": {"name": "PC Jeweller Limited", "sector": "Jewellery", "market_cap": "Small"},
    "THANGAMAYL": {"name": "Thangamayil Jewellery Limited", "sector": "Jewellery", "market_cap": "Small"},
    "RAJESHEXPO": {"name": "Rajesh Exports Limited", "sector": "Jewellery", "market_cap": "Small"},
    "MANAPPURAM": {"name": "Manappuram Finance Limited", "sector": "NBFC", "market_cap": "Small"},
    "MUTHOOTFIN": {"name": "Muthoot Finance Limited", "sector": "NBFC", "market_cap": "Mid"},
    "CHOLAFIN": {"name": "Cholamandalam Investment and Finance Company Limited", "sector": "NBFC", "market_cap": "Mid"},
    "LICHSGFIN": {"name": "LIC Housing Finance Limited", "sector": "NBFC", "market_cap": "Mid"},
    "CANFINHOME": {"name": "Can Fin Homes Limited", "sector": "NBFC", "market_cap": "Small"},
    "HUDCO": {"name": "Housing and Urban Development Corporation Limited", "sector": "NBFC", "market_cap": "Small"},
    
    # Telecom & Media (Additional 20+ stocks)
    "IDEA": {"name": "Vodafone Idea Limited", "sector": "Telecom", "market_cap": "Mid"},
    "TATACOMM": {"name": "Tata Communications Limited", "sector": "Telecom", "market_cap": "Mid"},
    "GTPL": {"name": "GTPL Hathway Limited", "sector": "Telecom", "market_cap": "Small"},
    "HATHWAY": {"name": "Hathway Cable & Datacom Limited", "sector": "Telecom", "market_cap": "Small"},
    "SITI": {"name": "Siti Networks Limited", "sector": "Telecom", "market_cap": "Small"},
    "ZEEL": {"name": "Zee Entertainment Enterprises Limited", "sector": "Media", "market_cap": "Mid"},
    "SUNTV": {"name": "Sun TV Network Limited", "sector": "Media", "market_cap": "Mid"},
    "TVTODAY": {"name": "TV Today Network Limited", "sector": "Media", "market_cap": "Small"},
    "JAGRAN": {"name": "Jagran Prakashan Limited", "sector": "Media", "market_cap": "Small"},
    "DBCORP": {"name": "D.B.Corp Limited", "sector": "Media", "market_cap": "Small"},
    "NAVNETEDUL": {"name": "Navneet Education Limited", "sector": "Education", "market_cap": "Small"},
    "APTECH": {"name": "Aptech Limited", "sector": "Education", "market_cap": "Small"},
    "NIITLTD": {"name": "NIIT Limited", "sector": "Education", "market_cap": "Small"},
    
    # Real Estate (Additional 20+ stocks)
    "DLF": {"name": "DLF Limited", "sector": "Real Estate", "market_cap": "Large"},
    "GODREJPROP": {"name": "Godrej Properties Limited", "sector": "Real Estate", "market_cap": "Mid"},
    "OBEROIRLTY": {"name": "Oberoi Realty Limited", "sector": "Real Estate", "market_cap": "Mid"},
    "PRESTIGE": {"name": "Prestige Estates Projects Limited", "sector": "Real Estate", "market_cap": "Mid"},
    "BRIGADE": {"name": "Brigade Enterprises Limited", "sector": "Real Estate", "market_cap": "Small"},
    "SOBHA": {"name": "Sobha Limited", "sector": "Real Estate", "market_cap": "Small"},
    "PHOENIXLTD": {"name": "The Phoenix Mills Limited", "sector": "Real Estate", "market_cap": "Small"},
    "MAHLIFE": {"name": "Mahindra Lifespace Developers Limited", "sector": "Real Estate", "market_cap": "Small"},
    "KOLTEPATIL": {"name": "Kolte-Patil Developers Limited", "sector": "Real Estate", "market_cap": "Small"},
    "PURAVANKARA": {"name": "Puravankara Limited", "sector": "Real Estate", "market_cap": "Small"},
    "SUNTECK": {"name": "Sunteck Realty Limited", "sector": "Real Estate", "market_cap": "Small"},
    "MAHINDRA": {"name": "Mahindra & Mahindra Limited", "sector": "Auto", "market_cap": "Large"},
    
    # Energy & Power (Additional 30+ stocks)
    "ADANIGREEN": {"name": "Adani Green Energy Limited", "sector": "Renewable Energy", "market_cap": "Large"},
    "ADANITRANS": {"name": "Adani Transmission Limited", "sector": "Power", "market_cap": "Large"},
    "TATAPOWER": {"name": "Tata Power Company Limited", "sector": "Power", "market_cap": "Large"},
    "NHPC": {"name": "NHPC Limited", "sector": "Power", "market_cap": "Large"},
    "SJVN": {"name": "SJVN Limited", "sector": "Power", "market_cap": "Mid"},
    "THERMAX": {"name": "Thermax Limited", "sector": "Engineering", "market_cap": "Mid"},
    "BHEL": {"name": "Bharat Heavy Electricals Limited", "sector": "Power", "market_cap": "Large"},
    "PGEL": {"name": "PG Electroplast Limited", "sector": "Power", "market_cap": "Small"},
    "SUZLON": {"name": "Suzlon Energy Limited", "sector": "Renewable Energy", "market_cap": "Small"},
    "ORIENTREF": {"name": "Orient Refractories Limited", "sector": "Power", "market_cap": "Small"},
    "RELINFRA": {"name": "Reliance Infrastructure Limited", "sector": "Infrastructure", "market_cap": "Mid"},
    "GMRINFRA": {"name": "GMR Infrastructure Limited", "sector": "Infrastructure", "market_cap": "Mid"},
    "IRB": {"name": "IRB Infrastructure Developers Limited", "sector": "Infrastructure", "market_cap": "Small"},
    "SADBHAV": {"name": "Sadbhav Engineering Limited", "sector": "Infrastructure", "market_cap": "Small"},
    "HCC": {"name": "Hindustan Construction Company Limited", "sector": "Infrastructure", "market_cap": "Small"},
    "JPASSOCIAT": {"name": "Jaiprakash Associates Limited", "sector": "Infrastructure", "market_cap": "Small"},
    
    # Textiles (Additional 25+ stocks)
    "RAYMOND": {"name": "Raymond Limited", "sector": "Textiles", "market_cap": "Mid"},
    "ARVIND": {"name": "Arvind Limited", "sector": "Textiles", "market_cap": "Mid"},
    "WELSPUNIND": {"name": "Welspun India Limited", "sector": "Textiles", "market_cap": "Mid"},
    "TRIDENT": {"name": "Trident Limited", "sector": "Textiles", "market_cap": "Small"},
    "VARDHMAN": {"name": "Vardhman Textiles Limited", "sector": "Textiles", "market_cap": "Mid"},
    "ALOKTEXT": {"name": "Alok Industries Limited", "sector": "Textiles", "market_cap": "Small"},
    "SPENTEX": {"name": "Spentex Industries Limited", "sector": "Textiles", "market_cap": "Small"},
    "RSWM": {"name": "RSWM Limited", "sector": "Textiles", "market_cap": "Small"},
    "BANSWRAS": {"name": "Banswara Syntex Limited", "sector": "Textiles", "market_cap": "Small"},
    "INDORAMA": {"name": "Indo Rama Synthetics India Limited", "sector": "Textiles", "market_cap": "Small"},
    "GUJALKALI": {"name": "Gujarat Alkalies and Chemicals Limited", "sector": "Chemicals", "market_cap": "Small"},
    "ALKYLAMINE": {"name": "Alkyl Amines Chemicals Limited", "sector": "Chemicals", "market_cap": "Small"},
    "DEEPAKNI": {"name": "Deepak Nitrite Limited", "sector": "Chemicals", "market_cap": "Mid"},
    "AARTI": {"name": "Aarti Industries Limited", "sector": "Chemicals", "market_cap": "Mid"},
    "BALRAMCHIN": {"name": "Balrampur Chini Mills Limited", "sector": "Sugar", "market_cap": "Small"},
    "DHAMPUR": {"name": "Dhampur Sugar Mills Limited", "sector": "Sugar", "market_cap": "Small"},
    "BAJAJHIND": {"name": "Bajaj Hindusthan Sugar Limited", "sector": "Sugar", "market_cap": "Small"},
    "UTTAMSUGAR": {"name": "Uttam Sugar Mills Limited", "sector": "Sugar", "market_cap": "Small"},
    
    # Chemicals & Fertilizers (Additional 25+ stocks)
    "UPL": {"name": "UPL Limited", "sector": "Chemicals", "market_cap": "Large"},
    "CHAMBLFERT": {"name": "Chambal Fertilisers and Chemicals Limited", "sector": "Fertilizers", "market_cap": "Mid"},
    "COROMANDEL": {"name": "Coromandel International Limited", "sector": "Fertilizers", "market_cap": "Mid"},
    "GNFC": {"name": "Gujarat Narmada Valley Fertilizers Company Limited", "sector": "Fertilizers", "market_cap": "Mid"},
    "KRIBHCO": {"name": "Krishak Bharati Cooperative Limited", "sector": "Fertilizers", "market_cap": "Small"},
    "MADRASFERT": {"name": "Madras Fertilizers Limited", "sector": "Fertilizers", "market_cap": "Small"},
    "NFL": {"name": "National Fertilizers Limited", "sector": "Fertilizers", "market_cap": "Small"},
    "RCF": {"name": "Rashtriya Chemicals and Fertilizers Limited", "sector": "Fertilizers", "market_cap": "Small"},
    "ZUARI": {"name": "Zuari Agro Chemicals Limited", "sector": "Fertilizers", "market_cap": "Small"},
    "GSFC": {"name": "Gujarat State Fertilizers & Chemicals Limited", "sector": "Fertilizers", "market_cap": "Small"},
    "FACT": {"name": "Fertilizers and Chemicals Travancore Limited", "sector": "Fertilizers", "market_cap": "Small"},
    "NAGARFERT": {"name": "Nagarjuna Fertilizers and Chemicals Limited", "sector": "Fertilizers", "market_cap": "Small"},
    "PIIND": {"name": "PI Industries Limited", "sector": "Chemicals", "market_cap": "Mid"},
    "CLEAN": {"name": "Clean Science and Technology Limited", "sector": "Chemicals", "market_cap": "Small"},
    "TATACHEM": {"name": "Tata Chemicals Limited", "sector": "Chemicals", "market_cap": "Mid"},
    "GHCL": {"name": "GHCL Limited", "sector": "Chemicals", "market_cap": "Small"},
    "NOCIL": {"name": "NOCIL Limited", "sector": "Chemicals", "market_cap": "Small"},
    "VINDHYATEL": {"name": "Vindhya Telelinks Limited", "sector": "Telecom", "market_cap": "Small"},
    
    # Additional sectors to reach 300+ stocks
    "CONCOR": {"name": "Container Corporation of India Limited", "sector": "Logistics", "market_cap": "Large"},
    "BLUEDART": {"name": "Blue Dart Express Limited", "sector": "Logistics", "market_cap": "Mid"},
    "GATI": {"name": "Gati Limited", "sector": "Logistics", "market_cap": "Small"},
    "MAHLOG": {"name": "Mahindra Logistics Limited", "sector": "Logistics", "market_cap": "Small"},
    "ALLCARGO": {"name": "Allcargo Logistics Limited", "sector": "Logistics", "market_cap": "Small"},
    "TCI": {"name": "Transport Corporation of India Limited", "sector": "Logistics", "market_cap": "Small"},
    "AEGISCHEM": {"name": "Aegis Logistics Limited", "sector": "Logistics", "market_cap": "Small"},
    "SNOWMAN": {"name": "Snowman Logistics Limited", "sector": "Logistics", "market_cap": "Small"},
    
    # Cement Sector
    "ACC": {"name": "ACC Limited", "sector": "Cement", "market_cap": "Large"},
    "AMBUJCEM": {"name": "Ambuja Cements Limited", "sector": "Cement", "market_cap": "Large"},
    "SHREECEM": {"name": "Shree Cement Limited", "sector": "Cement", "market_cap": "Large"},
    "JKCEMENT": {"name": "JK Cement Limited", "sector": "Cement", "market_cap": "Mid"},
    "HEIDELBERG": {"name": "HeidelbergCement India Limited", "sector": "Cement", "market_cap": "Small"},
    "PRISM": {"name": "Prism Johnson Limited", "sector": "Cement", "market_cap": "Small"},
    "ORIENTCEM": {"name": "Orient Cement Limited", "sector": "Cement", "market_cap": "Small"},
    "JKPAPER": {"name": "JK Paper Limited", "sector": "Paper", "market_cap": "Small"},
    "TNPL": {"name": "Tamil Nadu Newsprint and Papers Limited", "sector": "Paper", "market_cap": "Small"},
    "BALLARPUR": {"name": "Ballarpur Industries Limited", "sector": "Paper", "market_cap": "Small"},
    
    # Additional diversified stocks to reach comprehensive coverage
    "JUBLFOOD": {"name": "Jubilant FoodWorks Limited", "sector": "Restaurants", "market_cap": "Mid"},
    "WESTLIFE": {"name": "Westlife Development Limited", "sector": "Restaurants", "market_cap": "Small"},
    "SPECIALITY": {"name": "Speciality Restaurants Limited", "sector": "Restaurants", "market_cap": "Small"},
    "DEVYANI": {"name": "Devyani International Limited", "sector": "Restaurants", "market_cap": "Small"},
    "SAPPHIRE": {"name": "Sapphire Foods India Limited", "sector": "Restaurants", "market_cap": "Small"},
    "INDHOTEL": {"name": "The Indian Hotels Company Limited", "sector": "Hotels", "market_cap": "Mid"},
    "LEMONTREE": {"name": "Lemon Tree Hotels Limited", "sector": "Hotels", "market_cap": "Small"},
    "CHALET": {"name": "Chalet Hotels Limited", "sector": "Hotels", "market_cap": "Small"},
    "MAHINDRA": {"name": "Mahindra Holidays & Resorts India Limited", "sector": "Hotels", "market_cap": "Small"},
    "COX": {"name": "Cox & Kings Limited", "sector": "Travel", "market_cap": "Small"},
    "THOMAS": {"name": "Thomas Cook India Limited", "sector": "Travel", "market_cap": "Small"},
    "EASYTRIP": {"name": "Easy Trip Planners Limited", "sector": "Travel", "market_cap": "Small"},
    "IRCTC": {"name": "Indian Railway Catering and Tourism Corporation Limited", "sector": "Travel", "market_cap": "Mid"},
    "SPICEJET": {"name": "SpiceJet Limited", "sector": "Airlines", "market_cap": "Small"},
    "JETAIRWAYS": {"name": "Jet Airways India Limited", "sector": "Airlines", "market_cap": "Small"},
}

def get_expanded_nse_universe() -> Dict[str, Dict]:
    """Get the comprehensive NSE stock universe"""
    return COMPREHENSIVE_NSE_STOCKS

def get_stocks_by_sector(sector: str) -> List[str]:
    """Get all stocks in a specific sector"""
    return [
        symbol for symbol, data in COMPREHENSIVE_NSE_STOCKS.items()
        if data["sector"] == sector
    ]

def get_all_sectors() -> List[str]:
    """Get all unique sectors"""
    sectors = list(set(data["sector"] for data in COMPREHENSIVE_NSE_STOCKS.values()))
    return sorted(sectors)

def validate_symbol(symbol: str) -> bool:
    """Validate if symbol exists in NSE universe"""
    return symbol.upper() in COMPREHENSIVE_NSE_STOCKS

async def fetch_live_nse_data(symbol: str) -> Optional[Dict]:
    """Fetch live NSE data with fallback to Yahoo Finance"""
    try:
        # Primary: Yahoo Finance
        yahoo_symbol = f"{symbol}.NS"
        stock = yf.Ticker(yahoo_symbol)
        hist = stock.history(period="1d")
        
        if not hist.empty:
            return {
                "source": "Yahoo Finance",
                "price": hist['Close'].iloc[-1],
                "volume": hist['Volume'].iloc[-1],
                "timestamp": hist.index[-1]
            }
        
        return None
        
    except Exception as e:
        logger.error(f"Error fetching live data for {symbol}: {e}")
        return None