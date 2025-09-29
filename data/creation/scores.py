
function_score = {
    # Function 1: Low-income / Entry level
    'Student': 0.30,
    'Technician': 0.45,
    'Sales Associate': 0.40,
    'Customer Service Representative': 0.42,
    'Junior Analyst': 0.48,
    'Intern': 0.30,
    'Call Center Agent': 0.38,
    'Graphic Designer': 0.50,
    'IT Support Specialist': 0.50,
    'Receptionist': 0.40,
    'Marketing Assistant': 0.45,
    'Social Media Manager': 0.50,

    # Function 2: Mid-income / Experienced
    'Manager': 0.75,
    'Engineer': 0.80,
    'Teacher': 0.65,
    'Merchant': 0.70,
    'Doctor': 0.85,
    'Accountant': 0.70,
    'Civil Servant': 0.68,
    'Lawyer': 0.80,
    'Architect': 0.78,
    'Pharmacist': 0.80,
    'Senior Developer': 0.78,
    'Project Manager': 0.75,
    'Bank Employee': 0.72,
    'Business Owner': 0.85,
    'HR Specialist': 0.70,
    'Real Estate Agent': 0.74,

    # Function 3: High-income / Senior
    'Retired': 0.60,
    'Consultant': 0.85,
    'Director': 0.95,
    'Artisan': 0.65,
    'Professor': 0.88,
    'Senior Manager': 0.92,
    'Landowner': 0.90,
    'Judge': 0.95,
    'Experienced Merchant': 0.88,
    'Government Advisor': 0.96,
    'Investor': 1.00
}


city_score = {
    "Agadir": 0.75,
    "Benslimane": 0.50,
    "Berkane": 0.52,
    "Casablanca": 1.00,
    "Fès": 0.80,
    "Meknès": 0.70,
    "Nador": 0.56,
    "Oujda": 0.58,
    "Rabat": 0.90,
    "Tanger": 0.85,
    "Tétouan": 0.65,
    "Laâyoune": 0.38,
    "El Jadida": 0.68,
    "Fkih Ben Salah": 0.40,
    "Béni Mellal": 0.60,
    "Ouarzazate": 0.45
}
account_type_score = {
    "Everyday Deposit": 0.5,             # Regular daily-use accounts
    "Islamic Financing - Basic": 0.6,    # Mourabaha, Ijara, etc. for basic needs
    "Islamic Financing - Advanced": 0.8, # Musharaka, Mudaraba (for entrepreneurs, investors)
    "Real Estate Financing": 0.85,       # For home or land purchases
    "Agricultural Financing": 0.7,       # Equipment, irrigation, etc.
    "Investment Account": 0.9,           # Profit-focused clients
    "Takaful Insurance Account": 0.75    # Risk protection/savings mix
}



def age_score(age):
    if age < 25:
        return 0.3
    elif age < 35:
        return 0.5
    elif age < 50:
        return 0.8
    elif age < 65:
        return 1.0
    elif age < 75:
        return 0.8
    else:
        return 0.6
