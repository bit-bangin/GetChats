"""
This module interacts with the OpenAI API to retrieve data based upon a given query.

"""
import os
import time
import random
import logging
import requests
from requests.exceptions import RequestException

# Configure the logging module
logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)


def api_Talk(api_key, query):
    """
    Sends a POST request to the OpenAI API with the given query, using the provided API key for authentication. 

    Handles rate limits by sleeping for 60 seconds upon receipt of a 429 status code - then retries request.

    Arguments
        api_key (str): The API key for authentication.
        query (str): The query to send to the OpenAI API.

    Returns:
        dict: Data returned by the API, parsed from JSON into a dictionary.

    Raises:
        HTTPError: If response w/error status code received. 
    """
    url = "https://api.openai.com/v1/engines/davinci-codex/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "prompt": query,
        "max_tokens": 60
    }

    base_delay = 1 # Base delay in seconds
    max_delay = 60 # Maximum delay in seconds

    delay = base_delay

    while True:
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)

            if response.status_code == 200:
                # Request was successful, return the results
                return response.json()
            elif response.status_code == 429:
                # Use Retry-After header if available, otherwise use exponential backoff algorithm
                retry_after = int(response.headers.get("Retry-After", delay))
                logger.info(
                    "We have encountered the rate limit. Taking a quick nap.")
                time.sleep(retry_after)
                delay = min(2 * delay, max_delay) # Prepare for next possible delay. 
                continue
            else:
                # Some other error has occurred
                response.raise_for_status()
        except RequestException as e:
            # Catch any requests exceptions
            logger.error(f"A requests exception has occurred: {e}")
            jitter = random.uniform(0.5, 1.5) # Jitter to disperse requests
            time.sleep(delay * jitter) # Double the delay for next iteration. 
            continue
        except Exception as e:
            # Catch any other unforeseen exceptions.
            logger.error(f"An error ocurred: {e}")
            break


# Fetch API key from environment variable.
if __name__ == "__main__":
    api_key = os.getenv("OpenAI_API_Key")

    if api_key is None:
        logger.error(
            "API key not found. Set the OpenAI_API_Key environment variable.")
    else:
        result = api_Talk(api_key, "your-query-here")
        print(result)
