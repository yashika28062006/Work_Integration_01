import os
import pandas as pd


def strip_all_strings(df):
    """Strip whitespace from all string columns."""

    string_cols = df.select_dtypes(include=["object", "string"]).columns

    print("\n" + "=" * 60)
    print("TASK 1 - STRIP WHITESPACE")
    print("=" * 60)

    for col in string_cols:
        before = df[col].nunique(dropna=False)

        whitespace_count = (
            df[col]
            .fillna("")
            .astype(str)
            .str.startswith(" ")
            |
            df[col]
            .fillna("")
            .astype(str)
            .str.endswith(" ")
        ).sum()

        df[col] = df[col].str.strip()

        after = df[col].nunique(dropna=False)

        print(f"{col}: {before} → {after} unique values")
        print(f"Whitespace issues fixed: {whitespace_count}")

    return df


def normalize_casing(df, columns_to_lower):
    """Convert specified columns to lowercase."""

    print("\n" + "=" * 60)
    print("TASK 2 - NORMALIZE CASING")
    print("=" * 60)

    for col in columns_to_lower:
        df[col] = df[col].str.lower()
        print(f"Normalized '{col}' to lowercase")

    return df


def remove_special_characters(df, columns):
    """Remove special characters using regex."""

    print("\n" + "=" * 60)
    print("TASK 3 - REMOVE SPECIAL CHARACTERS")
    print("=" * 60)

    for col in columns:
        df[col] = df[col].str.replace(
            r"[^a-zA-Z0-9 ]",
            "",
            regex=True,
        )

        print(f"Removed special characters from '{col}'")

    return df


segment_map = {
    "b2b": "B2B",
    "b 2 b": "B2B",
    "businesstobusiness": "B2B",
    "sme": "SMB",
    "small medium enterprise": "SMB",
    "enterprise": "Enterprise",
}


def standardize_segments(df):
    """Standardize segment labels."""

    print("\n" + "=" * 60)
    print("TASK 4 - STANDARDIZE LABELS")
    print("=" * 60)

    before = df["segment"].value_counts(dropna=False)

    df["segment"] = df["segment"].replace(segment_map)

    after = df["segment"].value_counts(dropna=False)

    print("\nBefore:")
    print(before)

    print("\nAfter:")
    print(after)

    return df


def clean_text_column(
    series,
    lowercase=True,
    strip=True,
    remove_special=False,
    mapping=None,
):
    """Reusable text cleaning function."""

    result = series.copy()

    if strip:
        result = result.str.strip()

    if lowercase:
        result = result.str.lower()

    if remove_special:
        result = result.str.replace(
            r"[^a-zA-Z0-9 ]",
            "",
            regex=True,
        )

    if mapping:
        result = result.replace(mapping)

    return result


def main():

    # Create output folder automatically
    os.makedirs("data/processed", exist_ok=True)

    # Load dataset
    df = pd.read_csv("data/raw/string_data.csv")

    print("=" * 70)
    print("ORIGINAL DATA")
    print("=" * 70)
    print(df)

    print("\nCATEGORY VALUE COUNTS BEFORE")
    print(df["category"].value_counts(dropna=False))

    # Task 1
    df = strip_all_strings(df)

    # Task 2
    df = normalize_casing(
        df,
        [
            "name",
            "category",
            "segment",
            "city",
        ],
    )

    print("\nCATEGORY VALUE COUNTS AFTER LOWERCASE")
    print(df["category"].value_counts(dropna=False))

    # Task 3
    df = remove_special_characters(
        df,
        [
            "city",
            "segment",
        ],
    )

    # Task 4
    df = standardize_segments(df)

    print("\n" + "=" * 60)
    print("TASK 5 - REUSABLE FUNCTION")
    print("=" * 60)

    df["name"] = clean_text_column(
        df["name"],
        lowercase=True,
        strip=True,
    )

    df["category"] = clean_text_column(
        df["category"],
        lowercase=True,
        strip=True,
    )

    df["city"] = clean_text_column(
        df["city"],
        lowercase=True,
        strip=True,
        remove_special=True,
    )

    print("\nFINAL CLEANED DATA")
    print(df)

    # Save cleaned data
    output_path = "data/processed/string_cleaned_data.csv"

    df.to_csv(
        output_path,
        index=False,
    )

    print("\n" + "=" * 70)
    print("STRING CLEANING COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print(f"Cleaned dataset saved to:\n{output_path}")


if __name__ == "__main__":
    main()