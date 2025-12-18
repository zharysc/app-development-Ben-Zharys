#Import Libraries
import requests
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.ops import triangulate
from shapely.geometry import Polygon
import mapbox_earcut as earcut
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

## ==============================================================================================================
## Get Police Force Table from API
## ==============================================================================================================

def get_forces():

    """ 
    
    Defines the function to call the API and retrieve the police forces data table.
    
    Input: None.
    
    Output: Dataframe containing all the police forece ids and names.
    
    """

    # Defines the connection to the API
    url = "https://data.police.uk/api/forces"
    response = requests.get(url)

    # Raises exception if connection fails
    if response.status_code != 200:                                 
        raise Exception(f"API error: {response.status_code}")           
    
    # Converts responce to json
    data = response.json()

    # Converts json to dataframe
    df = pd.DataFrame(data)

    # Rename ID and name columns
    df.rename(columns={"id": "police_force_id", "name": "police_force_name"}, inplace=True)

    # Returns dataframe
    return df


## ==============================================================================================================
## Get Neighbourhood Table from API
## ==============================================================================================================


def get_neighbourhood(id):

    """

    Defines the function to call the API and retrieve the neighbourhood data table.

    Input: Police force ID.

    Output: Dataframe containing the neighbouthood id, name and which police force id it belongs to.

    """

    # Defines the connection to the API
    url = f"https://data.police.uk/api/{id}/neighbourhoods"     # Defines the API url 
    response = requests.get(url)                                # Defines the responce after we 'get' the url
    
    # Raises exception if connection fails
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    # Converts responce to json 
    data = response.json()

    # Converts json to dataframe
    df = pd.DataFrame(data)

    # Adds police force ID
    df['police_force_id'] = id

    # Renames the ID and name columns
    df.rename(columns={"id": "neighbourhood_id", "name": "neighbourhood_name"}, inplace=True)

    # Returns dataframe
    return df


def get_all_neighbourhoods(police_forces):

    """

    Defines the function to get all neighbourhoods for a list of police forces.

    Input: List of police force IDs.

    Output: Dataframe containing all neighbourhoods for the given police forces.

    """

    # Empty list of neighbourhood dataframes 
    df_neighbourhoods_list =[]

    # Appends each neighbourhood dataframe to the list
    for id in police_forces:
        df_neighbourhoods_list.append(get_neighbourhood(id))

    # Unions the list of dataframes into one
    df_neighbourhoods = pd.concat(df_neighbourhoods_list)

    # Returns dataframe
    return df_neighbourhoods

## ==============================================================================================================
## Get Street-Level Crimes from API
## ==============================================================================================================

def get_kml(neighbourhood_id): 
    
    """

    Defines the function to call the API and retrieve the neighbourhood KML file.

    Input: Neighbourhood ID.

    Output: Corresponding KML file content.
    
    """

    # Get pathfile from neighbourhood ID
    return f"data/{neighbourhood_id}.kml"



def get_street_level_crimes(poly_str):

    """
    
    Defines the function to call the API and retrieve the neighbourhood boundaries data table.

    Input: A polygon string defining the area to get street-level crimes for.

    Output: Street-level crime dataframe for the neighbourhood.

    """

    # Defines the connection to the API
    url = f"https://data.police.uk/api/crimes-street/all-crime?poly={poly_str}"
    response = requests.get(url)
    
    # Raises exception if connection fails
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    # Convert responce to json
    data = response.json()

    # Converts json to dataframe
    df = pd.DataFrame(data)

    # Returns dataframe
    return df

def load_polygon_from_kml(filepath):

    """

    A function to load a polygon from a KML file.

    Input: Filepath to the KML file.

    Output: Shapely polygon object.

    """

    # Loads KML file using geopandas
    gdf = gpd.read_file(filepath, driver="LIBKML")

    # Many KMLs contain a single feature
    polygon = gdf.geometry.iloc[0]

    # Returns polygon
    return polygon

def triangulate_polygon(polygon):

    """

    A function to triangulate a polygon into smaller triangles.

    Input: Shapely polygon object.

    Output: List of Shapely triangle objects.

    """

    # Triangulates polygon
    triangles = triangulate(polygon)

    # Keeps only triangles fully inside the polygon
    triangles = [t for t in triangles if polygon.contains(t.centroid)]

    # Returns list of triangles
    return triangles

def triangle_to_poly_string(triangle):
    
    """

    A function to convert a triangle to a polygon string.

    Input: Shapely triangle object.

    Output: Polygon string.

    """

    # Gets triangle coordinates
    coords = list(triangle.exterior.coords)[:-1]  # remove repeated closing point

    # convert (lng, lat) → (lat, lng)
    return ":".join(
        f"{coord[1]},{coord[0]}"
        for coord in coords
    )


def simplify_polygon(polygon, tolerance=0.0005):

    """

    Reduce polygon complexity while preserving shape.
    Tolerance ≈ 50m at UK latitudes.

    Input: Shapely polygon object, tolerance value.

    Output: Simplified Shapely polygon object.

    """

    # Simplifies polygon
    return polygon.simplify(tolerance, preserve_topology=True)

def process_kml_file_to_dataframe(police_force_id):

    """

    A function to process a KML file and retrieve street-level crime data for the area.

    Input: Filepath to the KML file.

    Output: Street-level crime dataframe for the area.

    """

    # Get KML filepath
    kml_path = get_kml(police_force_id)

    # Loads polygon
    polygon = load_polygon_from_kml(kml_path)

    # Simplifies polygon
    polygon = simplify_polygon(polygon)

    # Triangulates polygon
    triangles = triangulate_polygon(polygon)

    # Initialises a list to collect each triangle's dataframe
    all_dfs = []

    # Gets dataframa for each triangle
    for tri in triangles:
        
        # Converts the triangles to lists of coordiante strings
        poly_str = triangle_to_poly_string(tri)

        # Calls the API and gets the dataframe
        df = get_street_level_crimes(poly_str)

        # Combine dataframes
        all_dfs.append(df)

    # Checks that data has been collected, returns blank dataframe if no data is collected
    if len(all_dfs) == 0:
        return pd.DataFrame()

    # Combines all dataframes
    final_df = pd.concat(all_dfs, ignore_index=True)

    final_df["police_force_id"] = police_force_id

    # Returns combined dataframe
    return final_df

def get_crime_for_all_regions(police_forces):

    """ 

    A function to process KML files for all police forces and retrieve street-level crime data.

    Input: List of police force IDs.

    Output: Combined street-level crime dataframe for all police forces.

    """

    # Initialises a list to collect each police force's dataframe
    all_dfs = []

    # Gets dataframe for each police force
    for police_force_id in police_forces:
        df_crimes = process_kml_file_to_dataframe(police_force_id)

        # Add dataframe to list
        all_dfs.append(df_crimes)

    # Combines all dataframes
    final_df = pd.concat(all_dfs, ignore_index=True)

    # Returns combined dataframe
    return final_df

## ===============================================================================================================
## Get Specific Neighbourhood Table
## ===============================================================================================================
def get_specific_neighbourhood(police_force_id, neighbourhood_id):

    """

    A function to get data for a specific neighbourhood.

    Input: Police force ID. Neighbourhood ID.

    Output: Dataframe containing all data for the specific neighbourhood.


    """

    # Defines the connection to the API
    url = f"https://data.police.uk/api/{police_force_id}/{neighbourhood_id}"
    response = requests.get(url)
    
    # Raises exception if connection fails
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    # Convert responce to json
    data = response.json()

    # Converts json to dataframe
    df = pd.json_normalize(data)

    # Returns dataframe
    return df
    
    
def get_specific_neighnourhoods_from_police_force(police_force_id, df_neighbourhoods):

    """

    A function to get all specific neighbourhoods for a police force ID.

    Input: Police force ID. Neighbourhoods dataframe.

    Output: Dataframe containing all neighbourhoods for the specific police force ID.

    """

    # Initiates empty list to collect dataframes
    specific_neighbourhood_list = []

    # Loops through all neighbourhood ID's for the specific police force ID
    for neighbourhood_id in df_neighbourhoods["neighbourhood_id"][df_neighbourhoods["police_force_id"] == police_force_id]:

        # Calls the API and gets the dataframe
        df = get_specific_neighbourhood(police_force_id, neighbourhood_id)

        # Appends dataframe to the list
        specific_neighbourhood_list.append(df)

    # Unions the list of dataframes into one
    df = pd.concat(specific_neighbourhood_list, ignore_index=True)

    # Adds police force ID column
    df["police_force_id"] = police_force_id

    # Returns datatframe
    return df

## ==============================================================================================================
## Cleaning
## ==============================================================================================================

# == Null Filling Functions ==
def fill_blank_outcome_status(df):

    """

    A function to fill blank outcome status values with 'Unknown'.

    Input: Crime dataframe.

    Output: Crime dataframe with filled outcome status values.

    """

    # Fills nulls in the outcome column with 'Unknown'
    df["outcome_status"] = df["outcome_status"].fillna("Unknown")

    # Returns dataframe
    return df

# == Duplicate Removal Functions ==

def remove_duplicates(df):
    if "id" in df.columns:
        return df.drop_duplicates(subset=["id"]).reset_index(drop=True)

    subset = [c for c in ["latitude", "longitude", "month", "category"] if c in df.columns]
    return df.drop_duplicates(subset=subset).reset_index(drop=True)


# == Seperate Columns Extraction Functions ==
def extract_coordinates_and_street(df):

    """

    A function to extract latitude, longitude and street name from the location column.

    Input: Crime dataframe.

    Output: Crime dataframe with new latitude, longitude and street name columns.

    """

    # Extracts coordinates and street name from location column
    coords = pd.json_normalize(df["location"])
    df["latitude"] = pd.to_numeric(coords["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(coords["longitude"], errors="coerce")
    df["street_name"] = coords["street.name"]
    df.drop(columns=["location"], inplace=True)
    
    # Returns dataframe
    return df

def extract_date_components(df):

    """

    A function to extract year and month from the month column.

    Input: Crime dataframe.

    Output: Crime dataframe with new year and month columns.

    """

    # Converts month column to datetime format
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m")

    # Extracts year and month from month column
    df["year"] = df["month"].dt.year
    df["month"] = df["month"].dt.month

    # Returns dataframe
    return df

## == Main Cleaning Functions ==
def clean_population(pop):

    """

    A function to clean the population column.

    Input: Population.

    Output: Cleaned population.

    """

    # Removes m from population values
    pop = pop.replace("m", "")

    # Converts population to a float
    pop = float(pop)

    # Changes decimal to millions
    pop = pop * 1000000

    # Returns cleaned population
    return int(pop)


def clean_population_df(df_population):

    """

    A function to clean the population dataframe.

    Input: Population dataframe.

    Output: Cleaned population dataframe.

    """

    # Cleans population column
    df_population["population"] = df_population["population"].apply(clean_population)

    # Returns cleaned dataframe
    return df_population

def cleaning(df):

    """

    A function to clean the crime dataframe.

    Input: Crime dataframe.

    Output: Cleaned crime dataframe.

    """

    # Fills blank outcome status values
    df = fill_blank_outcome_status(df)

    # Removes duplicate rows
    df = remove_duplicates(df)

    # Extracts latitude, longitude and street name
    df = extract_coordinates_and_street(df)

    # Extracts year and month from month column
    df = extract_date_components(df)

    # Returns cleaned dataframe
    return df


# == Testing area for backend functions ==
if __name__ == "__main__":
    # Example: Get forces
    forces_df = get_forces()
    forces_df.to_csv("forces.csv")
    print("Police Forces:")
    print(forces_df.head())
# Cleaned population csv
df_population = clean_population_df(pd.read_csv("data/population_data.csv"))
df_population.to_csv("cleaned_population.csv",index=False)
# ## ==== Defining Police Forces List for Testing ====
# police_forces = ["bedfordshire", "hertfordshire", "thames-valley"]

# # == Get Crime frame for all regions ==
# df_crimes = get_crime_for_all_regions(police_forces)
# df_crimes = cleaning(df_crimes)
# print("Crime Dataframe:")
# print(df_crimes.head())
# # Save df_crimes to CSV
# df_crimes.to_csv("test_crime_data.csv", index=False)    

