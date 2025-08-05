import pandas as pd
import argparse
from helpers import tolerant_region_conversion

def read_from_owid(file_path: str, metric_in: str, metric_out: str) -> pd.DataFrame:
    """
    Reads data from an OWID file and returns it as a pandas DataFrame.
    
    Args:
        file_path (str): The path to the OWID file.
        metric_in (str): The metric to extract from the OWID data.
        metric_out (str): The name of the metric in the output file.
        
    Returns:
        pd.DataFrame: A DataFrame containing the data from the OWID file.
    """
    # Read the OWID file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Apply country code conversion only for rows where Code is empty or null
    if 'Code' in df.columns:
        df['Code'] = df.apply(lambda row: tolerant_region_conversion(row['Entity']) if pd.isna(row['Code']) or row['Code'] == '' else row['Code'], axis=1)
    else:
        df['Code'] = df['Entity'].apply(lambda x: tolerant_region_conversion(x))

    # Rename columns for consistency
    df.rename(columns={'Year': 'YEAR', 'Code': 'COUNTRYCODE', metric_in: metric_out}, inplace=True)

    return df[['COUNTRYCODE', 'YEAR', metric_out]]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process Our World In Data data file')
    parser.add_argument('--in', dest='input_file', required=True, help='Path to the input OWID CSV file')
    parser.add_argument('--out', dest='output_file', required=True, help='Path to the output CSV file')
    parser.add_argument('--metric_in', dest='metric_in', required=True, help='Metric to extract from the OWID data')
    parser.add_argument('--metric_out', dest='metric_out', required=True, help='Name of the metric in the output file')

    args = parser.parse_args()

    owid_data = read_from_owid(args.input_file, args.metric_in, args.metric_out)

    owid_data.to_csv(args.output_file, index=False)
    print(f"Data saved to {args.output_file}")
