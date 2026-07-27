# Python Data Workflow

## How to execute

python scripts/data_workflow.py

## Workflow

### ingest_data()

Reads the raw CSV file into a Pandas DataFrame.

### process_data()

Removes duplicate rows.

Fills missing values using median.

Removes rows having negative amount.

### output_results()

Saves the processed dataset into data/processed/.

Prints confirmation message.

## Modifying for another dataset

Simply replace the input CSV file and update the processing logic inside process_data().