import pandas as pd
## ===================================================================================
## Pie chart of top 3 crime types
#TODO: Function to plot pie chart
#TODO: Function to send prompt to LLM to generate analysis of the pie chart
## ===================================================================================

#TODO: Function to take neighbourhood id, calculate percentages of top 3 crime types
def get_crime_types_summary(id = None, csv_data = None):
    """
    Given neighbourhood id, return the proportions of top 3 crime types in that neighbourhood,
    and group the rest under 'Other'.
    Parameters:
    id (int): neighbourhood id
    Returns:
    df (DataFrame): DataFrame with top 3 crime types and their percentages 
    """

    if id is None: # Means that we are working with csv data instead of API
        df = pd.read_csv(csv_data)

        # Group by count of category
        df_grouped = df['category'].value_counts().reset_index()
        df_grouped.columns = ['category', 'count']

        # Getting top 3 crimes
        top_3 = df_grouped.nlargest(3, 'count')

        # Calculating 'Other' category
        others = df_grouped.iloc[3:]
        others_count = others['count'].sum()

        # Create new row for 'Other'
        other_row = pd.DataFrame({'category': ['Other'], 'count': [others_count]})

        # Combine top 3 with 'Other'
        result = pd.concat([top_3, other_row], ignore_index=True)

        # Adding percentage column
        result['percentage'] = (result['count'] / result['count'].sum()) * 100



        return result
    

if __name__ == "__main__":
    # Test data table for pie chart
    df_summary = get_crime_types_summary(csv_data='backend_files/street_data/leicestershire_street.csv')
    print(df_summary)
