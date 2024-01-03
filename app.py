import camelot
import pandas as pd
import numpy as np
import os
import shutil


def get_stmt_dates(filename, directory):
    # Read the PDF
    data = camelot.read_pdf(filename, pages='all')

    # Convert each table into a DataFrame and store them in a list
    df_list = [table.df for table in data]

    # Concatenate all the DataFrames in the list into a single DataFrame
    df = pd.concat(df_list, ignore_index=True)

    # Make the first row the name
    df.columns = ['date', 'description', 'debit', 'credit', 'balance']
    df = df.drop(df.index[0])

    #Use the [] operator to select all rows from the df where the value in the 'credit' column is not an empty string
    df = df[df['credit'] != '']

    # Get unique values in 'date' column
    unique_values = df['date'].unique()

    # Replace '/' with '-' in each element
    unique_values = np.array([str(item).replace('/', '_') for item in unique_values])
    # mkdir all the dates from bank statement into printable
    for dirnames in unique_values:
        os.makedirs(printable_dir + os.sep + dirnames)


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