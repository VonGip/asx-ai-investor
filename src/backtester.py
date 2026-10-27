"""
backtester.py

ASX AI Investor
Portfolio vs ASX200 Benchmark

Author: Lee + Copilot
"""

import yfinance as yf
import pandas as pd
import numpy as np


# --------------------------------------------------
# DOWNLOAD PRICES
# --------------------------------------------------

def get_prices(
    tickers,
    start="2016-01-01"
):

    data = yf.download(
        tickers,
        start=start,
        auto_adjust=True,
        progress=False
    )

    return data["Close"]


# --------------------------------------------------
# PORTFOLIO RETURNS
# --------------------------------------------------

def portfolio_returns(prices):

    returns = (
        prices
        .pct_change()
        .dropna()
    )

    portfolio = (
        returns.mean(axis=1)
    )

    return portfolio


# --------------------------------------------------
# CAGR
# --------------------------------------------------

def calculate_cagr(cumulative):

    years = len(cumulative) / 252

    return (
        cumulative.iloc[-1]
        ** (1 / years)
        - 1
    )


# --------------------------------------------------
# MAX DRAWDOWN
# --------------------------------------------------

def max_drawdown(cumulative):

    rolling_max = cumulative.cummax()

    drawdown = (
        cumulative
        /
        rolling_max
        - 1
    )

    return drawdown.min()


# --------------------------------------------------
# METRICS
# --------------------------------------------------

def calculate_metrics(
    returns
):

    cumulative = (
        1 + returns
    ).cumprod()

    cagr = calculate_cagr(
        cumulative
    )

    volatility = (
        returns.std()
        * np.sqrt(252)
    )

    sharpe = (
        cagr / volatility
    )

    mdd = max_drawdown(
        cumulative
    )

    return {

        "CAGR": round(
            cagr * 100,
            2
        ),

        "Volatility": round(
            volatility * 100,
            2
        ),

        "Sharpe": round(
            sharpe,
            2
        ),

        "MaxDrawdown": round(
            mdd * 100,
            2
        )

    }


# --------------------------------------------------
# BENCHMARK
# --------------------------------------------------

def benchmark_returns():

    benchmark = yf.download(
        "^AXJO",
        start="2016-01-01",
        auto_adjust=True,
        progress=False
    )

    prices = benchmark["Close"]

    returns = (
        prices
        .pct_change()
        .dropna()
    )

    return returns


# --------------------------------------------------
# RUN TEST
# --------------------------------------------------

def run_backtest():

    tickers = [

        "BHP.AX",
        "WOW.AX",
        "MQG.AX",
        "ANZ.AX",
        "WES.AX"

    ]

    print("\n")
    print("=" * 80)
    print("BACKTEST")
    print("=" * 80)

    prices = get_prices(
        tickers
    )

    strategy_returns = (
        portfolio_returns(
            prices
        )
    )

    benchmark = (
        benchmark_returns()
    )

    strategy_metrics = (
        calculate_metrics(
            strategy_returns
        )
    )

    benchmark_metrics = (
        calculate_metrics(
            benchmark.squeeze()
        )
    )

    print("\n")
    print("AI PORTFOLIO")

    for k, v in strategy_metrics.items():

        print(
            f"{k}: {v}"
        )

    print("\n")
    print("ASX200")

    for k, v in benchmark_metrics.items():

        print(
            f"{k}: {v}"
        )


if __name__ == "__main__":

    run_backtest()