import pdfplumber
import pandas as pd
import numpy as np
import os

def get_stmt_dates(filename, directory):
    # Initialize an empty list to store DataFrames
    df_list = []

    # Open the PDF
    with pdfplumber.open(filename) as pdf:
        # Iterate over each page in the PDF
        for page in pdf.pages:
            # Extract tables from the current page
            for table in page.extract_tables():
                # Convert the table to a DataFrame and append to list
                df_list.append(pd.DataFrame(table[1:], columns=table[0]))

    # Concatenate all DataFrames in the list into a single DataFrame
    df = pd.concat(df_list, ignore_index=True)

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

# Usage example:
# get_stmt_dates('path_to_pdf', 'path_to_directory')

# import camelot
# import pandas as pd
# import numpy as np
# import os
# import shutil

# from ctypes.util import find_library
# find_library("gs")

# gs_path = '/opt/homebrew/bin/gs'
# if os.path.isfile(gs_path):
#     os.environ['PATH'] += os.pathsep + os.path.dirname(gs_path)

# def get_stmt_dates(filename, directory):
#     # Read the PDF
#     data = camelot.read_pdf(filename, pages='all')

#     # Convert each table into a DataFrame and store them in a list
#     df_list = [table.df for table in data]

#     # Concatenate all the DataFrames in the list into a single DataFrame
#     df = pd.concat(df_list, ignore_index=True)

#     # Make the first row the name
#     df.columns = ['date', 'description', 'debit', 'credit', 'balance']
#     df = df.drop(df.index[0])

#     #Use the [] operator to select all rows from the df where the value in the 'credit' column is not an empty string
#     df = df[df['credit'] != '']

#     # Get unique values in 'date' column
#     unique_values = df['date'].unique()

#     # Replace '/' with '-' in each element
#     unique_values = np.array([str(item).replace('/', '_') for item in unique_values])
#     # mkdir all the dates from bank statement into printable
#     for dirnames in unique_values:
#         os.makedirs(printable_dir + os.sep + dirnames)


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