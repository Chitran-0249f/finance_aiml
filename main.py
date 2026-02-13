print("Program started")

from src.pipeline.runner import run_pipeline

if __name__ == "__main__":
    # Run pipeline every 30 seconds
    run_pipeline(interval_seconds=5)
