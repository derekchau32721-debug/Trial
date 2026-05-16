import yfinance as yf
import pandas as pd
from datetime import datetime

# Define sector ETFs
sector_etfs = {
    "Technology": "XLK",
    "Financials": "XLF",
    "Healthcare": "XLV",
    "Energy": "XLE",
    "Consumer Discretionary": "XLY",
    "Consumer Staples": "XLP",
    "Industrials": "XLI",
    "Materials": "XLB",
    "Utilities": "XLU",
    "Real Estate": "XLRE",
    "Communication Services": "XLC"
}

# Define country indices
country_indices = {
    "US (S&P 500)": "^GSPC",
    "Hong Kong (HSI)": "^HSI",
    "Japan (Nikkei 225)": "^N225",
    "UK (FTSE 100)": "^FTSE",
    "France (CAC 40)": "^FCHI",
    "Germany (DAX)": "^GDAXI",
    "China (Shanghai Composite)": "000001.SS",
    "India (Nifty 50)": "^NSEI",
    "South Korea (KOSPI)": "^KS11",
    "Taiwan (TWSE)": "^TWII",
    "Australia (ASX 200)": "^AXJO"
}

def get_performance(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="6mo")
    latest_price = hist['Close'].iloc[-1]
    daily_change = (hist['Close'].iloc[-1] / hist['Close'].iloc[-2] - 1) * 100
    weekly_change = (hist['Close'].iloc[-1] / hist['Close'].iloc[-6] - 1) * 100
    monthly_change = (hist['Close'].iloc[-1] / hist['Close'].iloc[-21] - 1) * 100
    return latest_price, daily_change, weekly_change, monthly_change

def build_table(etf_dict):
    rows = []
    for name, ticker in etf_dict.items():
        try:
            latest, d, w, m = get_performance(ticker)
            rows.append({
                "Name": name,
                "Ticker": ticker,
                "Latest Price": round(latest, 2),
                "Daily %": round(d, 2),
                "Weekly %": round(w, 2),
                "Monthly %": round(m, 2),
                "Refresh Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
    return pd.DataFrame(rows)

# Build tables
sector_table = build_table(sector_etfs)
country_table = build_table(country_indices)

# Export to Excel only
with pd.ExcelWriter("Market_Performance.xlsx") as writer:
    sector_table.to_excel(writer, sheet_name="Sector Performance", index=False)
    country_table.to_excel(writer, sheet_name="Country Performance", index=False)

print("✅ Excel file 'Market_Performance.xlsx' created successfully with sector and country performance data.")
