#Import Libraries
import requests
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.ops import triangulate
from shapely.geometry import Polygon
import mapbox_earcut as earcut
from pathlib import Path

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

def get_neighbourhood_boundaries(neighbourhood_id, police_force_ids):

    """

    Defines the function to call the API and retrieve the neighbourhood boundaries data table.

    Input: Neighbourhood ID.

    Output: Corresponding boundary polygon string.
    
    """

    #TODO: Change made here - creation of neighbourhoods dataframe within the function
    df_neighbourhoods_list =[]
    for id in police_force_ids:
        df_neighbourhoods_list.append(get_neighbourhood(id))
    df_neighbourhoods = pd.concat(df_neighbourhoods_list)

    # Finds the input's corresponding police force ID 
    police_force_id = df_neighbourhoods.loc[df_neighbourhoods["neighbourhood_id"] == neighbourhood_id, "police_force_id"].iloc[0]

    # Defines the connection to the API
    url = f"https://data.police.uk/api/{police_force_id}/{neighbourhood_id}/boundary"
    response = requests.get(url)
    
    # Raises exception if connection fails
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
    
    # Convert responce to json
    data = response.json()

    # Convert to polygon string format
    polygon_str = ":".join(
        f"{float(item['latitude'])},{float(item['longitude'])}"
        for item in data
    )

    # Returns polygon
    return polygon_str

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

def process_kml_file_to_dataframe(neighbourhood_id):

    """

    A function to process a KML file and retrieve street-level crime data for the area.

    Input: Filepath to the KML file.

    Output: Street-level crime dataframe for the area.

    """

    # Get KML filepath
    kml_path = get_kml(neighbourhood_id)

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

    # Returns combined dataframe
    return final_df

## ==============================================================================================================
## Cleaning
## ==============================================================================================================
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

def remove_duplicates(df):
    if "id" in df.columns:
        return df.drop_duplicates(subset=["id"]).reset_index(drop=True)

    subset = [c for c in ["latitude", "longitude", "month", "category"] if c in df.columns]
    return df.drop_duplicates(subset=subset).reset_index(drop=True)

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
    print("Police Forces:")
    print(forces_df.head())

    # Example: Get neighbourhoods for a specific force
    neighbourhoods_df = get_neighbourhood("leicestershire")
    print("\nNeighbourhoods in Leicestershire:")
    print(neighbourhoods_df.head())

    # Example: Get neighbourhood boundaries
    boundary_str = get_neighbourhood_boundaries("NC04", ["leicestershire"])
    print("\nBoundary String for NC04:")
    print(boundary_str)

    # Example: Process KML file to get street-level crimes
    crimes_df = process_kml_file_to_dataframe("leicestershire")
    print("\nStreet-level Crimes in Leicestershire:")
    print(crimes_df.head())

    # crimes_df.to_csv(
    # "raw_leicestershire_street_level_crimes.csv",
    # index=False
    # )

    ## Example: Clean the crimes dataframe
    cleaned_crimes_df = cleaning(crimes_df)
    print("\nCleaned Street-level Crimes in Leicestershire:")
    print(cleaned_crimes_df.head())
    cleaned_crimes_df.to_csv(
    "leicestershire_street.csv",
    index=False
    )

