import requests
import json
import logging
import os

# Define the API URL for Ollama
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434/api/generate")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "your_ollama_api_key")
def generate_health_recommendations(patient_name, blood_test_results):
    headers = {
        "Content-Type": "application/json"
    }

    # Construct the prompt for generating recommendations
    prompt = f"Patient {patient_name} has the following blood test results: {blood_test_results}. Based on this data, please provide detailed health recommendations including lifestyle changes, dietary suggestions, and any potential follow-up actions they should take to improve their overall health."

    data = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

        response_data = response.json()
        actual_response = response_data.get("response", "No recommendations available.")
        return actual_response

    except requests.exceptions.RequestException as e:
        logging.error(f"Request to Ollama API failed: {e}")
        return f"Error: {e}"

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return f"Error: {e}"
