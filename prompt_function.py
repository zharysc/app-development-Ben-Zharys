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
    client = OpenAI(api_key=api_key)

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature = temperature
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    prompt = "Explain the theory of relativity in simple terms. 10 words."
    response = get_completion(prompt)
    print(response)

