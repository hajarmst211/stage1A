import pandas as pd
# Faker is imported but not used, so it can be removed if you wish.
# from faker import Faker 
import random
import string
# Use datetime objects directly for cleaner code
from datetime import datetime, timedelta 
# Assumes you have a 'prefixes.py' file with a 'prefixes' dictionary inside.
from prefixes import prefixes 

branches=pd.read_csv('../csv/branches.csv')
branches['City'] = branches['City'].str.lower()
# --- FUNCTIONS ---

def load_names(file: str):
    # <-- Corrected Indentation
    with open(file, 'r', encoding='utf-8') as f:
        # <-- Corrected Indentation
        names = [name.strip() for name in f.readlines()]
    # <-- Corrected Indentation
    return names

def generate_email(fn: str, ln: str):
    fn = fn.lower().replace(' ', '')
    ln = ln.lower().replace(' ', '')
    character_pool = string.ascii_lowercase + string.digits
    random_suffix = ''.join(random.choices(character_pool, k=3))

    email = f"{fn}.{ln}_{random_suffix}@gmail.com"
    return email

def generate_join_date():
    # Using datetime objects directly is cleaner than strptime
    start_date = datetime(2017, 10, 1)
    end_date = datetime(2025, 7, 1)
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_function(age: int):
    # <-- Corrected Bug: Use <= to include the boundary ages (29, 55).
    if 18 <= age <= 29:
        # <-- Corrected Indentation
        function = random.choice(function1)
    elif 30 <= age <= 55:
        # <-- Corrected Indentation
        function = random.choice(function2)
    else:
        # <-- Corrected Indentation
        function = random.choice(function3)
    # <-- Corrected Indentation
    return function

def generate_cin(city: str):
    # <-- Corrected Indentation
    # <-- Corrected Bug: Use random.choice
    city_prefixes = prefixes.get(city, prefixes.get('default', ['XX']))
    prefix = random.choice(city_prefixes)
    # <-- Corrected Bug: Use random.randint
    numbers = random.randint(10000, 999999)
    # <-- Corrected Indentation
    return f"{prefix}{numbers}"

def find_branche(city):
    # The input city is already lowercased from the main loop
    possible_branches = branches[branches['City'] == city]['Branch Name'].tolist()
    if possible_branches:
        return random.choice(possible_branches)
    else:
        print(f"⚠️ No branch found for city: {city}")
        return None



# --- CONFIGURATION & DATA LOADING ---

function1 = [
    'Student', 'Technician', 'Sales Associate', 'Customer Service Representative',
    'Junior Analyst', 'Intern', 'Call Center Agent', 'Graphic Designer',
    'IT Support Specialist', 'Receptionist', 'Marketing Assistant', 'Social Media Manager'
]
function2 = [
    'Manager', 'Engineer', 'Teacher', 'Merchant', 'Doctor', 'Accountant','Engineer','Teacher',
    'Civil Servant', 'Lawyer', 'Architect', 'Pharmacist', 'Senior Developer',
    'Project Manager', 'Bank Employee', 'Business Owner', 'HR Specialist', 'Real Estate Agent'
]
function3 = [
    'Retired', 'Consultant', 'Director', 'Artisan', 'Professor', 'Senior Manager','Engineer','Teacher','Pharmacist',
    'Doctor', 'Landowner', 'Judge', 'Experienced Merchant', 'Government Advisor', 'Investor','Business Owner', 
    'Bank Employee','HR Specialist'
]
if __name__ == "__main__":

    first_names = load_names('first_names.txt')
    last_names = load_names('last_names.txt')
    cities = load_names('cities.txt')

    # <-- Corrected Bug: Fixed column names
    columns = ['client_id', 'first_name', 'last_name', 'age', 'city', 'function', 'email_adress', 'CIN', 'join_date','branche']

    # --- MAIN GENERATION SCRIPT ---

    all_rows = []
    generated_cines = set()
    branches['City'] = branches['City'].str.strip().str.lower()

    for i in range(3000):
        client_id = i + 1
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        age = random.randint(18, 80)
        city = random.choice(cities).strip().lower()
        function = generate_function(age)
        email = generate_email(fn, ln)
        branche= find_branche(city)

        
        while True:
            # <-- Corrected Indentation
            CIN = generate_cin(city)
            if CIN not in generated_cines:
                # <-- Corrected Indentation
                generated_cines.add(CIN)
                break

        join_date = generate_join_date()

        row = [client_id, fn, ln, age, city, function, email, CIN, join_date, branche]
        all_rows.append(row)

    # Create the DataFrame
    client_df = pd.DataFrame(all_rows, columns=columns)

    # Save the data to a CSV file (recommended)
    client_df.to_csv('../csv/clients.csv', index=False, encoding='utf-8-sig')
    print('data')