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
import shutil
import time

PARQUET_FILE_PATH = 'parquet/q-repo-list_q-kdb.parquet'

GITHUB_REPOS_DIR = 'github-repos'
TARGET_DIR = 'training-set-q-language'

SLEEP_SECONDS = 5

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

df = pd.read_parquet(PARQUET_FILE_PATH)
sorted_df = df.sort_values('stargazers_count', ascending=False).reset_index(drop=True)


DESIRED_EXTENSIONS = ('.q', '.md')

def copy_desired_files(org_name, repo_name):
    """
    Copies files with desired extensions from a specified GitHub repository to a target directory.

    This function traverses the directory structure of a given repository, filters out hidden files
    and directories, and copies files with specified extensions to a target directory while preserving
    the directory structure.

    Args:
        org_name (str): The name of the GitHub organization.
        repo_name (str): The name of the GitHub repository.

    Returns:
        None
    """
    repo_path = os.path.join(GITHUB_REPOS_DIR, org_name, repo_name)
    for root, dirs, files in os.walk(repo_path):
        # `root` is the current directory
        # `dirs` holds the list of directories in the current directory
        # `files` holds the list of files in the current directory

        # Remove hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        # Remove hidden files
        files = [f for f in files if not f.startswith('.')]

        rel_path = os.path.relpath(root, GITHUB_REPOS_DIR)
        os.makedirs(os.path.join(TARGET_DIR, rel_path), exist_ok=True)

        for file in files:
            if file.endswith(DESIRED_EXTENSIONS):
                src_file = os.path.join(root, file)
                dest_file = os.path.join(TARGET_DIR, rel_path, file)
                shutil.copy(src_file, dest_file)


# Loop through the DataFrame and download the repositories
for index, row in sorted_df.iterrows():
    # Keep org_name and repo_name separate since path separator may be different on different OS.
    org_name = row['owner']['login']
    repo_name = row['name']
    logging.info(f"Processing repository {index} : {org_name}/{repo_name}...")
    copy_desired_files(org_name, repo_name)


logging.info('Done')
# -


