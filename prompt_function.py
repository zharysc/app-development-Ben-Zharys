from openai import OpenAI
import os

## ====================================================================
## Function to get completion from LLM

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

    api_key = os.getenv("OPENAI_API_KEY")

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

