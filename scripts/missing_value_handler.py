import pandas as pd


def analyze_missing_before(df):
    """
    Display missing values before handling them.

    Input:
        df - Pandas DataFrame

    Output:
        Prints null count and percentage for each column.
    """

    print("\n===== BEFORE IMPUTATION =====")

    for col in df.columns:
        null_count = df[col].isnull().sum()
        null_percent = (null_count / len(df)) * 100

        if null_count > 0:
            print(f"{col}: {null_count} missing ({null_percent:.2f}%)")

    print()


def handle_missing_values(df):
    """
    Handle missing values based on data type.

    Strategy:
    - Drop rows with missing 'id'
    - Fill numerical columns using median
    - Fill text columns using mode

    Returns:
        Cleaned DataFrame
    """

    # Drop rows where influencer id is missing
    if "id" in df.columns:
        df = df.dropna(subset=["id"])

    # Fill numerical columns with median
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median = df[col].median()
            df[col] = df[col].fillna(median)

    # Fill categorical columns with mode
    object_cols = df.select_dtypes(include="object").columns

    for col in object_cols:
        if df[col].isnull().sum() > 0:
            mode = df[col].mode()[0]
            df[col] = df[col].fillna(mode)

    return df


def analyze_missing_after(df):
    """
    Display missing values after handling.
    """

    print("===== AFTER IMPUTATION =====")

    total_missing = df.isnull().sum()

    if total_missing.sum() == 0:
        print("No missing values remaining.")
    else:
        print(total_missing)

    print()


if __name__ == "__main__":

    try:
        df = pd.read_csv("data/raw/sample.csv")

        analyze_missing_before(df)

        cleaned_df = handle_missing_values(df)

        analyze_missing_after(cleaned_df)

        cleaned_df.to_csv(
            "output/cleaned_sample.csv",
            index=False
        )

        print("✓ Missing values handled successfully!")
        print("✓ Cleaned dataset saved to output/cleaned_sample.csv")

    except FileNotFoundError:
        print("Error: data/raw/sample.csv not found.")

    except Exception as e:
        print(f"Error: {e}")