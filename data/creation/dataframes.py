import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker for data generation
fake = Faker()

# --- 1. Define Constants (Control the size of your data here) ---
NUM_CLIENTS = 500
NUM_ACCOUNTS = 750
NUM_BRANCHES = 10
NUM_EMPLOYEES = 50
NUM_LOANS = 150
NUM_CREDIT_CARDS = 300
NUM_LOAN_PAYMENTS = 1800 # Multiple payments per loan
NUM_SUPPORT_TICKETS = 200

# --- 2. Regenerate Your Core Tables (for a self-contained, runnable example) ---
# We'll regenerate these so the script can run on its own.
# You can replace this section with loading your own existing CSVs.

print("--- Generating Core DataFrames ---")

# Clients DataFrame
clients_data = {
    'client_id': range(1, NUM_CLIENTS + 1),
    'first_name': [fake.first_name() for _ in range(NUM_CLIENTS)],
    'last_name': [fake.last_name() for _ in range(NUM_CLIENTS)],
    'age': np.random.randint(18, 80, size=NUM_CLIENTS),
    'city': [fake.city() for _ in range(NUM_CLIENTS)],
    'function': [fake.job() for _ in range(NUM_CLIENTS)],
    'email_address': [fake.unique.email() for _ in range(NUM_CLIENTS)],
    'CIN': [f'B{fake.unique.random_number(digits=7)}' for _ in range(NUM_CLIENTS)],
    'join_date': [fake.date_between(start_date='-15y', end_date='today') for _ in range(NUM_CLIENTS)]
}
clients_df = pd.DataFrame(clients_data)
clients_df['join_date'] = pd.to_datetime(clients_df['join_date']) # Convert to datetime objects
print("Clients DataFrame generated.")

# Accounts DataFrame
accounts_data = {
    'account_id': range(1001, 1001 + NUM_ACCOUNTS),
    'client_id': np.random.choice(clients_df['client_id'], size=NUM_ACCOUNTS),
    'account_type': np.random.choice(['Checking', 'Savings'], size=NUM_ACCOUNTS, p=[0.6, 0.4]),
    'balance': np.round(np.random.uniform(50, 80000, size=NUM_ACCOUNTS), 2),
    'open_date': [fake.date_between(start_date='-14y', end_date='today') for _ in range(NUM_ACCOUNTS)],
    'account_status': np.random.choice(['Active', 'Dormant', 'Frozen'], size=NUM_ACCOUNTS, p=[0.9, 0.08, 0.02]),
    'currency': 'SAR' # Assuming a single currency for Al Akhdar Bank
}
accounts_df = pd.DataFrame(accounts_data)
accounts_df['open_date'] = pd.to_datetime(accounts_df['open_date'])
print("Accounts DataFrame generated.")

# Note: We will not generate the full transactions table, as it's complex.
# We will assume the other tables are what you need to generate now.


# --- 3. Generate New, Supplementary DataFrames ---

print("\n--- Generating Supplementary DataFrames ---")

# Branches DataFrame
branches_data = {
    'branch_id': range(1, NUM_BRANCHES + 1),
    'branch_name': [f'{fake.city()} Main' for _ in range(NUM_BRANCHES)],
    'city': [fake.city() for _ in range(NUM_BRANCHES)],
    'address': [fake.street_address() for _ in range(NUM_BRANCHES)],
}
branches_df = pd.DataFrame(branches_data)

# Employees DataFrame
employees_data = {
    'employee_id': range(101, 101 + NUM_EMPLOYEES),
    'first_name': [fake.first_name() for _ in range(NUM_EMPLOYEES)],
    'last_name': [fake.last_name() for _ in range(NUM_EMPLOYEES)],
    'role': np.random.choice(['Teller', 'Loan Officer', 'Branch Manager', 'Analyst'], size=NUM_EMPLOYEES, p=[0.4, 0.3, 0.1, 0.2]),
    'branch_id': np.random.choice(branches_df['branch_id'], size=NUM_EMPLOYEES),
    'hire_date': [fake.date_between(start_date='-20y', end_date='-1M') for _ in range(NUM_EMPLOYEES)]
}
employees_df = pd.DataFrame(employees_data)

# Loans DataFrame
# Ensure only one loan per client in this generation for simplicity
active_clients = clients_df[clients_df['join_date'] < (datetime.now() - timedelta(days=365))]
loan_clients = np.random.choice(active_clients['client_id'], size=NUM_LOANS, replace=False)

loans_data = {
    'loan_id': range(2001, 2001 + NUM_LOANS),
    'client_id': loan_clients,
    'loan_type': np.random.choice(['Personal', 'Auto', 'Mortgage'], size=NUM_LOANS, p=[0.5, 0.3, 0.2]),
    'principal_amount': np.round(np.random.uniform(5000, 250000, size=NUM_LOANS), 2),
    'interest_rate': np.round(np.random.uniform(3.5, 15.0, size=NUM_LOANS), 2),
    'loan_term_months': np.random.choice([24, 48, 60, 120, 360], size=NUM_LOANS),
    'start_date': [fake.date_between(start_date='-8y', end_date='-3M') for _ in range(NUM_LOANS)],
    'loan_status': np.random.choice(['Active', 'Paid Off', 'Default'], size=NUM_LOANS, p=[0.8, 0.15, 0.05])
}
loans_df = pd.DataFrame(loans_data)
loans_df['start_date'] = pd.to_datetime(loans_df['start_date'])

# Loan Payments DataFrame
loan_payments_data = {
    'payment_id': range(3001, 3001 + NUM_LOAN_PAYMENTS),
    'loan_id': np.random.choice(loans_df['loan_id'], size=NUM_LOAN_PAYMENTS),
    'payment_date': [datetime.now()] * NUM_LOAN_PAYMENTS, # Placeholder, will be corrected below
    'amount_paid': 0.0 # Placeholder
}
loan_payments_df = pd.DataFrame(loan_payments_data)

# Make payment dates and amounts realistic (after loan start date)
loan_payments_df = pd.merge(loan_payments_df, loans_df[['loan_id', 'start_date', 'principal_amount', 'loan_term_months']], on='loan_id')
loan_payments_df['payment_date'] = loan_payments_df['start_date'].apply(
    lambda x: fake.date_between(start_date=x, end_date='today')
)
loan_payments_df['amount_paid'] = np.round(loan_payments_df['principal_amount'] / loan_payments_df['loan_term_months'] * np.random.uniform(0.9, 1.2), 2)
loan_payments_df = loan_payments_df[['payment_id', 'loan_id', 'payment_date', 'amount_paid']] # Keep original columns

# Credit Cards DataFrame
card_clients = np.random.choice(clients_df['client_id'], size=NUM_CREDIT_CARDS, replace=True)
credit_cards_data = {
    'card_id': range(4001, 4001 + NUM_CREDIT_CARDS),
    'client_id': card_clients,
    'card_number': [fake.credit_card_number() for _ in range(NUM_CREDIT_CARDS)],
    'card_type': [fake.credit_card_provider() for _ in range(NUM_CREDIT_CARDS)],
    'credit_limit': np.random.choice([2500, 5000, 10000, 25000, 50000], size=NUM_CREDIT_CARDS),
    'issue_date': [fake.date_between(start_date='-4y', end_date='-1y') for _ in range(NUM_CREDIT_CARDS)],
    'expiry_date': [fake.credit_card_expire(start="now", end="+4y", date_format="%m/%y") for _ in range(NUM_CREDIT_CARDS)],
    'card_status': np.random.choice(['Active', 'Lost', 'Expired'], size=NUM_CREDIT_CARDS, p=[0.9, 0.07, 0.03])
}
credit_cards_df = pd.DataFrame(credit_cards_data)

# Customer Support Tickets DataFrame
support_tickets_data = {
    'ticket_id': range(5001, 5001 + NUM_SUPPORT_TICKETS),
    'client_id': np.random.choice(clients_df['client_id'], size=NUM_SUPPORT_TICKETS),
    'employee_id': np.random.choice(employees_df['employee_id'], size=NUM_SUPPORT_TICKETS),
    'issue_type': np.random.choice(['Transaction Dispute', 'Card Service', 'Account Access', 'Loan Inquiry', 'General Question'], size=NUM_SUPPORT_TICKETS),
    'open_date': [fake.date_between(start_date='-2y', end_date='today') for _ in range(NUM_SUPPORT_TICKETS)],
    'status': np.random.choice(['Resolved', 'Open', 'In Progress'], size=NUM_SUPPORT_TICKETS, p=[0.7, 0.1, 0.2])
}
support_tickets_df = pd.DataFrame(support_tickets_data)
# Add a close date for resolved tickets
support_tickets_df['open_date'] = pd.to_datetime(support_tickets_df['open_date'])
resolved_mask = support_tickets_df['status'] == 'Resolved'
support_tickets_df.loc[resolved_mask, 'close_date'] = support_tickets_df.loc[resolved_mask, 'open_date'] + pd.to_timedelta(np.random.randint(1, 14, size=resolved_mask.sum()), unit='d')
support_tickets_df['close_date'] = pd.to_datetime(support_tickets_df['close_date'])


# --- 4. Display the Heads of All New DataFrames ---
print("\n--- Generated DataFrame Samples ---")

print("\nBranches DataFrame:")
print(branches_df.head())

print("\nEmployees DataFrame:")
print(employees_df.head())

print("\nLoans DataFrame:")
print(loans_df.head())

print("\nLoan Payments DataFrame:")
print(loan_payments_df.head())

print("\nCredit Cards DataFrame:")
print(credit_cards_df.head())

print("\nSupport Tickets DataFrame:")
print(support_tickets_df.head())


# --- 5. (Optional) Save to CSV Files ---
# This is a great next step to persist your data.
save_to_csv = False # Set to True to save the files

if save_to_csv:
    clients_df.to_csv('clients.csv', index=False)
    accounts_df.to_csv('accounts.csv', index=False)
    branches_df.to_csv('branches.csv', index=False)
    employees_df.to_csv('employees.csv', index=False)
    loans_df.to_csv('loans.csv', index=False)
    loan_payments_df.to_csv('loan_payments.csv', index=False)
    credit_cards_df.to_csv('credit_cards.csv', index=False)
    support_tickets_df.to_csv('support_tickets.csv', index=False)
    print("\nAll dataframes saved to .csv files.")