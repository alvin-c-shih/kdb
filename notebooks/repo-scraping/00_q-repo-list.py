# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.1
#   kernelspec:
#     display_name: almanac-2024-04
#     language: python
#     name: python3
# ---

# +
import requests
import logging
import time
import os
import pandas as pd
from typing import Optional
from dotenv import load_dotenv

PARQUET_DIR = "parquet"

# Define the base URL and search parameters
BASE_URL = "https://api.github.com/search/repositories"
LICENSE_QUERY = "license:apache-2.0 license:mit license:0bsd license:cc"
SLEEP_SECONDS = 5

# Bring in .env file in case it has the proxy settings.
load_dotenv()

# Ensure the output directory exists
os.makedirs(PARQUET_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_github_query(query: str) -> pd.DataFrame:
    """
    Executes a GitHub search query to fetch repositories based on the provided query string.

    Args:
        query (str): The search query string to be used for fetching repositories from GitHub.

    Returns:
        pd.DataFrame: A DataFrame containing the details of the repositories fetched from GitHub.

    Note:
        - The function uses the `requests` library to make HTTP requests to the GitHub API.
        - The function uses the `logging` library to log information and errors.
        - The function assumes the existence of constants `BASE_URL` and `SLEEP_SECONDS` for the GitHub API base URL and sleep duration between requests, respectively.
    """

    results = []

    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 100,  # Number of results per page
        "page": 1  # Start from the first page
    }

    while True:
        logging.info(f"Fetching page {params['page']}")
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            logging.error(f"Failed to fetch data: {response.status_code}")
            break

        data = response.json()
        results.extend(data.get("items", []))
        logging.info(f"Fetched {len(data.get('items', []))} repositories")

        # Check if there is a next page
        if "next" in response.links:
            params["page"] += 1
            time.sleep(SLEEP_SECONDS)
        else:
            logging.info("No more pages to fetch")
            break

    # Process the collected results
    logging.info(f"Total repositories found: {len(results)}")

    return pd.DataFrame(results)


def run_and_save_query(parquet_suffix:str, github_query: str, license_query: str = ''
        ) -> Optional[pd.DataFrame]:
    """
    Runs a GitHub query, saves the result as a Parquet file, and returns the DataFrame.

    Args:
        parquet_suffix (str): Suffix to append to the output Parquet file name.
        github_query (str): The GitHub query string to run.
        license_query (str): The license query string to append to the GitHub query.

    Returns:
        Optional[pd.DataFrame]: The resulting DataFrame from the GitHub query, or None if an error occurs.
    """

    query = f"{github_query} {license_query}"
    logging.info(f"Running query: {query}")

    df = run_github_query(query)

    output_path = os.path.join(PARQUET_DIR, f"q-repo-list_{parquet_suffix}.parquet")
    df.to_parquet(output_path, index=False)


run_and_save_query('q-kdb', 'topic:q topic:kdb', LICENSE_QUERY)

# -


