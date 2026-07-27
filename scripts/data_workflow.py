import pandas as pd
import logging
import os

# ==========================================================
# CONFIGURATION
# ==========================================================

INPUT_FILE = "data/raw/sample.csv"
OUTPUT_FILE = "data/processed/processed_data.csv"
LOG_FILE = "logs/workflow.log"

os.makedirs("data/processed", exist_ok=True)
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================================
# INGEST
# ==========================================================

def ingest_data(filepath):
    """
    Read raw CSV file.

    Input:
        CSV file path

    Returns:
        Pandas DataFrame
    """

    df = pd.read_csv(filepath)

    logging.info(f"Loaded {len(df)} rows.")

    return df


# ==========================================================
# PROCESS
# ==========================================================

def process_data(df):
    """
    Clean and prepare the dataset.

    Input:
        Raw dataframe

    Returns:
        Processed dataframe
    """

    rows_before = len(df)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing amount using median
    df["amount"] = df["amount"].fillna(df["amount"].median())

    # Keep only positive amounts
    df = df[df["amount"] >= 0]

    rows_after = len(df)

    logging.info(
        f"Processed {rows_before} rows -> {rows_after} rows."
    )

    return df


# ==========================================================
# OUTPUT
# ==========================================================

def output_results(df, filepath):
    """
    Save processed dataset.

    Input:
        Processed dataframe

    Output:
        CSV file
    """

    df.to_csv(filepath, index=False)

    logging.info(f"Saved output to {filepath}")

    print("✓ Data successfully processed")
    print(f"✓ Rows processed: {len(df)}")
    print(f"✓ Output saved to {filepath}")


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    try:

        print("=" * 60)
        print("STARTING DATA WORKFLOW")
        print("=" * 60)

        data = ingest_data(INPUT_FILE)

        processed = process_data(data)

        output_results(processed, OUTPUT_FILE)

        print("=" * 60)
        print("WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except FileNotFoundError:
        print("Input file not found.")
        logging.error("Input file missing.")

    except Exception as e:
        print(f"Workflow failed: {e}")
        logging.error(str(e))