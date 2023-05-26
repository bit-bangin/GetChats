import time
import requests
from requests.exceptions import Timeout

def apiTalk(api_key, query):
    """
    Function to 
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
                # Request was successful, return results
                return response.json()
            elif response.status_code == 429:
                # We have hit the rate limit, sleep then try again
                time.sleep(60)
                continue
            else:
                # Some other error has occurred
                response.raise_for_status()
        except Timeout:
            print("Request has timed out, sleeping for a time - then trying again.")
            time.sleep(1)
            continue
        except Exception as e:
            print(f"An error ocurred: {e}")
            break