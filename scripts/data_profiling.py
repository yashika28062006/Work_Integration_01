import pandas as pd


def load_data(filepath):
    """
    Load influencer data from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded dataset.
    """
    return pd.read_csv(filepath)


def profile_dataset(df):
    """
    Display basic information about the dataset.

    Args:
        df (pd.DataFrame): Input dataset.
    """

    print("\n===== DATASET PROFILE =====")

    print(f"\nRows : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumn Types")
    print(df.dtypes)

    print("\nMissing Values")
    print(df.isnull().sum())

    print("\nDuplicate Rows")
    print(df.duplicated().sum())


def profile_numerical(df):
    """
    Display summary statistics for numerical columns.

    Args:
        df (pd.DataFrame): Input dataset.
    """

    print("\n===== NUMERICAL STATISTICS =====")

    numerical_columns = df.select_dtypes(include="number").columns

    for col in numerical_columns:
        print(f"\n{col}")
        print(f"Minimum : {df[col].min()}")
        print(f"Maximum : {df[col].max()}")
        print(f"Mean    : {round(df[col].mean(), 2)}")
        print(f"Median  : {df[col].median()}")


def identify_issues(df, null_threshold=30):
    """
    Identify common data quality issues.

    Args:
        df (pd.DataFrame): Input dataset.
        null_threshold (int): Percentage threshold for null values.
    """

    print("\n===== QUALITY ISSUES =====")

    issues_found = False

    # Check for high null percentages
    for col in df.columns:
        null_percentage = (df[col].isnull().sum() / len(df)) * 100

        if null_percentage > null_threshold:
            print(f"⚠ {col} has {null_percentage:.2f}% missing values.")
            issues_found = True

    # Check duplicate rows
    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        print(f"⚠ Duplicate rows found: {duplicate_count}")
        issues_found = True

    # Check negative values in numerical columns
    numerical_columns = df.select_dtypes(include="number").columns

    for col in numerical_columns:
        if (df[col] < 0).any():
            print(f"⚠ Negative values found in '{col}'.")
            issues_found = True

    if not issues_found:
        print("✓ No major data quality issues found.")


def main():
    """
    Execute the data profiling workflow.
    """

    file_path = "data/raw/sample.csv"

    try:
        df = load_data(file_path)

        profile_dataset(df)
        profile_numerical(df)
        identify_issues(df)

        print("\n✓ Dataset profiling completed successfully!")

    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()