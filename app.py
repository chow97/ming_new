import pdfplumber
import pandas as pd
import numpy as np
import os

def extract_tables_from_pdf(pdf_path, headers=None):
    all_tables = []  # List to store all DataFrames

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if headers:
                    df = pd.DataFrame(table, columns=headers)  # Use provided headers
                else:
                    df = pd.DataFrame(table)  # No headers provided, use default indexing
                all_tables.append(df)

    return all_tables

def get_stmt_dates(filename, directory):

    df_list = extract_tables_from_pdf(filename)

    # Concatenate all DataFrames in the list into a single DataFrame
    df = pd.concat(df_list, ignore_index=True)

    df.drop(index=0, inplace=True)
    # Rename columns assuming the first row is the header
    df.columns = ['date', 'description', 'debit', 'credit', 'balance']

    # Filter out rows where 'credit' column is not an empty string
    df = df[df['credit'] != '']

    # Get unique values in 'date' column
    unique_values = df['date'].unique()

    # Replace '/' with '-' in each element
    unique_values = np.array([str(item).replace('/', '_') for item in unique_values])

    # Make directories for each unique date
    for dirnames in unique_values:
        os.makedirs(os.path.join(directory, dirnames), exist_ok=True)




############# MAIN #################################################
if __name__ == "__main__":
    # Prompt the user for the folder name
    folder_name = input("Please enter the folder name: ")
    # organize_files(folder_name)

    # Get the home directory of the current user
    user_home = os.path.expanduser('~')
    # Construct the absolute path
    directory = os.path.join(user_home, 'Desktop', folder_name)

    os.chdir(directory)
    # Command to remove all .DS_Store files
    command = "find . -type f -name '.DS_Store' -exec rm {} +"

    # Execute the command
    os.system(command)

    printable_dir = os.path.join(directory, 'printable')
    if not os.path.isdir(printable_dir):
        os.makedirs(printable_dir)
    
    stmt_path = os.path.join(directory, 'bank_statement.pdf')
    # Start mkdir for all dates credit
    get_stmt_dates(stmt_path, printable_dir)