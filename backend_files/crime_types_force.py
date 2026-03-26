## ===================================================================================
## Crime rates for Lollipop chart
## ===================================================================================
import pandas as pd

def add_crime_rate_column(df):

    """

    A function to calculate crime rate by region.

    Input: Dataframe with necessary columns for calculating crime rate by region.

    Output: Dataframe with crime rate by region.

    """

    

    # Calculates crime rate per 1,000 people
    df["crime_rate_per_1000"] = (df["crime_count"] / df["population"]) * 1000

    # Returns dataframe
    return df


def get_columns_for_heatmap_table(df_crimes = pd.read_csv("backend_files/street_data/test_crime_data.csv"),
                                          df_population = pd.read_csv("backend_files/data/cleaned_population.csv") ,
                                            df_forces = pd.read_csv("backend_files/data/forces.csv")):

    """

    A function to get the necessary columns for creating a heatmap.

    Input: Crime dataframe. Population dataframe. Police forces dataframe.

    Output: Dataframe with necessary columns for creating a heatmap.

    """
    

    # Groups crimes by police force and category and counts number of crimes
    df_crime_counts = df_crimes.groupby(["police_force_id", "category"]).size().reset_index(name="crime_count")

    # Merges crime counts with population data
    df_merged_1 = pd.merge(df_crime_counts, df_population, on="police_force_id", how="left")

    # Merges crime counts and population data with police forces data
    df_merged_2 = pd.merge(df_merged_1, df_forces, on="police_force_id", how="left")

    # Adds crime rate column
    df_merged_2 = add_crime_rate_column(df_merged_2)

    

    # Selects necessary columns
    df_result = df_merged_2[["police_force_name", "category", "crime_count", "population"]]

    # Adds crime rate column
    df_result = add_crime_rate_column(df_result)
    
    # Removes less overpowering categories
    df_result = df_result[~df_result["category"].isin(["violent-crime", "anti-social-behaviour"])]

    # Formats category names
    df_result["category"] = (df_result["category"].str.replace("-", " ").str.title())

    # Returns dataframe
    return df_result

def type_against_region_heatmap_info(id = None, csv_data = None):

    """ 

    A function to display information about crime categories by police force for the LLM.

    Input: Dataframe with crime categories by police force.

    Output: String containing information about crime categories by police force.

    """
    if id is None:
        df_heatmap = get_columns_for_heatmap_table()

    # Returns information string
    return df_heatmap

if __name__ == "__main__":
    print("Converting Crime data")
    df_crimes = pd.read_csv("street_data/test_crime_data.csv")

    print("Converting population data")
    df_population = pd.read_csv("data/cleaned_population.csv")
    print(df_population.dtypes)
    print(df_population.head())

    print("Getting forces")
    df_forces = pd.read_csv("data/forces.csv")

    df_heatmap = get_columns_for_heatmap_table(df_crimes, df_population, df_forces)
    print(type_against_region_heatmap_info(df_heatmap))
