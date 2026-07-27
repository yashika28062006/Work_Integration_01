import pandas as pd
import os
import json

# ==========================================================
# CREATE REQUIRED FOLDERS
# ==========================================================
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
os.makedirs("output", exist_ok=True)

# ==========================================================
# CREATE SAMPLE DATASET
# ==========================================================
df = pd.DataFrame({
    "name": [
        " John ",
        "JOHN",
        "john ",
        " Alice ",
        "BOB",
        " Bob ",
        None
    ],
    "category": [
        " Electronics ",
        "electronics",
        "ELECTRONICS",
        "Home Appliances",
        "Furniture",
        " furniture ",
        "Electronics"
    ],
    "segment": [
        "B2B",
        "b2b",
        "B 2 B",
        "business-to-business",
        "SME",
        "small medium enterprise",
        "Enterprise"
    ],
    "city": [
        "São Paulo",
        "Montréal",
        "São Paulo",
        "München",
        "Zürich",
        "Québec",
        "Bogotá"
    ]
})

# Save original data
df.to_csv("data/raw/string_data.csv", index=False)

print("=" * 70)
print("ORIGINAL DATA")
print("=" * 70)
print(df)

print("\nCATEGORY VALUE COUNTS BEFORE")
print(df["category"].value_counts(dropna=False))

print("\nNAME VALUE COUNTS BEFORE")
print(df["name"].value_counts(dropna=False))

print("\nFIRST 5 ROWS BEFORE CLEANING")
print(df.head())

# ==========================================================
# TASK 1 - STRIP WHITESPACE
# ==========================================================
print("\n" + "=" * 60)
print("TASK 1 - STRIP WHITESPACE")
print("=" * 60)

string_cols = df.select_dtypes(include=["object", "string"]).columns

total_fixed = 0

for col in string_cols:

    before_unique = df[col].nunique(dropna=False)

    whitespace_count = (
        df[col]
        .fillna("")
        .apply(lambda x: x != x.strip())
        .sum()
    )

    total_fixed += whitespace_count

    df[col] = df[col].str.strip()

    after_unique = df[col].nunique(dropna=False)

    print(f"{col}: {before_unique} -> {after_unique} unique values")
    print(f"Whitespace issues fixed: {whitespace_count}")

print(f"\nTotal whitespace issues fixed: {total_fixed}")

print("\nCATEGORY VALUE COUNTS AFTER STRIP")
print(df["category"].value_counts(dropna=False))

print("\nNAME VALUE COUNTS AFTER STRIP")
print(df["name"].value_counts(dropna=False))

# ==========================================================
# TASK 2 - NORMALIZE CASING
# ==========================================================
print("\n" + "=" * 60)
print("TASK 2 - NORMALIZE CASING")
print("=" * 60)

print("\nBusiness Decision:")
print("Using lowercase for consistency across all text fields.")

columns = ["name", "category", "segment", "city"]

for col in columns:
    df[col] = df[col].str.lower()
    print(f"Normalized '{col}' to lowercase")

print("\nAfter Lowercase")
print(df.head())

# ==========================================================
# TASK 3 - REMOVE SPECIAL CHARACTERS
# ==========================================================
print("\n" + "=" * 60)
print("TASK 3 - REMOVE SPECIAL CHARACTERS")
print("=" * 60)

print("""
Regex Pattern Used:
[^a-zA-Z0-9 ]

Explanation:
^ = NOT
a-z = lowercase letters
A-Z = uppercase letters
0-9 = digits
space = keep spaces

Everything else is removed.
""")

print("\nCities Before Cleaning")
print(df["city"])

df["city"] = df["city"].str.replace(
    r"[^a-zA-Z0-9 ]",
    "",
    regex=True
)

df["segment"] = df["segment"].str.replace(
    r"[^a-zA-Z0-9 ]",
    "",
    regex=True
)

print("\nCities After Cleaning")
print(df["city"])

# ==========================================================
# TASK 4 - STANDARDIZE LABELS
# ==========================================================
print("\n" + "=" * 60)
print("TASK 4 - STANDARDIZE LABELS")
print("=" * 60)

segment_map = {
    "b2b": "B2B",
    "b 2 b": "B2B",
    "businesstobusiness": "B2B",
    "sme": "SMB",
    "small medium enterprise": "SMB",
    "enterprise": "Enterprise"
}

print("\nBusiness Decision")
print("""
All business customer variants are standardized.

b2b
b 2 b
business-to-business

→ B2B

SME
small medium enterprise

→ SMB

enterprise

→ Enterprise
""")

print("\nBefore Mapping")
print(df["segment"].value_counts())

df["segment"] = df["segment"].replace(segment_map)

print("\nAfter Mapping")
print(df["segment"].value_counts())

# ==========================================================
# TASK 5 - REUSABLE FUNCTION
# ==========================================================
print("\n" + "=" * 60)
print("TASK 5 - REUSABLE FUNCTION")
print("=" * 60)


def clean_text_column(
    series,
    lowercase=True,
    strip=True,
    remove_special=False,
    mapping=None
):

    result = series.copy()

    if result.isna().any():
        print(f"Warning: {result.isna().sum()} null values detected.")

    if strip:
        result = result.str.strip()

    if lowercase:
        result = result.str.lower()

    if remove_special:
        result = result.str.replace(
            r"[^a-zA-Z0-9 ]",
            "",
            regex=True
        )

    if mapping is not None:
        result = result.replace(mapping)

    return result


print("\nApplying reusable function...")

df["name"] = clean_text_column(
    df["name"],
    lowercase=True,
    strip=True
)

df["category"] = clean_text_column(
    df["category"],
    lowercase=True,
    strip=True
)

df["city"] = clean_text_column(
    df["city"],
    lowercase=True,
    strip=True,
    remove_special=True
)

df["segment"] = clean_text_column(
    df["segment"],
    lowercase=False,
    strip=True,
    mapping=segment_map
)

print("\nParameter Choices")
print("""
Name:
lowercase=True
strip=True

Category:
lowercase=True
strip=True

City:
lowercase=True
strip=True
remove_special=True

Segment:
mapping=segment_map
""")

# ==========================================================
# EDGE CASE TESTING
# ==========================================================
print("\n" + "=" * 60)
print("EDGE CASE TESTING")
print("=" * 60)

test_cases = pd.Series([
    "  Product A  ",
    "PRODUCT B",
    "Product_C",
    None,
    ""
])

print("Original Test Data")
print(test_cases)

print("\nCleaned Test Data")

print(
    clean_text_column(
        test_cases,
        lowercase=True,
        strip=True,
        remove_special=True
    )
)

# ==========================================================
# SAVE OUTPUTS
# ==========================================================
df.to_csv(
    "data/processed/string_cleaned_data.csv",
    index=False
)

summary = {
    "rows": len(df),
    "columns": list(df.columns),
    "whitespace_fixed": int(total_fixed),
    "regex_used": "[^a-zA-Z0-9 ]",
    "mapping_categories": 3
}

with open(
    "output/string_cleaning_summary.json",
    "w"
) as f:
    json.dump(summary, f, indent=4)

print("\nFIRST 5 ROWS AFTER CLEANING")
print(df.head())

print("\nFINAL CLEANED DATA")
print(df)

print("\n" + "=" * 70)
print("STRING CLEANING COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated Files")
print("data/raw/string_data.csv")
print("data/processed/string_cleaned_data.csv")
print("output/string_cleaning_summary.json")