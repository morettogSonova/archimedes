import pandas as pd
import argparse

from helpers import tolerant_country_name_to_code_conversion

def read_md_horizontal(file_path):
    df_population = read_population(file_path)
    df_gdp = read_gdp(file_path)
    df_per_capita_gdp = read_per_capita_gdp(file_path)

    df = pd.merge(df_population, df_gdp, on=['COUNTRYCODE', 'YEAR'], how='outer')
    df = pd.merge(df, df_per_capita_gdp, on=['COUNTRYCODE', 'YEAR'], how='outer')

    return df

def read_population(file_path: str) -> pd.DataFrame:
    """
    Reads population data from a file and returns it as a pandas DataFrame.
    
    Args:
        file_path (str): The path to the population data file.
        
    Returns:
        pd.DataFrame: A DataFrame containing the population data.
    """
    df = pd.read_excel(file_path, sheet_name='Population', header=0, index_col=0)
    # Convert all index (country names) to country codes first
    df.index = df.index.map(lambda x: tolerant_country_name_to_code_conversion(x))
    df = df.reset_index()
    df = df.melt(id_vars=df.columns[0], var_name='YEAR', value_name='POPULATION')
    df.rename(columns={df.columns[0]: 'COUNTRYCODE'}, inplace=True)
    df = df[df['YEAR'].astype(str).str.isdigit()]
    df['POPULATION'] = df['POPULATION'] * 1000
    df = df[df['COUNTRYCODE'].str.len() == 3]
    df = df[['COUNTRYCODE', 'YEAR', 'POPULATION']]
    return df


def read_gdp(file_path: str) -> pd.DataFrame:
    """
    Reads GDP data from a file and returns it as a pandas DataFrame.

    Args:
        file_path (str): The path to the GDP data file.

    Returns:
        pd.DataFrame: A DataFrame containing the GDP data.
    """
    df = pd.read_excel(file_path, sheet_name='GDP', header=0, index_col=0)
    # Convert all index (country names) to country codes first
    df.index = df.index.map(lambda x: tolerant_country_name_to_code_conversion(x))
    df = df.reset_index()
    df = df.melt(id_vars=df.columns[0], var_name='YEAR', value_name='GDPVALUE')
    df.rename(columns={df.columns[0]: 'COUNTRYCODE'}, inplace=True)
    df = df[df['YEAR'].astype(str).str.isdigit()]
    df['GDPVALUE'] = df['GDPVALUE'] * 1000000
    df = df[df['COUNTRYCODE'].str.len() == 3]
    df = df[['COUNTRYCODE', 'YEAR', 'GDPVALUE']]
    return df


def read_per_capita_gdp(file_path: str) -> pd.DataFrame:
    """
    Reads per capita GDP data from a file and returns it as a pandas DataFrame.

    Args:
        file_path (str): The path to the per capita GDP data file.

    Returns:
        pd.DataFrame: A DataFrame containing the per capita GDP data.
    """
    df = pd.read_excel(file_path, sheet_name='PerCapita GDP', header=0, index_col=0)
    # Convert all index (country names) to country codes first
    df.index = df.index.map(lambda x: tolerant_country_name_to_code_conversion(x))
    df = df.reset_index()
    df = df.melt(id_vars=df.columns[0], var_name='YEAR', value_name='PERCAPITAGDP')
    df.rename(columns={df.columns[0]: 'COUNTRYCODE'}, inplace=True)
    df = df[df['YEAR'].astype(str).str.isdigit()]
    df['PERCAPITAGDP'] = df['PERCAPITAGDP']
    df = df[df['COUNTRYCODE'].str.len() == 3]
    df = df[['COUNTRYCODE', 'YEAR', 'PERCAPITAGDP']]
    return df


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process horizontal markdown data file')
    parser.add_argument('--in', dest='input_file', required=True, help='Path to the input horizontal markdown CSV file')
    parser.add_argument('--out', dest='output_file', required=True, help='Path to save the output file')

    args = parser.parse_args()

    md_data = read_md_horizontal(args.input_file)

    if args.output_file:
        md_data.to_csv(args.output_file, index=False)
        print(f"Data saved to {args.output_file}")