exclusions = {
    "Audible":      "fully in office",
    "Ciena":        "no relevant jobs",
    "Cirrus Logic": "no relevant jobs",
    "Dell":         "fully in office",
    "IMC":          "bad location (Chicago)",
    "Logitech":     "no relevant jobs",
    "Lululemon":    "bad location (Seattle)",
    "Nintendo":     "bad location (Redmond)",
    "Riot Games":   "bad location (Los Angeles)",
    "Ubisoft":      "bad location (Canada)"
}

def calculate_tier(company_data):
    if (company_data["company_name"]) in exclusions:
        return 'X'
    elif float(company_data["work_life_balance"]) < 3.4 \
        or float(company_data["company_culture"]) < 3.1 \
        or company_data["size"] == "1 to 50 employees" \
        or company_data["size"] == "51 to 200 employees":
        return 'C'
    elif float(company_data["work_life_balance"]) < 3.8 \
        or float(company_data["company_culture"]) < 3.5:
        return 'B'
    elif float(company_data["work_life_balance"]) < 4.2 \
        or float(company_data["company_culture"]) < 3.9:
        return 'A'
    else:
        return '$'