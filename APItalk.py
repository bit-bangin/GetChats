"""
This module interacts with the OpenAI API to retrieve data based upon a given query.

"""

import time
import logging
import requests
from requests.exceptions import RequestException

# Configure the logging module
logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)

def apiTalk(api_key, query):
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

    while True:
        try:
            response = requests.post(url, headers = headers, json = data, timeout = 10)

            if response.status_code == 200:
                # Request was successful, return the results
                return response.json()
            elif response.status_code == 429:
                # We've encountered the rate limit, napping before trying again.
                logger.info("We have encountered the rate limit. Taking a quick nap.")
                time.sleep(60)
                continue
            else:
                # Some other error has occurred
                response.raise_for_status()
        except RequestException as e:
            # Catch any requests exceptions.
            logger.error(f"A requests exception has occurred: {e}")
            time.sleep(1)
            continue
        except Exception as e:
            # Catch any other unforeseen exceptions.
            logger.error(f"An error ocurred: {e}")
            break