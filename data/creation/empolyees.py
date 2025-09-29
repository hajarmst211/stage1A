import pandas as pd
import random
# Assuming these client functions are in a file named clients.py
from clients import load_names, generate_email, generate_join_date, generate_cin
from clients import find_branche

# Load the branches data
branches=pd.read_csv('../csv/branches.csv')
branches['City'] = branches['City'].str.lower()

# Define the possible roles for employees
akhdar_bank_roles = [
    "Managing Director",
    "Branch Manager",
    "Directeur d’Agence",
    "Conseiller(ère) Clientèle",
    "Chargé(e) Principal(e) des Opérations Clientèle",
    "Chargé(e) des Opérations Clientèle",
    "Chargé(e) des Opérations Internationales",
    "Chargé(e) de Développement – Marché Immobilier",
    "Chargé(e) de Développement – Marché Automobile",
    "Juriste d’affaires",
    "Chargé(e) de Reporting Réglementaire",
    "Contrôleur de Gestion Confirmé",
    "Chef de Projet Organisation et Stratégie",
    "Auditeur Senior",
    "Ingénieur Réseau et Sécurité",
    "Chargé(e) Risque Crédit",
    "Agent de Fiabilisation de données",
    "Responsable contrôle des risques",
    "Chef de projet étude & développement",
    "Chef de projet AMOA",
    "Responsable bureau d’ordre",
    "Auditeur Senior"
]

def find_branche(city):
    possible_branches = branches[branches['City'] == city]['Branch Name'].tolist()  
    # Check if any branches were found for that city
    if possible_branches:
        # If yes, pick one randomly
        return random.choice(possible_branches)
    else:
        # If no, assign a placeholder (None is best, it becomes NaN in the DataFrame)
        return None

# Define the columns for the output DataFrame
columns = ['first_name', 'last_name', 'age', 'city', 'function', 'email_adress', 'CIN', 'join_date', 'branche']

# Initialize an empty list to store employee data rows
all_rows = []

# Load data from text files
fn = load_names('first_names.txt')
ln = load_names('last_names.txt')
cities = load_names('cities.txt')

# A set to keep track of generated CINs to ensure uniqueness
generated_cines = set()

# Loop to generate 170 employee records
for i in range(170):
    first_name = random.choice(fn)
    last_name = random.choice(ln)
    email = generate_email(first_name, last_name)  
    city = random.choice(cities).lower().strip()
    age = random.randint(25, 50)
    join_date = generate_join_date()
    function = random.choice(akhdar_bank_roles)
    branche= find_branche(city)

    # Generate a unique CIN
    while True:
        CIN = generate_cin(city)
        if CIN not in generated_cines:
            generated_cines.add(CIN)
            break

    row = [first_name, last_name, age, city, function, email, CIN, join_date, branche]
    all_rows.append(row)

# Create the DataFrame from the list of rows
employees = pd.DataFrame(all_rows, columns=columns)

# Save the DataFrame to a CSV file
employees.to_csv('../csv/employees.csv', index=False, encoding='utf-8-sig')

# Print a success message and the head of the DataFrame
print('data svaed successfully!')
