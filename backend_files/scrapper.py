import requests
from bs4 import BeautifulSoup
import pandas as pd
import pycountry_convert as pc


def country_to_continent(country_name):
    """
    This function converts a country name to its corresponding continent name.
    Parameters:
    country_name (str): The name of the country.
    Returns:
    str: The name of the continent.
    """
    try:
        country_code = pc.country_name_to_country_alpha2(country_name)
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_name = pc.convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except:
        return 'Unknown'


def crime_index_countries(continent = None, num_countries = 10, ascending = False):
    """ 
    This function returns a DataFrame of countries with their Crime Index and Continent.
    It can filter by continent and limit the number of countries returned.

    Parameters:
    continent (str): The continent to filter by (e.g., 'Europe', 'Asia'). If None, no filtering is applied.
    num_countries (int): The number of countries to return.
    ascending (bool): Whether to sort the Crime Index in ascending order.

    Returns:
    pd.DataFrame: A DataFrame with columns 'Country', 'Crime Index', and 'Continent'.
    """

    # === Scrapping from the web page ===============================================
    url = "https://www.numbeo.com/crime/rankings_current.jsp"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', {'id': 't2'})
    headers = [th.text.strip() for th in table.find_all('th')]

    rows = []
    for tr in table.find_all('tr')[1:]:  # skip header row
        cells = [td.text.strip() for td in tr.find_all('td')]
        if cells:
            rows.append(cells)

    # === Converting to DataFrame ===================================================
    df = pd.DataFrame(rows, columns=headers)
    df['Country'] = df['City'].apply(lambda x: x.split(',')[-1].strip())

    # === Determining continent =====================================================
    df['Continent'] = df['Country'].apply(country_to_continent)

    # === Filtering and sorting =====================================================
    if continent:
        df = df[df['Continent'] == continent]
    df['Crime Index'] = pd.to_numeric(df['Crime Index'], errors='coerce')
    df = df.sort_values(by='Crime Index', ascending=ascending).head(num_countries)   
    
    return df[['City', 'Crime Index']]


## Scrapping info -  breakdown of crime index
# TODO: Implement this function
def crime_index_breakdown(country_name):
    """
    This function scrapes the crime index.
    
    Parameters:
    country_name (str): The name of the country.
    
    Returns:
    pd.DataFrame: A DataFrame with crime categories and their respective indices.
    """
    url = "https://www.numbeo.com/crime/indices_explained.jsp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    