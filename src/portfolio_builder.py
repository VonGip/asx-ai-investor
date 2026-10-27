# Creates a portfolio from the ranked companies
"""
portfolio_builder.py

Builds investable portfolios from the ranked
ASX AI Investor stock list.

MVP Version:
- Selects top ranked stocks
- Equal weight allocation
- Calculates dollar allocations
- Calculates share quantities

Author: Lee + Copilot
"""

import pandas as pd


# --------------------------------------------------
# BUILD PORTFOLIO
# --------------------------------------------------

def build_portfolio(
    ranked_df,
    portfolio_size=5,
    capital=100000
):

    portfolio = ranked_df.head(
        portfolio_size
    ).copy()

    weight = 100 / len(portfolio)

    portfolio["WeightPct"] = round(
        weight,
        2
    )

    portfolio["DollarAllocation"] = round(
        capital * (
            portfolio["WeightPct"] / 100
        ),
        2
    )

    portfolio["Shares"] = (
        portfolio["DollarAllocation"]
        / portfolio["Price"]
    ).astype(int)

    portfolio["ActualInvestment"] = round(
        portfolio["Shares"]
        * portfolio["Price"],
        2
    )

    portfolio["CashRemaining"] = round(
        portfolio["DollarAllocation"]
        - portfolio["ActualInvestment"],
        2
    )

    return portfolio


# --------------------------------------------------
# PORTFOLIO SUMMARY
# --------------------------------------------------

def portfolio_summary(
    portfolio_df
):

    total_invested = round(
        portfolio_df[
            "ActualInvestment"
        ].sum(),
        2
    )

    total_cash = round(
        portfolio_df[
            "CashRemaining"
        ].sum(),
        2
    )

    total_positions = len(
        portfolio_df
    )

    print("\n")
    print("=" * 80)
    print("ASX AI INVESTOR PORTFOLIO")
    print("=" * 80)

    print(
        f"Positions: {total_positions}"
    )

    print(
        f"Invested: ${total_invested:,.2f}"
    )

    print(
        f"Cash Remaining: ${total_cash:,.2f}"
    )

    print("=" * 80)

    return {
        "positions": total_positions,
        "invested": total_invested,
        "cash": total_cash
    }


# --------------------------------------------------
# EXPORT PORTFOLIO
# --------------------------------------------------

def save_portfolio(
    portfolio_df,
    filename="portfolio.csv"
):

    portfolio_df.to_csv(
        filename,
        index=False
    )

    print(
        f"Portfolio saved to {filename}"
    )


# --------------------------------------------------
# TOP HOLDINGS REPORT
# --------------------------------------------------

def holdings_report(
    portfolio_df
):

    columns = [

        "Rank",
        "Ticker",
        "Company",

        "FactorScore",

        "Price",

        "WeightPct",

        "DollarAllocation",

        "Shares",

        "ActualInvestment"

    ]

    available_columns = [

        col for col in columns
        if col in portfolio_df.columns

    ]

    return portfolio_df[
        available_columns
    ]


# --------------------------------------------------
# REBALANCE PORTFOLIO
# --------------------------------------------------

def rebalance_portfolio(
    ranked_df,
    current_capital,
    portfolio_size=5
):

    return build_portfolio(
        ranked_df=ranked_df,
        portfolio_size=portfolio_size,
        capital=current_capital
    )


# --------------------------------------------------
# TEST RUN
# --------------------------------------------------

if __name__ == "__main__":

    sample = pd.DataFrame({

        "Rank": [
            1,
            2,
            3,
            4,
            5
        ],

        "Ticker": [
            "BHP.AX",
            "CSL.AX",
            "CBA.AX",
            "MQG.AX",
            "XRO.AX"
        ],

        "Company": [
            "BHP",
            "CSL",
            "Commonwealth Bank",
            "Macquarie",
            "Xero"
        ],

        "Price": [
            45.50,
            300.00,
            170.00,
            210.00,
            140.00
        ],

        "FactorScore": [
            91.0,
            87.0,
            84.0,
            81.0,
            79.0
        ]

    })

    portfolio = build_portfolio(
        ranked_df=sample,
        portfolio_size=5,
        capital=100000
    )

    print("\nPortfolio Holdings\n")

    print(
        holdings_report(
            portfolio
        )
    )

    portfolio_summary(
        portfolio
    )