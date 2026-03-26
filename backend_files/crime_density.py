## ===================================================================================
## Crime rates for Lollipop chart
## ===================================================================================

import pandas as pd
from geopy.geocoders import Nominatim

def get_columns_for_crime_density_heatmap(df, theme = ["whitegrid", "viridis"]):

    """

    A function to create a heatmap of crime on a geographical map.

    Input: Dataframe with crime data.

    Output: Dataframe with necessary columns for creating a heatmap.

    """

    # Get location data
    df_locations = df[["latitude", "longitude", "category", "police_force_id"]].copy()

    # Returns dataframe
    return df_locations

def crime_density_heatmap_info(df):

    """ 

    A function to display information about crime density heatmap for the LLM.

    Input: Dataframe with crime location data.

    Output: String containing information about crime density heatmap.

    """

    # Gets descriptive statistics
    info = df.describe()

    # Returns information string
    return info

def crime_density_heatmap_info(df, lat_col="latitude", lon_col="longitude", 
                               grid_size=0.01, top_n=10):
    """
    Returns a table of top crime hotspots with reverse geocoded area names.

    Input:
        df: DataFrame with crime location data (must include lat & lon).
        lat_col: name of latitude column.
        lon_col: name of longitude column.
        grid_size: size/degrees of grid cell for density aggregation.
        top_n: number of hotspots to return.

    Output:
        DataFrame with: lat_bin, lon_bin, count, area_name.
    """

    # Validate input
    if lat_col not in df.columns or lon_col not in df.columns:
        raise ValueError("DataFrame must include latitude and longitude columns")

    # Create grid cell identifiers
    df["lat_bin"] = (df[lat_col] // grid_size) * grid_size
    df["lon_bin"] = (df[lon_col] // grid_size) * grid_size

    # Count crimes per grid cell
    hotspot_counts = (
        df.groupby(["lat_bin", "lon_bin"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    # Select top hotspots
    top_hotspots = hotspot_counts.head(top_n).copy()
    
    # Initialize geocoder
    geolocator = Nominatim(user_agent="crime_hotspot_app")

    # Add area names via reverse geocoding
    area_names = []
    for _, row in top_hotspots.iterrows():
        coord = f"{row['lat_bin']}, {row['lon_bin']}"
        try:
            location = geolocator.reverse(coord, exactly_one=True)
            if location and location.address:
                area_names.append(location.address)
            else:
                area_names.append("Unknown")
        except Exception as e:
            area_names.append("Error")
        # Optional sleep to respect rate limits
        # time.sleep(1)

    top_hotspots["area_name"] = area_names

    return top_hotspots

if __name__ == "__main__":

    print("Converting Crime data")
    df_crimes = pd.read_csv("street_data/test_crime_data.csv")

    # Get top hotspots with area names
    result = crime_density_heatmap_info(df_crimes, grid_size=0.005, top_n=5)

    # Print results
    print("\nTop 5 Crime Hotspots with Area Names:\n")
    print(result)

