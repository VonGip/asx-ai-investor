# Calculates company quality, value, growth and momentum scores
# Calculates company quality, value, growth and momentum scores
"""
factor_engine.py

ASX AI Investor

Calculates factor scores using:

- ROE
- Revenue Growth
- Debt To Equity
- PE Ratio
- 6 Month Momentum
- 12 Month Momentum

Higher score = more attractive stock.

Author: Lee + Copilot
"""

import pandas as pd


# --------------------------------------------------
# NORMALISATION
# --------------------------------------------------

def normalise(series):
    """
    Convert values into a 0-100 scale.
    """

    minimum = series.min()
    maximum = series.max()

    if minimum == maximum:

        return pd.Series(
            [50] * len(series),
            index=series.index
        )

    return (
        (
            series - minimum
        ) /
        (
            maximum - minimum
        )
    ) * 100


# --------------------------------------------------
# MAIN SCORING FUNCTION
# --------------------------------------------------

def score_stocks(df):

    scored = df.copy()

    # ------------------------------------------
    # REMOVE ONLY TRULY BAD DATA
    # ------------------------------------------

    scored = scored.dropna(
        subset=[
            "ROE",
            "RevenueGrowth"
        ]
    )

    scored = scored[
    scored["ROE"] > 0
    ]

    scored = scored[
    scored["RevenueGrowth"] > 0
    ]
    # ------------------------------------------
    # FILL MISSING PE VALUES
    # ------------------------------------------

    scored["PE"] = scored["PE"].fillna(
        scored["PE"].median()
    )

    # ------------------------------------------
    # FILL MISSING DEBT VALUES
    # ------------------------------------------

    scored["DebtToEquity"] = (
        scored["DebtToEquity"].fillna(
            scored["DebtToEquity"].median()
        )
    )

    # ------------------------------------------
    # MOMENTUM FALLBACKS
    # ------------------------------------------

    scored["Momentum6M"] = (
        scored["Momentum6M"]
        .fillna(0)
    )

    scored["Momentum12M"] = (
        scored["Momentum12M"]
        .fillna(0)
    )

    # ------------------------------------------
    # POSITIVE FACTORS
    # HIGHER IS BETTER
    # ------------------------------------------

    scored["ROE_Score"] = normalise(
        scored["ROE"]
    )

    scored["RevenueGrowth_Score"] = normalise(
        scored["RevenueGrowth"]
    )

    scored["Momentum6M_Score"] = normalise(
        scored["Momentum6M"]
    )

    scored["Momentum12M_Score"] = normalise(
        scored["Momentum12M"]
    )

    # ------------------------------------------
    # NEGATIVE FACTORS
    # LOWER IS BETTER
    # ------------------------------------------

    scored["PE_Score"] = (
        100 -
        normalise(
            scored["PE"]
        )
    )

    scored["DebtToEquity_Score"] = (
        100 -
        normalise(
            scored["DebtToEquity"]
        )
    )

    # ------------------------------------------
    # WEIGHTINGS
    # ------------------------------------------

    scored["FactorScore"] = (

        scored["ROE_Score"] * 0.20 +

        scored["RevenueGrowth_Score"] * 0.15 +

        scored["DebtToEquity_Score"] * 0.10 +

        scored["PE_Score"] * 0.10 +

        scored["Momentum6M_Score"] * 0.20 +

        scored["Momentum12M_Score"] * 0.25

    )

    scored["FactorScore"] = (
        scored["FactorScore"]
        .round(2)
    )

    return scored

# --------------------------------------------------
# FACTOR BREAKDOWN
# --------------------------------------------------

def factor_breakdown(df):

    columns = [

        "Ticker",

        "ROE",

        "RevenueGrowth",

        "PE",

        "DebtToEquity",

        "Momentum6M",

        "Momentum12M",

        "ROE_Score",

        "RevenueGrowth_Score",

        "PE_Score",

        "DebtToEquity_Score",

        "Momentum6M_Score",

        "Momentum12M_Score",

        "FactorScore"

    ]

    available_columns = [

        column
        for column in columns
        if column in df.columns

    ]

    return df[
        available_columns
    ]


# --------------------------------------------------
# TOP FACTOR SCORES
# --------------------------------------------------

def top_factor_scores(
    df,
    top_n=10
):

    return (
        df.sort_values(
            by="FactorScore",
            ascending=False
        )
        .head(top_n)
    )


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    sample = pd.DataFrame({

        "Ticker": [
            "AAA",
            "BBB",
            "CCC"
        ],

        "ROE": [
            10,
            20,
            30
        ],

        "RevenueGrowth": [
            5,
            10,
            15
        ],

        "DebtToEquity": [
            150,
            75,
            30
        ],

        "PE": [
            30,
            20,
            10
        ],

        "Momentum6M": [
            2,
            10,
            25
        ],

        "Momentum12M": [
            4,
            12,
            30
        ]

    })

    scored = score_stocks(
        sample
    )

    print("\nFactor Rankings\n")

    print(

        scored[
            [
                "Ticker",
                "FactorScore"
            ]
        ]
        .sort_values(
            by="FactorScore",
            ascending=False
        )

    )