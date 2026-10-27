import yfinance as yf
import pandas as pd


def benchmark_return():

    benchmark = "^AXJO"

    data = yf.download(
        benchmark,
        period="10y",
        progress=False
    )

    returns = (
        data["Close"]
        .pct_change()
        .dropna()
    )

    cumulative = (
        1 + returns
    ).cumprod()

    return cumulative