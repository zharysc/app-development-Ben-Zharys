import pandas as pd
## ===================================================================================
## Population data
## ===================================================================================

def get_population_summary(id = None, csv_data = None):
    """
    This is a bridging function. Population is already in the 
    format required. But to have it be able to be called in the same
    way as the other graphs we have this function

    """ 
    if id is None:
        df = pd.read_csv(csv_data)

    return df

if __name__ == "__main__":
    # Test data table for pie chart
    df_summary = get_population_summary(csv_data='data/cleaned_population.csv')
    print(df_summary)
    print(df_summary.columns)

    # # Prompt test for Population
    # from prompt_function import generate_chart_analysis_summary
    # summary = generate_chart_analysis_summary(data_fetcher=get_population_summary, csv_data='data/cleaned_population.csv', word_limit=30)
    # print(summary)
