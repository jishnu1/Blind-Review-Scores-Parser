import csv
import json
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

# CONFIGURATION (MODIFY THESE)

# Paths to input, output, and database files
INPUT_FILE_PATH    = "input/input_5.txt"
OUTPUT_FILE_PATH   = "output/output_5.csv"
DATABASE_FILE_PATH = "database/database.json"

# Set fields you want in the output file to True, and those you don't want to False
# The fields in the output file will be in the same order as they are in this dictionary
OUTPUT_FILE_HEADERS = {
    # general
    "company_name": True,
    "url":          True,
    # overview
    "website":   False,
    "industry":  True,
    "locations": True,
    "founded":   False,
    "size":      True,
    "salary":    False,
    # reviews
    "overall":               True,
    "career_growth":         True,
    "work_life_balance":     True,
    "compensation_benefits": True,
    "company_culture":       True,
    "management":            True,
    # compensation"
    "median_total_compensation": True,
    "25th_percentile": False,
    "70th_percentile": False,
    "90th_percentile": False,
    # other
    "last_updated":    True
}

# Set the time delay (seconds) between requests to avoid overwhelming the server
TIME_DELAY = 1

# Set the maximum age (days) of the data in the database before it is considered stale
# (this is not used in the current version of the code, but can be used for future improvements)
MAX_AGE = 60

# CONSTANTS

BLIND_URL = "https://www.teamblind.com/company/"
HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# HELPER FUNCTIONS

def build_url(input_company_name):
    formatted_name = format_company_name(input_company_name)
    return f"{BLIND_URL}{formatted_name}"

def format_company_name(input_company_name):
    return input_company_name.replace(" & ", "&").replace(" ", "-").replace(".", "")

def read_database_file():
    try:
        with open(DATABASE_FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_database_file(database):
    with open(DATABASE_FILE_PATH, "w") as file:
        json.dump(database, file, indent=4)

def read_input_file():
    with open(INPUT_FILE_PATH, "r") as file:
        company_names = file.readlines()
    return [name.strip() for name in company_names]

def get_company_data_from_database(database, company_name):
    if company_name in database:
        company_data = database[company_name]
        current_date = datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
        last_updated = datetime.strptime(company_data["last_updated"], "%Y-%m-%d")
        if (current_date - last_updated).days > MAX_AGE:
            print(f"\tData for {company_name} is stale. Fetching new data.")
            del database[company_name]
            return None
        return company_data
    else:
        return None

def get_company_data_from_blind(database, input_company_name):
    url = build_url(input_company_name)
    response = requests.get(url, headers=HTTP_HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    if response.status_code != 200:
        print(f"Failed to retrieve data for {input_company_name}. Status code: {response.status_code}")
    else:
        try:
            # general
            company_name_tag = soup.find("div", class_="text-center text-2xl font-bold lg:text-left")
            company_name = company_name_tag.text.strip() if company_name_tag else None
            link_tag = soup.find("link", rel="canonical")
            url = link_tag["href"] if link_tag and "href" in link_tag.attrs else None

            # overview
            website = soup.find("h3", class_="text-base font-semibold sm:text-lg").text.strip()
            overview_div_list = soup.find_all("div", class_="text-base font-semibold sm:text-lg")
            industry = overview_div_list[0].text.strip()
            locations = overview_div_list[1].text.strip()
            founded = overview_div_list[2].text.strip()
            size = overview_div_list[3].text.strip()
            salary = overview_div_list[4].text.strip()

            # reviews
            overall_score = soup.find("div", class_="flex items-start gap-2 border-b border-gray-300 pb-1 pr-4 lg:flex-col lg:border-b-0 lg:border-r").find("div", class_="text-xl font-semibold").text.strip()
            reviews_div_list = soup.find("div", class_="grid grid-flow-row grid-cols-1 gap-x-10 gap-y-4 lg:ml-9 lg:grid-cols-2").find_all("div", class_="font-semibold")
            career_growth_score = reviews_div_list[0].text.strip()
            work_life_balance_score = reviews_div_list[1].text.strip()
            compensation_benefits_score = reviews_div_list[2].text.strip()
            company_culture_score = reviews_div_list[3].text.strip()
            management_score = reviews_div_list[4].text.strip()

            # compensation
            median_total_compensation = soup.find("p", class_="font-bold text-blue-system sm:text-lg").text.strip()
            compensation_h5_list = soup.find_all("h5", class_="text-md font-semibold")
            _25th_percentile = compensation_h5_list[0].text.strip()
            _70th_percentile = compensation_h5_list[1].text.strip()
            _90th_percentile = compensation_h5_list[2].text.strip()
            
            # other
            current_date = time.strftime("%Y-%m-%d")

            company_data = {
                # general
                "company_name": company_name,
                "url": url,
                # overview
                "website": website,
                "industry": industry,
                "locations": locations,
                "founded": founded,
                "size": size,
                "salary": salary,
                # reviews
                "overall": overall_score,
                "career_growth": career_growth_score,
                "work_life_balance": work_life_balance_score,
                "compensation_benefits": compensation_benefits_score,
                "company_culture": company_culture_score,
                "management": management_score,
                # compensation
                "median_total_compensation": median_total_compensation,
                "25th_percentile": _25th_percentile,
                "70th_percentile": _70th_percentile,
                "90th_percentile": _90th_percentile,
                # other
                "last_updated": current_date
            }
            database[input_company_name] = company_data
        except AttributeError as e:
            print(f"Error parsing data for {company_name}: {e}")
            return None
    return company_data

def process_data(input_company_names):
    with open(OUTPUT_FILE_PATH, "w", newline="") as file:
        writer = csv.writer(file)
        header_row = []
        for key, value in OUTPUT_FILE_HEADERS.items():
            if value:
                header_row.append(key)
        writer.writerow(header_row)
        for i, input_company_name in enumerate(input_company_names):
            print(f"Processing {i + 1}/{len(input_company_names)}: {input_company_name}")
            company_data = get_company_data_from_database(database, input_company_name)
            if company_data:
                print("Got data from database")
            else:
                company_data = get_company_data_from_blind(database, input_company_name)
                if company_data:
                    print("Got data from Blind")
                time.sleep(TIME_DELAY)
            if company_data:
                data_row = []
                for key, value in OUTPUT_FILE_HEADERS.items():
                    if value:
                        if key in company_data:
                            data_row.append(company_data[key])
                        else:
                            data_row.append("")
                writer.writerow(data_row)
            else:
                writer.writerow(input_company_name)


# MAIN FUNCTION

if __name__ == "__main__":
    input_company_names = read_input_file()
    database = read_database_file()
    process_data(input_company_names)
    write_database_file(database)
