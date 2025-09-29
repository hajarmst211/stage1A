import pandas as pd 
import random
from scores import function_score, city_score, age_score, account_type_score

# Load client data
clients_df = pd.read_csv("../csv/clients_data.csv")  # was 'read_as_csv' — corrected

# Compute balance based on multiple scores
def compute_balance(city, function, age, account_type):
    f_score = function_score.get(function, 0.4)
    c_score = city_score.get(city, 0.5)
    a_score = age_score(age)
    acc_score = account_type_score.get(account_type, 0.5)

    global_score = f_score * c_score * a_score * acc_score
    BASE_MIN_BALANCE = 500    
    BASE_MAX_BALANCE = 500000 
    balance = BASE_MIN_BALANCE + global_score * (BASE_MAX_BALANCE - BASE_MIN_BALANCE)

    noise = random.uniform(-0.05, 0.05) 
    balance *= (1 + noise)

    return round(balance, 2)

# Determine account type based on age
def get_account_type(age):
    if 18 <= age <= 23:
        return "Student"
    elif 24 <= age <= 30:
        return random.choices(["Student", "Everyday Deposit", "E-Banking"], weights=[0.4, 0.4, 0.2])[0]
    elif 31 <= age <= 45:
        return random.choices([
            "Everyday Deposit", "E-Banking", "Islamic Financing - Basic", "Savings", "Agricultural Financing"
        ], weights=[0.3, 0.2, 0.2, 0.2, 0.1])[0]
    elif 46 <= age <= 60:
        return random.choices([
            "Islamic Financing - Basic", "Islamic Financing - Advanced", "Real Estate Financing",
            "Investment Account", "Takaful Insurance Account", "Savings"
        ], weights=[0.15, 0.2, 0.25, 0.15, 0.15, 0.1])[0]
    elif 61 <= age <= 75:
        return random.choices([
            "Takaful Insurance Account", "Savings", "Investment Account"
        ], weights=[0.5, 0.3, 0.2])[0]
    else:
        return "Savings"	

# Generate unique account ID
def generate_account_id(index):
    return f"AKB{100000 + index}"

# Generate accounts data
accounts_data = []

for idx, row in clients_df.iterrows():
    client_id = row['client_id']
    age = row['age']
    city = row['city']
    function = row['function']
    
    account_type = get_account_type(age)
    balance = compute_balance(city, function, age, account_type)
    account_id = generate_account_id(idx)
    
    accounts_data.append({
        "account_id": account_id,
        "client_id": client_id,
        "account_type": account_type,
        "balance": balance
    })

# Save to CSV
accounts_df = pd.DataFrame(accounts_data)
accounts_df.to_csv("accounts.csv", index=False)

print("✅ accounts.csv generated successfully.")
