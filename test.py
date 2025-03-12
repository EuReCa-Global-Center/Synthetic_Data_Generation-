#!/usr/bin/env python3

import argparse
import pandas as pd
import json
from sdv.metadata import Metadata
from sdv.single_table import (
    GaussianCopulaSynthesizer,
    CTGANSynthesizer,
    TVAESynthesizer,
    CopulaGANSynthesizer
)
from sdv.evaluation.single_table import evaluate_quality, get_column_plot

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Generate synthetic data using SDV synthesizers.")
parser.add_argument('--input', type=str, required=True, help="Path to the input CSV file containing real data")
parser.add_argument('--metadata', type=str, required=True, help="Path to the JSON metadata file")
parser.add_argument('--synthesizer', type=str, required=True, choices=['gaussian', 'ctgan', 'tvae', 'copulagan'], 
                    help="Choose the synthesizer: gaussian, ctgan, tvae, or copulagan")

args = parser.parse_args()

# Load real data from CSV
real_data = pd.read_csv(args.input)

# Load metadata from JSON and convert to Metadata class
with open(args.metadata, 'r') as f:
    metadata_dict = json.load(f)

metadata = Metadata.load_from_dict(metadata_dict)  # Using the new recommended Metadata class

# Debugging: Print column names
print("Columns in cleaned_data.csv:", real_data.columns.tolist())
print("Columns in metadata:", list(metadata_dict["tables"]["fake_hotel_guests"]["columns"].keys()))

# Align columns to match metadata
metadata_columns = list(metadata_dict["tables"]["fake_hotel_guests"]["columns"].keys())
real_data = real_data.reindex(columns=metadata_columns)

# Select the synthesizer based on user input
synthesizers = {
    'gaussian': GaussianCopulaSynthesizer,
    'ctgan': CTGANSynthesizer,
    'tvae': TVAESynthesizer,
    'copulagan': CopulaGANSynthesizer
}

selected_synthesizer = synthesizers[args.synthesizer](metadata)

# Fit the synthesizer
print(f"Using {args.synthesizer.upper()} synthesizer...")
selected_synthesizer.fit(data=real_data)

# Generate synthetic data
synthetic_data = selected_synthesizer.sample(num_rows=500)

# Evaluate the quality of the synthetic data
quality_report = evaluate_quality(real_data, synthetic_data, metadata)
print("\nQuality Report:\n", quality_report)

# Generate column plot
fig = get_column_plot(
    real_data=real_data,
    synthetic_data=synthetic_data,
    column_name='amenities_fee',  # Change column if needed
    metadata=metadata,
    plot_type="bar"
)

fig.show()

# Save synthetic data
synthetic_data.to_csv("synthetic_data.csv", index=False)
print("\nSynthetic data saved to synthetic_data.csv")