import pandas as pd
import os

# --- Configuration ---

# <<< CHANGE HERE >>>
# Set the relative path to the folder containing your CSV files.
data_directory = '../csv' 

# The names of your CSV files and their date columns.
# The script will look for these files inside the data_directory.
files_and_date_columns = {
    'employees.csv': ['join_date', 'termination_date'],
    'clients.csv': ['join_date'],
    'transactions.csv': ['transaction_date'],
    'accounts.csv': ['date_opened'],
    'loans.csv': ['start_date', 'end_date']
}

# --- Script Logic ---

all_dates = []

print(f"Scanning for CSV files in directory: '{os.path.abspath(data_directory)}'")

# Create the data directory if it doesn't exist, to prevent errors.
os.makedirs(data_directory, exist_ok=True)

# Loop through each file and its specified date columns
for filename, date_cols in files_and_date_columns.items():
    # <<< CHANGE HERE >>>
    # Construct the full path to the CSV file
    full_path = os.path.join(data_directory, filename)

    if os.path.exists(full_path):
        try:
            # Read from the full path
            df = pd.read_csv(full_path) 
            for col in date_cols:
                if col in df.columns:
                    valid_dates = pd.to_datetime(df[col], errors='coerce').dropna()
                    all_dates.extend(valid_dates)
            print(f"  - Processed {full_path}")
        except Exception as e:
            print(f"Could not process {full_path}. Error: {e}")
    else:
        print(f"  - WARNING: {filename} not found in '{data_directory}', skipping.")


if not all_dates:
    # A helpful error message if no data is found
    print("\n--- ERROR ---")
    print("No dates found in any of the files. Cannot create calendar.")
    print("Please check that:")
    print(f"1. Your CSV files are located in the '{os.path.abspath(data_directory)}' directory.")
    print("2. The filenames in the script match your actual filenames.")
    print("3. The date columns in the script exist in your CSVs and contain data.")
    exit() # Exit the script

# Find the overall minimum and maximum date
min_date = min(all_dates).date()
max_date = max(all_dates).date()

print(f"\nDate range identified: from {min_date} to {max_date}")

# Create a continuous date range
date_range = pd.date_range(start=min_date, end=max_date, freq='D')

# Create the calendar DataFrame
calendar_df = pd.DataFrame({'date': date_range})

print("Generating calendar attributes...")

# Add useful calendar columns
calendar_df['year'] = calendar_df['date'].dt.year
calendar_df['quarter_of_year'] = calendar_df['date'].dt.quarter
calendar_df['month_number'] = calendar_df['date'].dt.month
calendar_df['month_name'] = calendar_df['date'].dt.month_name()
calendar_df['day_of_month'] = calendar_df['date'].dt.day
calendar_df['day_of_week_number'] = calendar_df['date'].dt.dayofweek # Monday=0, Sunday=6
calendar_df['day_of_week_name'] = calendar_df['date'].dt.day_name()
calendar_df['week_of_year'] = calendar_df['date'].dt.isocalendar().week
calendar_df['is_weekday'] = calendar_df['day_of_week_number'] < 5 # True for Monday-Friday

# Format the date column to be just YYYY-MM-DD
calendar_df['date'] = calendar_df['date'].dt.date

# --- Save the file ---
output_filename = 'calendar.csv'
# <<< CHANGE HERE >>>
# Construct the full output path to save the calendar in the same data directory
output_path = os.path.join(data_directory, output_filename)

calendar_df.to_csv(output_path, index=False)

print(f"\nSuccessfully created file at: '{os.path.abspath(output_path)}' with {len(calendar_df)} rows.")
print("\nFirst 5 rows of the calendar:")
print(calendar_df.head())