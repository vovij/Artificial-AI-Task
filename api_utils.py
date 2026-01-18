import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("BASE_URL")

if not API_KEY or not BASE_URL:
    raise ValueError("Missing required environment variables. Please check your .env file.")

def get_ai_response(ai_context, timeout=60):
    """Send request to AI API and return raw JSON response"""

    response = requests.post(
        BASE_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY
        },
        json={
            "model": "gpt-5-mini-2025-08-07",
            "input": ai_context # full conversation context in the required format
        },
        timeout=timeout
    )
    response.raise_for_status() # raise HTTPError for bad status codes
    
    return response.json()


def format_output_response(input_json):
    """Extract text content from API response JSON"""

    output_text = []
    for item in input_json["output"]:
        if item["type"] == "message":
            for block in item["content"]:
                if block["type"] == "output_text":
                    output_text.append(block["text"])

    return "".join(output_text)