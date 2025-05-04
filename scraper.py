import csv
import requests
import time
from bs4 import BeautifulSoup

# MODIFY THESE
INPUT_FILE_PATH = "input/input_5.txt"
OUTPUT_FILE_PATH = "output/output_5.csv"
TIME_DELAY = 1 # seconds

# CONSTANTS
BLIND_URL = "https://www.teamblind.com/company/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def build_url(company_name):
    formatted_name = format_company_name(company_name)
    return f"{BLIND_URL}{formatted_name}"

def format_company_name(company_name):
    return company_name.replace(" ", "-").lower()

def read_input_file():
    with open(INPUT_FILE_PATH, "r") as file:
        company_names = file.readlines()
    return [name.strip() for name in company_names]

def parse_review_scores(company_names):
    review_data = []
    for company_name in company_names:
        url = build_url(company_name)
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")
        if response.status_code != 200:
            print(f"Failed to retrieve data for {company_name}. Status code: {response.status_code}")
            continue
        try:
            company_name_tag = soup.find("div", class_="text-center text-2xl font-bold lg:text-left")
            company_name = company_name_tag.text.strip() if company_name_tag else None
            link_tag = soup.find("link", rel="canonical")
            url = link_tag["href"] if link_tag and "href" in link_tag.attrs else None
            overall_score = soup.find("div", class_="flex items-start gap-2 border-b border-gray-300 pb-1 pr-4 lg:flex-col lg:border-b-0 lg:border-r").find("div", class_="text-xl font-semibold").text.strip()
            subscores_div = soup.find("div", class_="grid grid-flow-row grid-cols-1 gap-x-10 gap-y-4 lg:ml-9 lg:grid-cols-2").find_all("div", class_="font-semibold")
            career_growth_score = subscores_div[0].text.strip()
            work_life_balance_score = subscores_div[1].text.strip()
            compensation_benefits_score = subscores_div[2].text.strip()
            company_culture_score = subscores_div[3].text.strip()
            management_score = subscores_div[4].text.strip()
            company_data = {
                "company_name": company_name,
                "overall": overall_score,
                "career_growth": career_growth_score,
                "work_life_balance": work_life_balance_score,
                "compensation_benefits": compensation_benefits_score,
                "company_culture": company_culture_score,
                "management": management_score,
                "url": url
            }
            review_data.append((company_name, company_data))
        except AttributeError:
            print(f"Review scores not found for {company_name}.")
        time.sleep(TIME_DELAY)

    return review_data

def write_output_file(review_data):
    with open(OUTPUT_FILE_PATH, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Overall", "Career Growth", "Work-Life Balance", "Compensation & Benefits", "Company Culture", "Management", "URL"])
        for company_name, company_data in review_data:
            writer.writerow([
                company_data["company_name"],
                company_data["overall"],
                company_data["career_growth"],
                company_data["work_life_balance"],
                company_data["compensation_benefits"],
                company_data["company_culture"],
                company_data["management"],
                company_data["url"]
            ])

def print_review_data(review_data):
    for company_name, review_score in review_data:
        print(f"{company_name}:\t{review_score}")

# MAIN
if __name__ == "__main__":
    company_names = read_input_file()
    review_data = parse_review_scores(company_names)
    write_output_file(review_data)
    print_review_data(review_data)