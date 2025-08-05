import country_converter as coco
import pandas as pd
import argparse

from helpers import tolerant_country_code_conversion

def read_from_wipo(file_path: str) -> pd.DataFrame:
    """
    Reads data from a WIPO file and returns it as a pandas DataFrame.
    
    Args:
        file_path (str): The path to the WIPO file.
        
    Returns:
        pd.DataFrame: A DataFrame containing the data from the WIPO file.
    """
    # Read the WIPO file into a DataFrame
    df = pd.read_csv(file_path)
    out_df = pd.DataFrame()
    
    # Convert country codes to names using country_converter
    out_df['COUNTRYCODE'] = df['office_code'].apply(lambda x: tolerant_country_code_conversion(x))
    out_df['PATENTFILINGS'] = df['filings']
    out_df['YEAR'] = df['filing_year']

    return out_df




if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Process WIPO data file')
    parser.add_argument('--in', dest='input_file', required=True, help='Path to the input WIPO CSV file')
    parser.add_argument('--out', dest='output_file', required=True, help='Path to save the output file')
    
    args = parser.parse_args()
    
    wipo_data = read_from_wipo(args.input_file)
    
    if args.output_file:
        wipo_data.to_csv(args.output_file, index=False)
        print(f"Data saved to {args.output_file}")
    