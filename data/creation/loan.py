import pandas as pd
import random
from datetime import datetime, timedelta
from clients import function1, function2, function3

# Load accounts data
clients_data = pd.read_csv('clients_data.csv')
account_ids = clients_data['client_id'].tolist()

def generate_start_date():
    start_date = datetime(2018, 1, 1)
    end_date = datetime(2025, 7, 1)
    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days)

def generate_end_date(start_date):
    end_date = datetime(2025, 7, 1)
    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days + 60)  # 60 days buffer

def generate_amount(category):
    if category in function1:
        return random.randint(1000, 10000)
    elif category in function2:
        return random.randint(10000, 50000)
    else:
        return random.randint(50000, 250000)

def generate_monthly_amount(function, loan_amount, start_date, end_date):
    if function in function1:
        category = 'Cat1'
    elif function in function2:
        category = 'Cat2'
    else:
        category = 'Cat3'

    interest_rates = {'Cat1': 0.05, 'Cat2': 0.07, 'Cat3': 0.10}  # annual rates

    annual_interest_rate = interest_rates[category]
    term_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    term_months = max(1, term_months)
    term_years = term_months / 12

    total_repayment = loan_amount * (1 + annual_interest_rate * term_years)
    monthly_payment = total_repayment / term_months

    return round(monthly_payment, 2)

def calculate_amount_paid(start_date, end_date, monthly_payment):
    today = datetime.now().date()
    start_date = start_date.date()
    end_date = end_date.date()

    months_passed = (today.year - start_date.year) * 12 + (today.month - start_date.month)
    total_months_in_term = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    total_months_in_term = max(1, total_months_in_term)
    number_of_payments_made = max(0, min(months_passed, total_months_in_term))

    total_paid = number_of_payments_made * monthly_payment
    return round(total_paid, 2)

# Generate loan data
columns = ['client_id', 'amount', 'loan_term_months', 'start_date', 'end_date', 'amount_paid', 'monthly_deposit']
loaned_accounts = set()
all_rows = []

# You probably want more than one loan, so use a loop
for _ in range(1000):  # Adjust number of loans
    id = random.choice(account_ids)
    if id not in loaned_accounts:
        function = clients_data.loc[clients_data['client_id'] == id, 'function'].values[0]
        amount = generate_amount(function)
        loan_term_months = random.choice([12, 24, 36, 48, 60])
        start = generate_start_date()
        end = generate_end_date(start)
        monthly_payment = generate_monthly_amount(function, amount, start, end)
        amount_paid = calculate_amount_paid(start, end, monthly_payment)

        row = [id, amount, loan_term_months, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), amount_paid, monthly_payment]
        all_rows.append(row)
        loaned_accounts.add(id)

# Save to CSV
loans = pd.DataFrame(all_rows, columns=columns)
loans.to_csv('loans.csv', index=False, encoding='utf-8-sig')
