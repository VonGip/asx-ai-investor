from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

rankings = pd.read_csv(
    BASE_DIR / "output" / "latest_rankings.csv"
)

portfolio = pd.read_csv(
    BASE_DIR / "output" / "latest_portfolio.csv"
)

import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="ASX AI Investor",
    layout="wide"
)

st.title(
    "ASX AI Investor"
)

st.subheader(
    "Latest Rankings"
)

rankings = pd.read_csv(
    "output/latest_rankings.csv"
)

st.dataframe(
    rankings,
    use_container_width=True
)

st.subheader(
    "Top Stock Scores"
)

st.bar_chart(
    rankings.set_index(
        "Ticker"
    )["FactorScore"]
)

st.subheader(
    "Top Portfolio"
)

portfolio = pd.read_csv(
    "output/latest_portfolio.csv"
)

st.dataframe(
    portfolio,
    use_container_width=True
)