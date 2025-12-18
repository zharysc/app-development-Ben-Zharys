from openai import OpenAI
from dotenv import load_dotenv
import os

## ====================================================================
## Function to get completion from LLM

## Set your OpenAI API key here
load_dotenv(dotenv_path=".env")

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY not set in .env")

#TODO: Need to set api key in environment variable OPENAI_API_KEY  -- > setx OPENAI_API_KEY "sk-xxxxxxxxxxxxxxxx"
# Do this in your terminal or command prompt

## ====================================================================

def get_completion(prompt,model="gpt-4o-mini", temperature=0):
    """
    This function takes a prompt as input and returns the response from the LLM.
    Parameters:
    prompt (str): The prompt to send to the LLM
    Returns:
    response (str): The response from the LLM
    """
    # API key setup
    load_dotenv(dotenv_path=".env")

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY not set in .env")

    # Client initialization
    client = OpenAI(api_key=api_key)

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature = temperature
    )
    return response.choices[0].message.content

def generate_chart_analysis_summary(data_fetcher, id=None, csv_data='backend_files/street_data/leicestershire_street.csv',word_limit=50,prompt_template=None):
    """
    Generates a prompt for the LLM to analyze a specific chart type based on provided data summary.
    Parameters:
    data_fetcher (function): Function gives summary data based on the csv. Returns a DataFrame.
    id (str): Optional identifier for specific data fetching
    csv_data (str): Path to the CSV data file
    Returns:
    summary (str): Generated summary from the LLM
    """
    # Fetch data summary
    df_summary = data_fetcher(id=id, csv_data=csv_data)

    # Default prompt if none provided
    if prompt_template is None:
        prompt_template = (
            "Analyze the following summary data:\n{data}\n"
            f"Provide insights and notable observations. Limit to {word_limit} words."
        )

    # Generate prompt by inserting the dataframe
    prompt = prompt_template.format(data=df_summary.to_string(index=False))

    # Call LLM to get analysis
    summary = get_completion(prompt)

    return summary

if __name__ == "__main__":
    # prompt = "Explain the theory of relativity in simple terms. 10 words."
    # response = get_completion(prompt)
    # print(response)

    # print("="*40)
    # print("generate_chart_analysis_prompt test")
    # from backend_files.pie_top_3 import get_crime_types_summary
    # summary = generate_chart_analysis_summary(data_fetcher=get_crime_types_summary, csv_data='street_data/leicestershire_street.csv', word_limit=30)
    # print(summary)

    print("="*40)
    print("Prompt test for Population")
    from population_functions import get_population_summary
    summary = generate_chart_analysis_summary(data_fetcher=get_population_summary, csv_data='data/cleaned_population.csv', word_limit=30)
    print(summary)
