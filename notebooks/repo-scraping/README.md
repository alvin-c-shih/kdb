# Fine-Tuning LLMs on Q Code for Better Completions

## Introduction

This repository contains a collection of Jupyter notebooks designed to
collect q code and Markdown documentation from a variety of open source
repositories. The goal is to test whether naive fine tuning of an LLM
will allow it to be more useful for code completion tasks.

## Contents

- `00_q-repo-list.ipynb`
  - Query for repos which have `language:q` or `topic:q` and are permissively licensed.
- `10_fetch-repos.ipynb`
  - Clone repos into a staging area.
- `20_combine-repos.ipynb`
  - Copy files of interest into a target directory.
  - Ignore hidden directories like `.git`.
  - Seeking files with extensions: `.q`, `.md`

## Directories Created

- `parquet/`
  - Parquet files holding information about relevant repos.
  
- `github-repos/`
  - Repositories checked out from GitHub.

- `training-set-q-language/`
  - Copy of only the `.q` and `.md` files.

