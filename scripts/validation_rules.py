import os
import json
import pandas as pd


def load_data():
    """Load dataset and convert date columns."""

    df = pd.read_csv("data/raw/validation_data.csv")

    date_cols = ["birth_date", "start_date", "end_date"]

    for col in date_cols:
        df[col] = pd.to_datetime(df[col])

    return df


def range_checks(df):
    print("\n" + "=" * 60)
    print("TASK 1 - RANGE CHECKS")
    print("=" * 60)

    df["valid_age"] = (df["age"] >= 0) & (df["age"] <= 150)
    df["valid_price"] = df["price"] >= 0
    df["valid_birth_date"] = (
        (df["birth_date"] >= pd.Timestamp("1920-01-01"))
        & (df["birth_date"] <= pd.Timestamp.now())
    )

    print(f"Invalid ages        : {(~df['valid_age']).sum()}")
    print(f"Invalid prices      : {(~df['valid_price']).sum()}")
    print(f"Invalid birth dates : {(~df['valid_birth_date']).sum()}")

    return df


def null_constraints(df):
    print("\n" + "=" * 60)
    print("TASK 2 - NULL CONSTRAINTS")
    print("=" * 60)

    df["valid_customer_id"] = df["customer_id"].notna()
    df["valid_email"] = df["email"].notna()

    print(f"Missing Customer IDs : {(~df['valid_customer_id']).sum()}")
    print(f"Missing Emails       : {(~df['valid_email']).sum()}")

    return df


def format_validation(df):
    print("\n" + "=" * 60)
    print("TASK 3 - FORMAT VALIDATION")
    print("=" * 60)

    df["valid_email_format"] = df["email"].str.contains("@", na=False)

    df["valid_phone"] = df["phone"].astype(str).str.match(
        r"^\d{10}$",
        na=False,
    )

    print(f"Invalid Emails : {(~df['valid_email_format']).sum()}")
    print(f"Invalid Phones : {(~df['valid_phone']).sum()}")

    return df


def business_rules(df):
    print("\n" + "=" * 60)
    print("TASK 4 - BUSINESS RULES")
    print("=" * 60)

    df["valid_date_order"] = (
        df["end_date"] >= df["start_date"]
    )

    print(
        f"Invalid Date Ranges : {(~df['valid_date_order']).sum()}"
    )

    return df


def referential_integrity(df):
    """
    Simple example.
    Valid customer ids are assumed to exist
    if they are not null.
    """

    print("\n" + "=" * 60)
    print("EXTRA - REFERENTIAL INTEGRITY")
    print("=" * 60)

    valid_ids = {101, 102, 103, 104, 105, 106}

    df["valid_reference"] = df["customer_id"].isin(valid_ids)

    print(
        f"Invalid References : {(~df['valid_reference']).sum()}"
    )

    return df


def validation_report(df):

    print("\n" + "=" * 60)
    print("TASK 5 - VALIDATION REPORT")
    print("=" * 60)

    validation_cols = [
        "valid_age",
        "valid_price",
        "valid_birth_date",
        "valid_customer_id",
        "valid_email",
        "valid_email_format",
        "valid_phone",
        "valid_date_order",
    ]

    df["passes_all_checks"] = (
        df[validation_cols]
        .all(axis=1)
    )

    failures = df[
        ~df["passes_all_checks"]
    ]

    passed = df[
        df["passes_all_checks"]
    ]

    os.makedirs("output", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    failures.to_csv(
        "output/validation_failures.csv",
        index=False,
    )

    passed.to_csv(
        "data/processed/validated_data.csv",
        index=False,
    )

    report = {
        "total_records": int(len(df)),
        "passed": int(df["passes_all_checks"].sum()),
        "failed": int((~df["passes_all_checks"]).sum()),
        "validation_rules": validation_cols,
    }

    with open(
        "output/validation_report.json",
        "w",
    ) as f:
        json.dump(report, f, indent=4)

    print(f"Records : {len(df)}")
    print(f"Passed  : {report['passed']}")
    print(f"Failed  : {report['failed']}")

    print("\nValidation report saved.")
    print("output/validation_report.json")
    print("output/validation_failures.csv")
    print("data/processed/validated_data.csv")

    return df


def main():

    print("=" * 70)
    print("DATA CONSISTENCY & VALIDATION RULES")
    print("=" * 70)

    df = load_data()

    print("\nOriginal Dataset")
    print(df)

    df = range_checks(df)

    df = null_constraints(df)

    df = format_validation(df)

    df = business_rules(df)

    df = referential_integrity(df)

    df = validation_report(df)

    print("\nValidation Complete.")


if __name__ == "__main__":
    main()