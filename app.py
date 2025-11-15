import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

# 💾 Cache NSE tickers


@st.cache_data
def load_nse_tickers():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    df = pd.read_csv(url)
    tickers = df['SYMBOL'].dropna().unique().tolist()
    return [symbol + ".NS" for symbol in tickers]



# Custom CSS Styling

st.markdown("""
    <style>
        /* Main panel */
        .main {
            background-color: #f0f0f0;
            color: #003366;
        }
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #003366;
            color: white;
        }
        section[data-testid="stSidebar"] * {
            color: white;
        }
        /* Header */
        h1, h2, h3 {
            color: #003366;
        }
    </style>
""", unsafe_allow_html=True)


# Sidebar Info

st.sidebar.title("📊 Sharpe Ratio App")


st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ How it Works")
st.sidebar.markdown("""
- Select a NSE listed stock from the dropdown.
- The app compares its Sharpe Ratio of selected stock with Sharpe ratio of NIFTY 500.The Nifty 500 represents the top 500 companies based on full market capitalisation and average daily turnover from the eligible universe.
(Represents 91.76% free float marketcap)
- Sharpe Ratio = Return ÷ Volatility (annualized).
""")

st.sidebar.markdown(
    "Creator: Vishwas Kulkarni (vishwaskulkarni@zohomail.in)")
st.sidebar.markdown(f"📅 Date: {datetime.today().strftime('%d %b %Y')}")

st.sidebar.markdown("**📈 Visitor Count:**")
if "visits" not in st.session_state:
    st.session_state.visits = 1
else:
    st.session_state.visits += 1
st.sidebar.markdown(f"🔢 {st.session_state.visits}")




# Main Panel Header

st.title("📈 Sharpe Ratio Comparison")
st.markdown("""Economist William F. Sharpe proposed the Sharpe ratio in 1966 after his work on the capital asset pricing model (CAPM),
The Sharpe ratio compares a fund's historical or projected returns relative to an investment benchmark with the historical or expected variability of such returns.
Excess returns are those above an industry benchmark or the risk-free rate of return.
Here we are comparing Sharpe ratio of stock with Nifty 500 index as Benchmark.
""")

# Load Stock List from CSV

# 📋 Load tickers and set defaults
tickers = load_nse_tickers()
default_stocks = [s for s in ['RELIANCE.NS'] if s in tickers]



# User Input

stock_symbol = st.selectbox(
    "🔍 Select a stock :", options=tickers, index=tickers.index("RELIANCE.NS") if "RELIANCE.NS" in tickers else 0
)

benchmark_symbol = "^CRSLDX"


# Data Download



@st.cache_data(show_spinner=False)
def get_data(symbols, start_date):
    data = yf.download(symbols, start=start_date,
                       progress=False, auto_adjust=False)
    return data


try:
    hist = yf.Ticker(stock_symbol).history(period="max")
    if hist.empty:
        st.error("No historical data found for the selected stock.")
        st.stop()

    start_date = hist.index[0].strftime("%Y-%m-%d")
    data = get_data([stock_symbol, benchmark_symbol], start_date)

    if isinstance(data.columns, pd.MultiIndex):
        close_df = data["Close"].copy()
        close_df.columns = ["Close_stock", "Close_nifty"]
    else:
        st.error("Unexpected data format from yfinance.")
        st.stop()

    close_df["ret_stock"] = close_df["Close_stock"].pct_change(
        fill_method=None)
    close_df["ret_nifty"] = close_df["Close_nifty"].pct_change(
        fill_method=None)
    close_df = close_df.dropna()

    def sharpe_ratio(series):
        std = series.std()
        return np.sqrt(252) * (series.mean() / std) if std != 0 else np.nan

    latest_price = close_df["Close_stock"].iloc[-1]
    st.markdown(f"  Latest Price of {stock_symbol}:   ₹{latest_price:.2f}")

    sharpe_stock = sharpe_ratio(close_df["ret_stock"])
    sharpe_nifty = sharpe_ratio(close_df["ret_nifty"])

    
    # Results
   
    st.subheader("📊 Results")
    st.markdown(f"Sharpe Ratio ({stock_symbol}):  `{sharpe_stock:.4f}`")
    st.markdown(f"Sharpe Ratio (NIFTY 500):   `{sharpe_nifty:.4f}`")

    if np.isnan(sharpe_stock) or np.isnan(sharpe_nifty):
        st.warning("Insufficient data to compute Sharpe Ratios.")
    elif sharpe_stock > sharpe_nifty:
        st.success("✅ The stock outperforms NIFTY 500 on a risk-adjusted basis.")
    elif sharpe_stock < sharpe_nifty:
        st.error("⚠️ The stock underperforms NIFTY 500 on a risk-adjusted basis.")
    else:
        st.info("ℹ️ The stock matches NIFTY 500 in risk-adjusted performance.")

except Exception as e:
    st.error(f"Error: {e}")

# Disclaimer

st.markdown("---")
st.caption(" Disclaimer: This tool is for educational purposes only and does not constitute financial advice.")


