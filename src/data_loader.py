# Downloads and stores ASX data
"""
data_loader.py

Downloads live ASX company data from Yahoo Finance
for use in the ASX AI Investor project.

Factors collected:

- Price
- PE Ratio
- Return on Equity (ROE)
- Revenue Growth
- Debt To Equity
- Market Capitalisation
- 6-Month Momentum
- 12-Month Momentum

Author: Lee + Copilot
"""

import pandas as pd
import yfinance as yf


# --------------------------------------------------
# ASX WATCHLIST
# --------------------------------------------------

ASX_TICKERS = [
    "BHP.AX",
    "CBA.AX",
    "CSL.AX",
    "WBC.AX",
    "NAB.AX",
    "ANZ.AX",
    "WES.AX",
    "WOW.AX",
    "MQG.AX",
    "XRO.AX",
    "AQN.AX",
    "PPY.AX"
]


# --------------------------------------------------
# SAFE VALUE HANDLER
# --------------------------------------------------

def safe_number(value, default=None):
    """
    Prevents errors when data is missing,
    None, NaN or non-numeric.
    """

    try:

        if value is None:
            return default

        if pd.isna(value):
            return default

        return float(value)

    except Exception:

        return default


# --------------------------------------------------
# MOMENTUM CALCULATION
# --------------------------------------------------

def calculate_momentum(history):

    momentum_6m = None
    momentum_12m = None

    try:

        if len(history) >= 126:

            current_price = history["Close"].iloc[-1]
            price_6m = history["Close"].iloc[-126]

            momentum_6m = (
                (current_price - price_6m)
                / price_6m
            ) * 100

        if len(history) >= 252:

            current_price = history["Close"].iloc[-1]
            price_12m = history["Close"].iloc[0]

            momentum_12m = (
                (current_price - price_12m)
                / price_12m
            ) * 100

    except Exception:

        pass

    return momentum_6m, momentum_12m


# --------------------------------------------------
# LOAD SINGLE STOCK
# --------------------------------------------------

def load_stock_data(ticker_symbol):

    print(f"Loading {ticker_symbol}...")

    try:

        ticker = yf.Ticker(ticker_symbol)

        info = ticker.info

        history = ticker.history(
            period="1y"
        )

        company_name = info.get(
            "shortName",
            ticker_symbol
        )

        pe_ratio = safe_number(
            info.get("trailingPE")
        )

        roe = safe_number(
            info.get("returnOnEquity")
        )

        if roe is not None:
            roe *= 100

        revenue_growth = safe_number(
            info.get("revenueGrowth")
        )

        if revenue_growth is not None:
            revenue_growth *= 100

        debt_to_equity = safe_number(
            info.get("debtToEquity")
        )

        market_cap = safe_number(
            info.get("marketCap")
        )

        current_price = None

        if not history.empty:

            current_price = float(
                history["Close"].iloc[-1]
            )

        momentum_6m, momentum_12m = (
            calculate_momentum(history)
        )

        return {

            "Ticker": ticker_symbol,

            "Company": company_name,

            "Price": (
                round(current_price, 2)
                if current_price is not None
                else None
            ),

            "PE": (
                round(pe_ratio, 2)
                if pe_ratio is not None
                else None
            ),

            "ROE": (
                round(roe, 2)
                if roe is not None
                else None
            ),

            "RevenueGrowth": (
                round(revenue_growth, 2)
                if revenue_growth is not None
                else None
            ),

            "DebtToEquity": (
                round(debt_to_equity, 2)
                if debt_to_equity is not None
                else None
            ),

            "MarketCap": market_cap,

            "Momentum6M": (
                round(momentum_6m, 2)
                if momentum_6m is not None
                else None
            ),

            "Momentum12M": (
                round(momentum_12m, 2)
                if momentum_12m is not None
                else None
            )

        }

    except Exception as e:

        print(
            f"Error loading {ticker_symbol}: {e}"
        )

        return None


# --------------------------------------------------
# LOAD ENTIRE UNIVERSE
# --------------------------------------------------

def load_data():

    results = []

    print("\n")
    print("=" * 50)
    print("ASX AI INVESTOR")
    print("Loading market data...")
    print("=" * 50)

    for ticker in ASX_TICKERS:

        stock_data = load_stock_data(
            ticker
        )

        if stock_data is not None:

            results.append(
                stock_data
            )

    df = pd.DataFrame(
        results
    )

    print("\n")
    print(
        f"Loaded {len(df)} stocks"
    )

    return df


# --------------------------------------------------
# TEST RUN
# --------------------------------------------------

if __name__ == "__main__":

    data = load_data()

    pd.set_option(
        "display.max_columns",
        None
    )

    print("\n")
    print(data)