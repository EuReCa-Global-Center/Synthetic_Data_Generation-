import pandas as pd
import numpy as np
import json
import argparse
from faker import Faker

fake = Faker()

# Mapping SDTypes to Faker generators
def generate_fake_data(sdtype, existing_values=None, metadata=None):
    if sdtype == 'email':
        return fake.email()
    elif sdtype == 'phone_number':
        return fake.phone_number()
    elif sdtype == 'ssn':
        return fake.ssn()
    elif sdtype == 'first_name':
        return fake.first_name()
    elif sdtype == 'last_name':
        return fake.last_name()
    elif sdtype == 'country_code':
        return fake.country_code()
    elif sdtype == 'state_abbr':
        return fake.state_abbr()
    elif sdtype == 'city':
        return fake.city()
    elif sdtype == 'postcode':
        return fake.postcode()
    elif sdtype == 'address':
        return fake.address()
    elif sdtype == 'street_address':
        return fake.street_address()
    elif sdtype == 'secondary_address':
        return fake.secondary_address()
    elif sdtype == 'latitude':
        return fake.latitude()
    elif sdtype == 'longitude':
        return fake.longitude()
    elif sdtype == 'ipv4_address':
        return fake.ipv4()
    elif sdtype == 'ipv6_address':
        return fake.ipv6()
    elif sdtype == 'mac_address':
        return fake.mac_address()
    elif sdtype == 'user_agent_string':
        return fake.user_agent()
    elif sdtype == 'iban':
        return fake.iban()
    elif sdtype == 'credit_card_number':
        return fake.credit_card_number()
    elif sdtype == 'license_plate':
        return fake.license_plate()
    elif sdtype == 'boolean':
        return fake.boolean()
    elif sdtype == 'categorical' and existing_values is not None:
        return np.random.choice(existing_values)
    elif sdtype == 'numerical' and existing_values is not None:
        return np.random.uniform(min(existing_values), max(existing_values))
    elif sdtype == 'datetime' and metadata:
        date_format = metadata.get('datetime_format', '%Y-%m-%d')
        return fake.date_between(start_date='-2y', end_date='today').strftime(date_format)
    return None

# Function to handle missing data
def handle_missing_data(df, metadata, method=1, debug=False):
    modified_rows = []
    
    for col, col_meta in metadata['tables']['fake_hotel_guests']['columns'].items():
        sdtype = col_meta.get('sdtype', 'unknown')
        existing_values = df[col].dropna().unique() if col in df.columns else None
        
        if method == 1:  # Random value based on type
            df[col] = df[col].apply(lambda x: generate_fake_data(sdtype, existing_values, col_meta) if pd.isnull(x) else x)
        elif method == 2:  # Mean/mode for numerical/categorical; random generation for others
            if sdtype == 'numerical' and existing_values is not None and len(existing_values) > 0:
                mean_value = np.mean(existing_values.astype(float))
                df[col].fillna(mean_value, inplace=True)
            elif sdtype == 'categorical' and existing_values is not None and len(existing_values) > 0:
                mode_value = pd.Series(existing_values).mode()[0]
                df[col].fillna(mode_value, inplace=True)
            else:
                df[col] = df[col].apply(lambda x: generate_fake_data(sdtype, existing_values, col_meta) if pd.isnull(x) else x)
        elif method == 3:  # Drop rows with missing data
            df.dropna(subset=[col], inplace=True)
        
        # Collect modified rows for debugging
        modified_rows.append(df[df[col].isnull() == False])

    if debug:
        print("\nModified Rows:")
        print(pd.concat(modified_rows).to_string(index=False))

    return df


# Command-line arguments
parser = argparse.ArgumentParser(description="Handle missing data in a dataset based on metadata.")
parser.add_argument('--input', type=str, required=True, help="Path to the input CSV file")
parser.add_argument('--metadata', type=str, required=True, help="Path to the metadata JSON file")
parser.add_argument('--output', type=str, default="cleaned_data.csv", help="Path to save the cleaned dataset")
parser.add_argument('--method', type=int, choices=[1, 2, 3], required=True, help="Method to handle missing data (1: Random, 2: Mean/Mode, 3: Drop rows)")
parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode to print modified rows")
args = parser.parse_args()

# Load metadata
with open(args.metadata, 'r') as f:
    metadata = json.load(f)

# Load dataset
df = pd.read_csv(args.input)

# Handle missing data
cleaned_df = handle_missing_data(df, metadata, args.method, args.debug)

# Save cleaned data
cleaned_df.to_csv(args.output, index=False)
print(f"Processed data saved to {args.output}")