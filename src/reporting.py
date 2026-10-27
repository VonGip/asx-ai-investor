"""
reporting.py

Exports rankings, portfolio holdings,
summary statistics and latest run results.

Author: Lee + Copilot
"""

from datetime import datetime
import os


def save_reports(
    scored_df,
    ranked_df,
    portfolio_df
):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_dir = "output"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    scored_file = (
        f"{output_dir}/scored_{timestamp}.csv"
    )

    ranked_file = (
        f"{output_dir}/ranked_{timestamp}.csv"
    )

    portfolio_file = (
        f"{output_dir}/portfolio_{timestamp}.csv"
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

    summary_file = (
        f"{output_dir}/summary_{timestamp}.txt"
    )

    with open(
        summary_file,
        "w"
    ) as f:

        f.write(
            "ASX AI INVESTOR\n"
        )

        f.write(
            "=" * 40
            + "\n\n"
        )

        f.write(
            "TOP 5 HOLDINGS\n\n"
        )

        for _, row in portfolio_df.iterrows():

            f.write(
                f"{row['Ticker']} "
                f"{row['WeightPct']}%\n"
            )

    print(
        "\nReports Exported"
    )
