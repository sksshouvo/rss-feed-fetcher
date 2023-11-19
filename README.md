# RssFeedFetcher

A simple CLI system for fetch feed from a Rss feed.

# Requirements

- Python 3.10
- python3-tk
- virtualenv or your favourite Python environment tool

# Get Started

- Clone the repository
```sh
git clone git@github.com:sksshouvo/rssFeedFetcher.git
```
- Checkout the develop branch

```sh
git checkout develop
```
- Install Python and create or use a Python Environment with Python Version listed in requirements
```sh
python3.10 -m venv env
```
- Activate Python3.10 environment
```sh
source env/bin/activate
```
- Install the local requirements
```sh
pip install -r requirements.txt
```
- Run
```sh
python main.pyw
```

# Branching Model

We use a branching model similar to this site (https://nvie.com/posts/a-successful-git-branching-model/).
When you work on a new task, please create a feature-branch ( **feature/RFF-14-Feature-Title** ) from the ( **develop** ) branch.
To publish any changes instead of direct push, create a **PR** to **develop** 

- feature/RFF-###-Title
- develop
- release-#.#.#
- hotfix-#.#.#
- main


## NOTE : WE BELIEVE IN MAINTAINING STANDARD. 

SO DON'T FORGET TO RUN AT LEAST ```flake8``` AND ```isort``` IN CHANGED FILE BEFORE ANY NEW COMMIT AND PULL REQUEST


# Copyright

Copyright (c) 2023 sksshouvo inc. All rights reserved.
