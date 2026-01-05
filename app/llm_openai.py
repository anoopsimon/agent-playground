import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key here or via the OPENAI_API_KEY environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def query_openai(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Send a prompt to OpenAI's chat completion API and return the response.
    Compatible with openai>=1.0.0
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
