import pandas as pd


def ingest_csv(filepath, delimiter=",", encoding="utf-8"):
    """
    Read a CSV file using explicit delimiter and encoding.

    Input:
        filepath (str)

    Returns:
        Pandas DataFrame
    """

    df = pd.read_csv(
        filepath,
        delimiter=delimiter,
        encoding=encoding
    )

    return df


def ingest_json(filepath):
    """
    Read and flatten JSON data.

    Input:
        filepath (str)

    Returns:
        Pandas DataFrame
    """

    df = pd.read_json(filepath)
    df = pd.json_normalize(df.to_dict(orient="records"))

    return df


def document_ingestion(df, source):
    """
    Print ingestion summary.
    """

    print(f"\n===== {source} =====")
    print(f"Rows : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumn Types")
    print(df.dtypes)

    print("\nFirst 3 Rows")
    print(df.head(3))


if __name__ == "__main__":

    csv_df = ingest_csv("data/raw/sample.csv")

    json_df = ingest_json("data/json/sample.json")

    document_ingestion(csv_df, "CSV REPORT")

    document_ingestion(json_df, "JSON REPORT")
    