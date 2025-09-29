import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Load your existing CSVs
clients_df = pd.read_csv("clients_data.csv")
accounts_df = pd.read_csv("accounts.csv")

# Setup
START_DATE = datetime(2017, 10, 1)
END_DATE = datetime.now()
TRANSACTIONS_PER_ACCOUNT = (10, 50)
transaction_types = ["Deposit", "Withdrawal", "Transfer Out", "Transfer In", "Bill Payment", "Salary"]
channels = ["ATM", "Online", "Branch", "Mobile App"]

clients_lookup = clients_df.set_index("client_id").to_dict(orient="index")
accounts = accounts_df.to_dict(orient="records")
transactions = []
transaction_id = 1

for acc in accounts:
    acc_id = acc["account_id"]
    client_id = acc["client_id"]
    join_date = pd.to_datetime(clients_lookup[client_id]["join_date"])
    balance = acc["balance"]
    
    num_tx = random.randint(*TRANSACTIONS_PER_ACCOUNT)
    tx_dates = sorted([join_date + timedelta(days=random.randint(0, (END_DATE - join_date).days))
                       for _ in range(num_tx)])

    for date in tx_dates:
        tx_type = random.choices(transaction_types, weights=[25, 25, 15, 15, 10, 10])[0]
        channel = random.choice(channels)
        counterparty = None

        if tx_type in ["Deposit", "Salary"]:
            amount = round(random.uniform(100, 5000), 2)
            balance += amount
        elif tx_type == "Withdrawal":
            amount = -round(random.uniform(50, min(balance, 2000)), 2)
            balance += amount
        elif tx_type == "Bill Payment":
            amount = -round(random.uniform(100, min(balance, 1500)), 2)
            balance += amount
        elif tx_type == "Transfer Out":
            amount = -round(random.uniform(100, min(balance, 3000)), 2)
            balance += amount
            counterparty_row = random.choice([a for a in accounts if a["account_id"] != acc_id])
            counterparty = counterparty_row["account_id"]
            transactions.append({
                "transaction_id": f"TXN{transaction_id + 1}",
                "account_id": counterparty,
                "client_id": counterparty_row["client_id"],
                "transaction_type": "Transfer In",
                "amount": -amount,
                "transaction_date": date,
                "balance_after": None,
                "counterparty_account_id": acc_id,
                "description": f"Transfer received from ACC{acc_id}",
                "channel": channel
            })

        else:
            amount = round(random.uniform(50, 2000), 2)
            balance += amount

        transactions.append({
            "transaction_id": f"TXN{transaction_id}",
            "account_id": acc_id,
            "client_id": client_id,
            "transaction_type": tx_type,
            "amount": amount,
            "transaction_date": date,
            "balance_after": round(balance, 2),
            "counterparty_account_id": counterparty,
            "description": f"{tx_type} via {channel}",
            "channel": channel
        })

        transaction_id += 2 if tx_type == "Transfer Out" else 1

# Save the result
transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv("transactions_table.csv", index=False)
print(transactions_df.head())
