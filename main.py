print("Program started")

import sys

# Import pipelines
from src.pipeline.runner import run_pipeline
from src.financial_api.fmp_pipeline import run_fmp_pipeline


if __name__ == "__main__":

    # Read argument from terminal
    # Example: python main.py fmp
    choice = sys.argv[1] if len(sys.argv) > 1 else None


    if choice == "yahoo":
        print("Running Yahoo pipeline...")
        run_pipeline(interval_seconds=5)


    elif choice == "fmp":
        print("Running FMP API pipeline...")
        run_fmp_pipeline()


    else:
        print("Usage:")
        print("python main.py yahoo")
        print("python main.py fmp")

