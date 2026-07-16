import pandas as pd


def ingest_data(filepath):
    """
    Reads data from a CSV file.

    Input:
        filepath -> path of csv file

    Returns:
        Pandas DataFrame
    """

    df = pd.read_csv(filepath)
    return df


def process_data(df):
    """
    Cleans and processes the data.

    Input:
        Raw DataFrame

    Returns:
        Cleaned DataFrame
    """

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing salary with median salary
    df["salary"] = df["salary"].fillna(df["salary"].median())

    return df


def output_results(df, output_path):
    """
    Saves processed data.

    Input:
        Processed DataFrame

    Returns:
        None
    """

    df.to_csv(output_path, index=False)

    print("✓ Data successfully processed")
    print(f"✓ Rows processed: {len(df)}")
    print(f"✓ Output saved to {output_path}")


if __name__ == "__main__":

    data = ingest_data("data/raw/sample.csv")

    processed = process_data(data)

    output_results(processed, "output/processed.csv")