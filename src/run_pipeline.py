# Main program that runs the entire workflow
from data_loader import load_data
from factor_engine import calculate_factors
from ranking_engine import rank_stocks
from portfolio_builder import build_portfolio


print("ASX AI Investor Starting...")

load_data()

calculate_factors()

rank_stocks()

build_portfolio()

print("Finished.")