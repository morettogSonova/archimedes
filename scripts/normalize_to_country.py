import pandas as pd



def norm_value(df, country_code, column_name):
    """
    Normalize the specified column for a given country against the USA's value for that year.
    """
    # DROP duplicates based on YEAR and COUNTRYCODE
    df = df.drop_duplicates(subset=["YEAR", "COUNTRYCODE", column_name]).copy()

    df_country = (
        df[df["COUNTRYCODE"] == country_code].drop(columns=["COUNTRYCODE"]).copy()
    )
    df_country = df_country.rename(
        columns={column_name: f"{column_name}_{country_code}"}
    )

    df_temp = pd.merge(df, df_country, on="YEAR", how="left")
    df_temp[f"{column_name}_NORM"] = (
        df_temp[column_name] / df_temp[f"{column_name}_{country_code}"]
    )
    out_df = df_temp.drop(columns=[f"{column_name}_{country_code}"])

    return out_df
