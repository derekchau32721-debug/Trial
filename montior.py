import yfinance as yf
import pandas as pd
from datetime import datetime

# Define sector ETFs (SPDR sector ETFs)
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

# Define country indices (no emojis)
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

# Export to Excel
with pd.ExcelWriter("Market_Performance.xlsx") as writer:
    sector_table.to_excel(writer, sheet_name="Sector Performance", index=False)
    country_table.to_excel(writer, sheet_name="Country Performance", index=False)

# HTML with sortable tables and color coding
def df_to_sortable_table(df, title, table_id):
    table_html = f"<h2>{title}</h2><table id='{table_id}' class='sortable'><thead><tr>"
    for col in df.columns:
        table_html += f"<th>{col}</th>"
    table_html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        table_html += "<tr>"
        for col in df.columns:
            val = row[col]
            if "%" in col:  # color coding for % changes
                color = "green" if val > 0 else "red" if val < 0 else "black"
                table_html += f"<td style='color:{color}'>{val}</td>"
            else:
                table_html += f"<td>{val}</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"
    return table_html

html_output = f"""
<html>
<head>
<title>Market Performance Dashboard</title>
<style>
body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 20px;
    color: #fff;
    background: linear-gradient(-45deg, #1e3c72, #2a5298, #3a6073, #16222a);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}}
@keyframes gradientBG {{
    0% {{background-position: 0% 50%;}}
    50% {{background-position: 100% 50%;}}
    100% {{background-position: 0% 50%;}}
}}
h1 {{
    text-align: center;
    margin-bottom: 30px;
}}
.tabs {{
    display: flex;
    justify-content: center;
    cursor: pointer;
    margin-bottom: 20px;
}}
.tab {{
    padding: 10px 20px;
    background: rgba(255,255,255,0.2);
    margin-right: 10px;
    border-radius: 5px;
    transition: background 0.3s;
}}
.tab:hover {{
    background: rgba(255,255,255,0.4);
}}
.content {{
    display: none;
}}
.active {{
    display: block;
}}
table {{
    border-collapse: collapse;
    width: 95%;
    margin: 20px auto;
    background: #fff;
    color: #333;
    border-radius: 8px;
    overflow: hidden;
}}
th, td {{
    padding: 10px;
    text-align: center;
    border-bottom: 1px solid #ddd;
}}
th {{
    background: #2a5298;
    color: #fff;
    cursor: pointer;
}}
tr:hover {{
    background-color: #f0f8ff;
}}
</style>
<script>
// Universal table sort function
function sortTable(tableId, colIndex) {{
    var table = document.getElementById(tableId);
    var rows = Array.from(table.tBodies[0].rows);
    var asc = table.getAttribute("data-sort-dir") !== "asc";
    rows.sort((a, b) => {{
        var valA = parseFloat(a.cells[colIndex].innerText) || a.cells[colIndex].innerText;
        var valB = parseFloat(b.cells[colIndex].innerText) || b.cells[colIndex].innerText;
        return asc ? (valA > valB ? 1 : -1) : (valA < valB ? 1 : -1);
    }});
    rows.forEach(r => table.tBodies[0].appendChild(r));
    table.setAttribute("data-sort-dir", asc ? "asc" : "desc");
}}
document.addEventListener("DOMContentLoaded", () => {{
    document.querySelectorAll("table.sortable").forEach(table => {{
        table.querySelectorAll("th").forEach((th, i) => {{
            th.addEventListener("click", () => sortTable(table.id, i));
        }});
    }});
}});
function showTab(tabId) {{
    document.getElementById('sector').style.display = 'none';
    document.getElementById('country').style.display = 'none';
    document.getElementById(tabId).style.display = 'block';
}}
</script>
</head>
<body>
<h1>Market Performance Dashboard</h1>
<div class="tabs">
  <div class="tab" onclick="showTab('sector')">Sector Performance</div>
  <div class="tab" onclick="showTab('country')">Country Performance</div>
</div>
<div id="sector" class="content active">
{df_to_sortable_table(sector_table, "Sector Performance", "sectorTable")}
</div>
<div id="country" class="content">
{df_to_sortable_table(country_table, "Country Performance", "countryTable")}
</div>
</body>
</html>
"""

with open("Market_Performance.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("Excel and HTML files with sortable tables, color coding, and animated background created successfully.")
