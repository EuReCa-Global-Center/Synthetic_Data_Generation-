import pandas as pd

def validate_time_order(df, earlier_column, later_column):
    """
    Validate the temporal order between two columns in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        earlier_column (str): Name of the column that should contain earlier timestamps.
        later_column (str): Name of the column that should contain later timestamps.

    Returns:
        float: Percentage of rows where the earlier_column is <= later_column.
        int: Total number of rows checked.
        int: Number of rows with correct order.
        int: Number of rows with incorrect order.
    """
    if earlier_column not in df.columns or later_column not in df.columns:
        raise ValueError(f"One or both columns '{earlier_column}', '{later_column}' not found in DataFrame")

    # Convert columns to datetime (handle errors gracefully)
    df[earlier_column] = pd.to_datetime(df[earlier_column], errors='coerce')
    df[later_column] = pd.to_datetime(df[later_column], errors='coerce')

    # Drop rows with invalid dates (NaT values)
    valid_rows = df.dropna(subset=[earlier_column, later_column])

    # Check order: earlier column should be <= later column
    correct_order = valid_rows[earlier_column] <= valid_rows[later_column]
    correct_count = correct_order.sum()
    total_count = len(valid_rows)
    incorrect_count = total_count - correct_count

    correct_percentage = (correct_count / total_count) * 100 if total_count > 0 else 0

    return correct_percentage, total_count, correct_count, incorrect_count

def main():
    # Get file path and column names from user input
    file_path = input("Enter the path to the CSV file: ").strip()
    earlier_column = input("Enter the name of the earlier time column: ").strip()
    later_column = input("Enter the name of the later time column: ").strip()

    try:
        # Load data
        df = pd.read_csv(file_path)

        # Run validation
        percentage, total, correct, incorrect = validate_time_order(df, earlier_column, later_column)

        # Output results
        print(f"\nTime Order Validation Results:")
        print(f"  - Correct Time Order Percentage: {percentage:.2f}%")
        print(f"  - Total Rows Checked: {total}")
        print(f"  - Rows with Correct Order: {correct}")
        print(f"  - Rows with Incorrect Order: {incorrect}")

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()