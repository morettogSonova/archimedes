# Imports

import pandas as pd
import country_converter as coco
import os
import matplotlib.pyplot as plt


# Data Functions

def convert_clio_to_longform(file_name):
    df = pd.read_excel(file_name)
    name = file_name.split('/')[-1].split('_')[0]
    df['Country'] = df['ccode'].apply(lambda x: coco.convert(names=x, to="ISO3"))
    df = df.drop(columns=['ccode', 'country name'])
    df_long = df.set_index('Country').stack().reset_index()
    df_long.columns = ['Country', 'Year', name]
    df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce').astype('Int64')
    return df_long

def merge_datasets(df1, df2, on=['Country', 'Year'], how='outer'):
    return pd.merge(df1, df2, on=on, how=how)

def import_files(folder):
    file_locations = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.xlsx')]
    return file_locations

# Plotting functions

def plot_metric(df, countries, metric):
    if isinstance(countries, str):
        countries = [countries]
    plt.figure(figsize=(10,6))
    for country in countries:
        data = df[(df['Country'] == country) & (metric in df.columns)]
        if data.empty:
            print(f"No data found for {country} with metric {metric}")
            continue
        plt.plot(data['Year'], data[metric], marker='o', label=country)
    plt.title(f"{metric} over time")
    plt.xlabel("Year")
    plt.ylabel(metric)
    plt.legend()
    plt.grid(True)
    
    # Set x-ticks every 50 years and rotate vertically
    years = pd.to_numeric(df['Year'], errors='coerce').dropna().astype(int).unique()
    xticks = [year for year in years if year % 100 == 0]
    plt.xticks(xticks, rotation=90)
    
    plt.show()



def main():
    # Step 0: Collect file locations
    folder = '../data/in/clio'
    file_locations = import_files(folder)


    # Step 1: Convert each file to long form
    dfs = [convert_clio_to_longform(f) for f in file_locations]

    # Step 2: Merge all DataFrames iteratively
    from functools import reduce
    merged_df = reduce(lambda left, right: merge_datasets(left, right), dfs)

    merged_df.to_csv("all_clio_data.csv", index=False)
    


if __name__ == "__main__":
    main()