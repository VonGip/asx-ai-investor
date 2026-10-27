# Main program that runs the entire workflow
"""
run_pipeline.py

ASX AI Investor
End-to-End Execution Pipeline

Workflow:

1. Load market data
2. Calculate factor scores
3. Rank stocks
4. Build portfolio
5. Save outputs
6. Display results

Author: Lee + Copilot
"""

from datetime import datetime
import os

from data_loader import load_data
from factor_engine import score_stocks
from ranking_engine import (
    rank_stocks,
    print_summary,
    candidate_report
)
from portfolio_builder import (
    build_portfolio,
    portfolio_summary,
    holdings_report
)


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PORTFOLIO_SIZE = 5

STARTING_CAPITAL = 100000

OUTPUT_FOLDER = "output"


# --------------------------------------------------
# CREATE OUTPUT DIRECTORY
# --------------------------------------------------

def create_output_folder():

    if not os.path.exists(
        OUTPUT_FOLDER
    ):
        os.makedirs(
            OUTPUT_FOLDER
        )


# --------------------------------------------------
# SAVE OUTPUT FILES
# --------------------------------------------------

def save_outputs(
    scored_df,
    ranked_df,
    portfolio_df
):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    scored_file = (
        f"{OUTPUT_FOLDER}/"
        f"scored_data_{timestamp}.csv"
    )

    ranked_file = (
        f"{OUTPUT_FOLDER}/"
        f"rankings_{timestamp}.csv"
    )

    portfolio_file = (
        f"{OUTPUT_FOLDER}/"
        f"portfolio_{timestamp}.csv"
    )

    scored_df.to_csv(
        scored_file,
        index=False
    )

    ranked_df.to_csv(
        ranked_file,
        index=False
    )

    portfolio_df.to_csv(
        portfolio_file,
        index=False
    )

    print("\n")
    print("=" * 80)
    print("FILES SAVED")
    print("=" * 80)

    print(scored_file)
    print(ranked_file)
    print(portfolio_file)


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------

def main():

    print("\n")
    print("=" * 80)
    print("ASX AI INVESTOR")
    print("FACTOR MODEL PIPELINE")
    print("=" * 80)

    create_output_folder()

    # ------------------------------------------
    # STEP 1
    # LOAD DATA
    # ------------------------------------------

    print("\nSTEP 1")
    print("Loading market data...")

    raw_data = load_data()

    if raw_data.empty:

        print(
            "No market data returned."
        )

        return

    # ------------------------------------------
    # STEP 2
    # SCORE STOCKS
    # ------------------------------------------

    print("\nSTEP 2")
    print("Calculating factor scores...")

    scored_data = score_stocks(
        raw_data
    )

    print("\n")
    print("=" * 80)
    print("FACTOR SCORE BREAKDOWN")
    print("=" * 80)

    print(
        scored_data[
            [
                "Ticker",
                "ROE_Score",
                "RevenueGrowth_Score",
                "PE_Score",
                "DebtToEquity_Score",
                "Momentum6M_Score",
                "Momentum12M_Score",
                "FactorScore"
            ]
        ]
        .sort_values(
            by="FactorScore",
            ascending=False
        )
)
    # ------------------------------------------
    # STEP 3
    # RANK STOCKS
    # ------------------------------------------

    print("\nSTEP 3")
    print("Ranking stocks...")

    ranked_data = rank_stocks(
        scored_data
    )

    print_summary(
        ranked_data,
        top_n=10
    )

    # ------------------------------------------
    # STEP 4
    # BUILD PORTFOLIO
    # ------------------------------------------

    print("\nSTEP 4")
    print("Building portfolio...")

    portfolio = build_portfolio(
        ranked_df=ranked_data,
        portfolio_size=PORTFOLIO_SIZE,
        capital=STARTING_CAPITAL
    )

    # ------------------------------------------
    # STEP 5
    # DISPLAY PORTFOLIO
    # ------------------------------------------

    print("\n")
    print("=" * 80)
    print("PORTFOLIO HOLDINGS")
    print("=" * 80)

    print(
        holdings_report(
            portfolio
        )
    )

    portfolio_summary(
        portfolio
    )

    # ------------------------------------------
    # STEP 6
    # TOP CANDIDATES
    # ------------------------------------------

    print("\n")
    print("=" * 80)
    print("TOP INVESTMENT CANDIDATES")
    print("=" * 80)

    print(
        candidate_report(
            ranked_data,
            top_n=5
        )
    )

    # ------------------------------------------
    # STEP 7
    # SAVE FILES
    # ------------------------------------------

    print("\nSTEP 5")
    print("Saving outputs...")

    save_outputs(
        scored_data,
        ranked_data,
        portfolio
    )

    print("\n")
    print("=" * 80)
    print("PIPELINE COMPLETE")
    print("=" * 80)

    ranked_data.to_csv(
        "output/latest_rankings.csv",
        index=False
    )

    portfolio.to_csv(
        "output/latest_portfolio.csv",
        index=False
    )

# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    main()