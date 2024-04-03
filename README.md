# Task Tracker
CCT211 Project 2

## Description:
A simple GUI for organizing tasks


## Technologies Used
* Python
* TKinter


## Setup
First, install all dependencies by running `pip install -r requirements.txt`

To setup local DB:
* Run the `python init_db`. All data will be stored in the `task_db.sqlite` file which will be created in the `src/` directory.

To setup the pre-commit hook (for contribution purposes):
* Run `pre-commit install`. On every commit, this will enforce PEP8 style guidelines.
