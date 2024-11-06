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
import logging
import pandas as pd
import os

CLONE_SLEEP_SECONDS = 150

GITHUB_REPOS_DIR = 'github-repos'
PARQUET_DIR = "parquet"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

df = pd.read_parquet(os.path.join(PARQUET_DIR, 'q-repo-list_q-kdb.parquet'))
logging.info(f"{len(df)=}")
# -

df['license'].value_counts()

# +
import os
import subprocess
import time

# Function to check if a repository is already downloaded
def check_and_download_repo(org_name, repo_name):
    """
    Check if a GitHub repository exists locally, and if not, download it.

    Args:
        org_name (str): The name of the GitHub organization or user.
        repo_name (str): The name of the repository.

    Returns:
        None

    Side Effects:
        - Creates directories if they do not exist.
        - Clones the repository from GitHub if it does not exist locally.
        - Logs information and errors during the process.

    Raises:
        subprocess.CalledProcessError: If the git clone command fails.
    """
    full_name = f'{org_name}/{repo_name}'
    repo_url = f'https://github.com/{full_name}.git'
    org_path = os.path.join(GITHUB_REPOS_DIR, org_name)
    repo_path = os.path.join(org_path, repo_name)
    if not os.path.exists(repo_path):
        os.makedirs(org_path, exist_ok=True)
        logging.info(f"Downloading repository {full_name} into {GITHUB_REPOS_DIR}...")
        try:
            subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to clone repository {full_name} from {repo_url}. Error: {e}")

        time.sleep(CLONE_SLEEP_SECONDS)

    else:
        logging.info(f"Repository {repo_name} already exists in {org_path}.")

# Loop through the DataFrame and download the repositories
for index, row in df.head(232).iterrows():
    # Keep org_name and repo_name separate since path separator may be different on different OS.
    org_name = row['owner']['login']
    repo_name = row['name']
    stars = row['stargazers_count']
    check_and_download_repo(org_name, repo_name)

# -

logging.info('Done')


