import requests
from bs4 import BeautifulSoup


INPUT_FILE_PATH = "input/input_1.txt"
OUTPUT_FILE_PATH = "output/output_1.txt"

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
            overall_score = soup.find("div", class_="flex items-start gap-2 border-b border-gray-300 pb-1 pr-4 lg:flex-col lg:border-b-0 lg:border-r").find("div", class_="text-xl font-semibold").text.strip()
            subscores_div = soup.find("div", class_="grid grid-flow-row grid-cols-1 gap-x-10 gap-y-4 lg:ml-9 lg:grid-cols-2").find_all("div", class_="font-semibold")
            career_growth_score = subscores_div[0].text.strip()
            work_life_balance_score = subscores_div[1].text.strip()
            compensation_benefits_score = subscores_div[2].text.strip()
            company_culture_score = subscores_div[3].text.strip()
            management_score = subscores_div[4].text.strip()
            company_review_scores = {
                "overall": overall_score,
                "career_growth": career_growth_score,
                "work_life_balance": work_life_balance_score,
                "compensation_benefits": compensation_benefits_score,
                "company_culture": company_culture_score,
                "management": management_score
            }
            review_data.append((company_name, company_review_scores))
        except AttributeError:
            print(f"Review scores not found for {company_name}.")

    return review_data

def write_output_file(review_data):
    with open(OUTPUT_FILE_PATH, "w") as file:
        for company_name, review_scores in review_data:
            file.write(f"{company_name}: {review_scores}\n")

def print_review_data(review_data):
    for company_name, review_score in review_data:
        print(f"{company_name}: {review_score}")

# Main
if __name__ == "__main__":
    company_names = read_input_file()
    review_data = parse_review_scores(company_names)
    write_output_file(review_data)
    print_review_data(review_data)