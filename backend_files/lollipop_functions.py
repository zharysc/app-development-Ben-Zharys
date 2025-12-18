import pandas as pd
## ===================================================================================
## Crime rates for Lollipop chart
## ===================================================================================
print("Imports done")
def add_crime_rate_column(df):

    """

    A function to calculate crime rate by region.

    Input: Dataframe with necessary columns for calculating crime rate by region.

    Output: Dataframe with crime rate by region.

    """
    # Calculates crime rate per 1,000 people
    df["crime_rate_per_1000"] = (df["crime_count"] / df["population"]) * 1000

    # Returns dataframe
    print("Done")

    return df



def get_columns_for_crime_rate_by_region(df_crimes = pd.read_csv("backend_files/street_data/test_crime_data.csv"),
                                          df_population = pd.read_csv("backend_files/data/cleaned_population.csv") ,
                                            df_forces = pd.read_csv("backend_files/data/forces.csv")):

    """

    A function to get the necessary columns for calculating crime rate by region.

    Input: Crime dataframe. Population dataframe. Police forces dataframe.

    Output: Dataframe with necessary columns for calculating crime rate by region.

    """
    print("get_columns_for_crime_rate_by_region")

    # Groups crimes by region and counts number of crimes
    df_crime_counts = df_crimes.groupby("police_force_id").size().reset_index(name="crime_count")

    # Merges crime counts with population data
    df_merged_1 = pd.merge(df_crime_counts, df_population, on="police_force_id", how="left")

    # Merges crime counts and population data with police forces data
    df_merged_2 = pd.merge(df_merged_1, df_forces, on="police_force_id", how="left")

    # Selects necessary columns
    df_result = df_merged_2[["police_force_name", "crime_count", "population"]]

    # Adds crime rate column
    df_result = add_crime_rate_column(df_result)

    # Returns dataframe
    print("Done")
    return df_result

def crime_rate_by_region_info(id = None, csv_data = None):

    """ 

    A function to display information about crime rate by region for the LLM.

    Input: Dataframe with crime rate by region.

    Output: String containing information about crime rate by region.

    """

    if id is None: # Means that we are working with csv data instead of API
        df_crime_rate = get_columns_for_crime_rate_by_region()

    return df_crime_rate

if __name__ == "__main__":
    print("Converting Crime data")
    df_crimes = pd.read_csv("street_data/test_crime_data.csv")

    print("Converting population data")
    df_population = pd.read_csv("data/cleaned_population.csv")
    print(df_population.dtypes)
    print(df_population.head())

    print("Getting forces")
    df_forces = pd.read_csv("data/forces.csv")

    df_crime_rate = get_columns_for_crime_rate_by_region(df_crimes, df_population, df_forces)
    print(crime_rate_by_region_info(df_crime_rate))
    print(f"Columns: {df_crime_rate.dtypes}")