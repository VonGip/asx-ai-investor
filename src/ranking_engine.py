# Combines scores and ranks ASX companies
"""
ranking_engine.py

Ranks stocks based on FactorScore and
produces the master ranking table.

Input:
DataFrame containing FactorScore

Output:
Ranked DataFrame with Rank column

Author: Lee + Copilot
"""

import pandas as pd


# --------------------------------------------------
# RANK STOCKS
# --------------------------------------------------

def rank_stocks(df):

    ranked = df.copy()

    ranked = ranked.sort_values(
        by="FactorScore",
        ascending=False
    )

    ranked = ranked.reset_index(
        drop=True
    )

    ranked["Rank"] = (
        ranked.index + 1
    )

    columns = [

        "Rank",
        "Ticker",
        "Company",
        "FactorScore",

        "Price",

        "ROE",
        "RevenueGrowth",

        "PE",
        "DebtToEquity",

        "Momentum6M",
        "Momentum12M"

    ]

    available_columns = [

        col for col in columns
        if col in ranked.columns

    ]

    ranked = ranked[
        available_columns
    ]

    return ranked


# --------------------------------------------------
# TOP STOCKS
# --------------------------------------------------

def get_top_stocks(
    ranked_df,
    top_n=5
):

    return ranked_df.head(top_n)


# --------------------------------------------------
# EXPORT RANKINGS
# --------------------------------------------------

def save_rankings(
    ranked_df,
    filename="rankings.csv"
):

    ranked_df.to_csv(
        filename,
        index=False
    )

    print(
        f"Rankings saved to {filename}"
    )


# --------------------------------------------------
# RANKING SUMMARY
# --------------------------------------------------

def print_summary(
    ranked_df,
    top_n=10
):

    print("\n")
    print("=" * 80)
    print("ASX AI INVESTOR RANKINGS")
    print("=" * 80)

    display_df = ranked_df.head(
        top_n
    )

    print(
        display_df[
            [
                "Rank",
                "Ticker",
                "FactorScore"
            ]
        ]
    )

    print("\n")
    print(
        f"Total Stocks Ranked: {len(ranked_df)}"
    )


# --------------------------------------------------
# TOP CANDIDATES REPORT
# --------------------------------------------------

def candidate_report(
    ranked_df,
    top_n=5
):

    candidates = ranked_df.head(
        top_n
    )

    report_columns = [

        "Rank",
        "Ticker",
        "Company",

        "FactorScore",

        "ROE",
        "RevenueGrowth",

        "PE",
        "DebtToEquity",

        "Momentum6M",
        "Momentum12M"

    ]

    available_columns = [

        c for c in report_columns
        if c in candidates.columns

    ]

    return candidates[
        available_columns
    ]


# --------------------------------------------------
# TEST RUN
# --------------------------------------------------

if __name__ == "__main__":

    sample = pd.DataFrame({

        "Ticker": [
            "BHP.AX",
            "CSL.AX",
            "CBA.AX"
        ],

        "Company": [
            "BHP",
            "CSL",
            "Commonwealth Bank"
        ],

        "Price": [
            46.50,
            312.75,
            172.30
        ],

        "FactorScore": [
            85.3,
            78.7,
            73.2
        ],

        "ROE": [
            24.2,
            18.5,
            13.1
        ],

        "RevenueGrowth": [
            10.5,
            12.8,
            6.2
        ],

        "PE": [
            12.4,
            31.5,
            25.7
        ],

        "DebtToEquity": [
            38.0,
            22.0,
            145.0
        ],

        "Momentum6M": [
            18.4,
            12.2,
            6.8
        ],

        "Momentum12M": [
            27.5,
            19.6,
            11.4
        ]

    })

    ranked = rank_stocks(
        sample
    )

    print_summary(
        ranked
    )

    print("\nTop Candidates\n")

    print(
        candidate_report(
            ranked,
            top_n=3
        )
    )