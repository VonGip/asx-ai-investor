"""
backtester_v2.py

ASX AI Investor

Walk-Forward Momentum Backtest
Annual Rebalancing
vs ASX200 Benchmark

Version 2

Author: Lee + Copilot
"""

import pandas as pd
import numpy as np
import yfinance as yf
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

START_YEAR = 2016

END_YEAR = 2026

TOP_N = 5

INITIAL_CAPITAL = 100000


# --------------------------------------------------
# UNIVERSE
# --------------------------------------------------

TICKERS = [

    "BHP.AX",
    "CBA.AX",
    "CSL.AX",
    "WBC.AX",
    "NAB.AX",
    "ANZ.AX",
    "WES.AX",
    "WOW.AX",
    "MQG.AX",
    "XRO.AX"

]


# --------------------------------------------------
# DOWNLOAD DATA
# --------------------------------------------------

def download_prices():

    print("\nDownloading price history...")

    data = yf.download(
        TICKERS,
        start=f"{START_YEAR - 1}-01-01",
        auto_adjust=True,
        progress=False
    )

    return data["Close"]


# --------------------------------------------------
# GET YEAR RETURN
# --------------------------------------------------

def get_year_return(series, year):

    try:

        year_data = series.loc[
            str(year)
        ]

        if len(year_data) < 2:
            return None

        start_price = year_data.iloc[0]
        end_price = year_data.iloc[-1]

        return (
            end_price / start_price
        ) - 1

    except Exception:

        return None


# --------------------------------------------------
# RANK STOCKS USING PRIOR YEAR MOMENTUM
# --------------------------------------------------

def rank_stocks(prices, year):

    rankings = []

    lookback_year = year - 1

    for ticker in TICKERS:

        try:

            yearly_return = get_year_return(
                prices[ticker],
                lookback_year
            )

            if yearly_return is not None:

                rankings.append(
                    (
                        ticker,
                        yearly_return
                    )
                )

        except Exception:

            continue

    rankings.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return rankings[:TOP_N]


# --------------------------------------------------
# RUN STRATEGY
# --------------------------------------------------

def run_strategy(prices):

    annual_results = []

    equity_curve = []

    portfolio_value = INITIAL_CAPITAL

    for year in range(
        START_YEAR + 1,
        END_YEAR + 1
    ):

        selected = rank_stocks(
            prices,
            year
        )

        tickers = [
            item[0]
            for item in selected
        ]

        print(
            f"{year} -> {tickers}"
        )

        returns = []

        for ticker in tickers:

            annual_return = get_year_return(
                prices[ticker],
                year
            )

            if annual_return is not None:

                returns.append(
                    annual_return
                )

        if len(returns) == 0:
            continue

        portfolio_return = np.mean(
            returns
        )

        portfolio_value *= (
            1 + portfolio_return
        )

        equity_curve.append(
            portfolio_value
        )

        annual_results.append({

            "Year": year,

            "PortfolioReturnPct":
            round(
                portfolio_return * 100,
                2
            ),

            "PortfolioValue":
            round(
                portfolio_value,
                2
            )

        })

    return (
        pd.DataFrame(
            annual_results
        ),
        pd.Series(
            equity_curve
        )
    )


# --------------------------------------------------
# BENCHMARK
# --------------------------------------------------

def get_benchmark():

    benchmark = yf.download(
        "^AXJO",
        start=f"{START_YEAR - 1}-01-01",
        auto_adjust=True,
        progress=False
    )

    close = benchmark["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    benchmark_value = INITIAL_CAPITAL

    benchmark_curve = []

    benchmark_returns = []

    for year in range(
        START_YEAR + 1,
        END_YEAR + 1
    ):

        try:

            year_prices = close.loc[
                str(year)
            ]

            start_price = (
                year_prices.iloc[0]
            )

            end_price = (
                year_prices.iloc[-1]
            )

            annual_return = float(
                (end_price / start_price) - 1
            )

            benchmark_returns.append(
                annual_return
            )

            benchmark_value *= (
                1 + annual_return
            )

            benchmark_curve.append(
                benchmark_value
            )

        except Exception:

            continue

    return (
        pd.Series(
            benchmark_returns
        ),
        pd.Series(
            benchmark_curve
        )
    )


# --------------------------------------------------
# METRICS
# --------------------------------------------------

def calculate_metrics(
    annual_returns
):

    returns = pd.Series(
        annual_returns,
        dtype=float
    ).dropna()

    cumulative = (
        1 + returns
    ).cumprod()

    years = len(returns)

    total_return = (
        cumulative.iloc[-1]
    )

    cagr = (
        total_return
        ** (1 / years)
    ) - 1

    volatility = (
        returns.std()
    )

    sharpe = (

        cagr / volatility

        if volatility > 0

        else 0

    )

    drawdown = (

        cumulative
        /
        cumulative.cummax()

    ) - 1

    max_drawdown = (
        drawdown.min()
    )

    return {

        "CAGR":
        round(
            cagr * 100,
            2
        ),

        "Volatility":
        round(
            volatility * 100,
            2
        ),

        "Sharpe":
        round(
            sharpe,
            2
        ),

        "MaxDrawdown":
        round(
            max_drawdown * 100,
            2
        )

    }


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("\n")
    print("=" * 80)
    print("ASX AI INVESTOR")
    print("WALK-FORWARD BACKTEST")
    print("=" * 80)

    prices = download_prices()

    annual_results, strategy_curve = (
        run_strategy(
            prices
        )
    )

    strategy_returns = (
        annual_results[
            "PortfolioReturnPct"
        ] / 100
    )

    benchmark_returns, benchmark_curve = (
        get_benchmark()
    )

    strategy_metrics = (
        calculate_metrics(
            strategy_returns
        )
    )

    benchmark_metrics = (
        calculate_metrics(
            benchmark_returns
        )
    )

    print("\n")
    print("=" * 80)
    print("ANNUAL RETURNS")
    print("=" * 80)

    print(
        annual_results
    )

    print("\n")
    print("=" * 80)
    print("STRATEGY METRICS")
    print("=" * 80)

    for key, value in strategy_metrics.items():

        print(
            f"{key}: {value}"
        )

    print("\n")
    print("=" * 80)
    print("ASX200 METRICS")
    print("=" * 80)

    for key, value in benchmark_metrics.items():

        print(
            f"{key}: {value}"
        )

    output_dir = Path(
        "output"
    )

    output_dir.mkdir(
        exist_ok=True
    )

    annual_results.to_csv(

        output_dir /
        "walkforward_results.csv",

        index=False

    )

    pd.DataFrame({

        "Strategy":
        strategy_curve,

        "Benchmark":
        benchmark_curve

    }).to_csv(

        output_dir /
        "equity_curve.csv",

        index=False

    )

    print("\n")
    print("Files Saved:")

    print(
        "output/walkforward_results.csv"
    )

    print(
        "output/equity_curve.csv"
    )


if __name__ == "__main__":

    main()