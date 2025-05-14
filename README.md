
# Description

This program allows users to easily determine how good companies are to work at based on their specific criteria (compensation, work life balance, etc.). The program takes as input a list of companies, fetches company data from Blind website, categorizes companies into tiers based on criteria provided, and then outputs data requested into a csv file. 

# Instructions

- Create required files and set fields below according to your preferences
- See example files and my files for reference
- Run scraper.py
- View results in output file

## Main File - blind_scraper.py

- CONFIG_FILE_PATH
  - set path to config file
  - file is required to exist beforehand
- import calculate_tier
  - set import to python file containing calculate_tier function
  - file is required to exist beforehand

## Config File - config.json

- INPUT_FILE_PATH
  - set path to input file
  - file is required to exist beforehand
- OUTPUT_FILE_PATH
  - set path to output file
  - file is automatically created
- DATABASE_FILE_PATH
  - set path to database file
  - file is automatically created
- OUTPUT_FILE_HEADERS
  - set fields you want in output file to true, and those you don't want to false
- TIME_DELAY
  - set time delay (seconds) between web requests
- MAX_REQUESTS
  - set maximum number of web requests to send in a single run
- MAX_AGE
  - set maximum age (days) of data in database before it is considered stale
- HTTP_HEADERS
  - set HTTP headers to allow access to website via python
  - you do not need to modify this

# Tier Calculator File - tier_calculator.py

- create a function named calculate_tier that takes as input company_data and outputs a tier based on your criteria
- see blind_scraper.py -> get_company_data_from_blind() or example_config.json -> OUTPUT_FILE_HEADERS for a list of fields in company_data
