import pdfplumber
import pandas as pd
import numpy as np
import os
import shutil

# This function reads pdf and returns all tables in the pdf; up to others to concat and clean up
def extract_tables_from_pdf(pdf_path, headers=None): # headers=None will not use every first row as column headers
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

# This function get the statement credit dates and create folders according to them
def get_stmt_dates(filename, directory):

    df_list = extract_tables_from_pdf(filename)

    # Concatenate all DataFrames in the list into a single DataFrame
    df = pd.concat(df_list, ignore_index=True)

    # remove 1st row because it is the column header in public bank statement case
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

# This function returns date of the DHL COD bank transfer
def get_cod_date(filename):
    directory = "cod_statement" 
    pdf_path = os.path.join(directory, filename)
    tables = extract_tables_from_pdf(pdf_path)
    date = tables[1].iloc[1, 1]
    date = date.replace('.', '_')

    return(date)

# This function cp all COD statements into appropriate date folders in printable folder
def sort_cod():
    # ls COD statement directory and save it to names
    names = os.listdir('cod_statement')
    # loop through names and rm .ds_store
    for name in names:
        if(name == ".DS_Store"):
            os.remove("cod_statement/.DS_Store")

    # loop through names and move cod pdfs to the right date folder in printable directory
    for filename in names:
        date = get_cod_date(filename)
        source = os.path.join("cod_statement/", filename)
        destination = os.path.join("printable/", date+"/")
        shutil.copy(source, destination)

# this function returns the date in the name of the files
def get_slip_date(filename):
    # example filename: 02_10_2023 NO 877087117 LEE BENG SEE will return=02_10_2023
    return filename[:10]

# this function cp all files into the appropriate dates
def sort_bankslip():
    
    names = os.listdir('bank_slip') 

    for filename in names:
        date = get_slip_date(filename)
        source = os.path.join("bank_slip/", filename)
        destination = os.path.join("printable/", date+"/")
        shutil.copy(source, destination)


####################################### MAIN #################################################
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

    # remove statement directory if it already exist
    if os.path.exists('printable'):
        shutil.rmtree('printable')

    # Create a directory called printable
    printable_dir = os.path.join(directory, 'printable')
    if not os.path.isdir(printable_dir):
        os.makedirs(printable_dir)
    
    # Build the path to bank_statement.pdf
    stmt_path = os.path.join(directory, 'bank_statement.pdf')
    # Start mkdir for all dates credit
    get_stmt_dates(stmt_path, printable_dir)

    sort_cod()
    sort_bankslip()
    
    print("Success you JIBAI kia!")