import pandas as pd
import argparse
import dataclasses
from bs4 import BeautifulSoup
from typing import List
from helpers import tolerant_country_name_to_code_conversion

@dataclasses.dataclass
class Nobel_Laureate:
    country: str
    year: int

def read_nobel_laureates(file_path: str, fields: List[str]) -> pd.DataFrame:
    """
    Reads data from a Nobel laureates file and returns it as a pandas DataFrame.
    
    Args:
        file_path (str): The path to the Nobel laureates file.
        fields (list[str]): List of fields to include for Nobel prize.
        
    Returns:
        pd.DataFrame: A DataFrame containing the data from the Nobel laureates file.
    """
    # Read the Nobel laureates file which is in HTML format
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        # Find the table containing laureate data
        table = soup.find('tbody')

        if not table:
            raise ValueError("Could not find tbody with laureate data in the HTML file")
            
        data: List[Nobel_Laureate] = []

        rows = table.find_all('tr')
        current_year: int = 1901
        for row in rows:
            # Extract cells from the row
            cells = row.find_all('td')
            if len(cells) == 5:
                current_year = int(cells[0].get_text(strip=True))
                field = cells[1].get_text(strip=True)
                country = cells[3].get_text(strip=True)
            elif len(cells) == 4:  # Ensure row has enough data
                field = cells[0].get_text(strip=True)
                country = cells[2].get_text(strip=True)

            data.append({
                'field': field,
                'country': country,
                'year': current_year
            })

    filtered_data: List[Nobel_Laureate] = [item for item in data if item['field'].lower() in fields]

    df = pd.DataFrame(filtered_data)
    df['isocode'] = df['country'].apply(lambda x: tolerant_country_name_to_code_conversion(x))

    out_df = pd.DataFrame()
    out_df['YEAR'] = df['year']
    out_df['COUNTRY'] = df['isocode']
    # Group by year and country, count the number of laureates, and reset index to get a DataFrame
    laureate_counts = df.groupby(['year', 'isocode']).size().reset_index(name='count')
    
    # Merge the counts back to out_df
    out_df = out_df.merge(laureate_counts[['year', 'isocode', 'count']], 
                         left_on=['YEAR', 'COUNTRY'], 
                         right_on=['year', 'isocode'],
                         how='left')
    
    # Assign the count to NOBELLAUREATES column and drop unnecessary columns
    out_df['NOBELLAUREATES'] = out_df['count'].fillna(0).astype(int)
    out_df = out_df.drop(['year', 'isocode', 'count'], axis=1)
    
    return out_df

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process Nobel laureates data file')
    parser.add_argument('--in', dest='input_file', required=True, help='Path to the input Nobel laureates HTML file')
    parser.add_argument('--out', dest='output_file', required=True, help='Path to save the output file')
    parser.add_argument('--fields', dest='fields', type=List[str], default=['physiology/medicine', 'chemistry', 'physics'], help='Filter by year of Nobel prize')

    args = parser.parse_args()
    
    nobel_data = read_nobel_laureates(args.input_file, args.fields)
    
    if args.output_file:
        nobel_data.to_csv(args.output_file, index=False)
        print(f"Data saved to {args.output_file}")
    