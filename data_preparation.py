# Function to convert Excel to CSV
import os
import pandas as pd

#Function to convert Excels into CSVs
def excel_to_csv(input_file, output_dir):
    # Read the Excel file
    excel_data = pd.read_excel(input_file, sheet_name=None, keep_default_na=False)

    # Loop through the sheets
    for sheet_name, df in excel_data.items():
        # Fill empty cells with an empty string
        df.fillna(value="", inplace=True)

        # Create CSV file path
        csv_file_path = output_dir + f'output_{sheet_name}.csv'

        # Save DataFrame as CSV
        df.to_csv(csv_file_path, index=False, encoding='utf-8')

# Convert the first Excel file
excel_to_csv('data/input/excel/Polifonia_lexicon_Total_first_version.xlsx', 'data/input/csv_to_compare/initial_csv/')
excel_to_csv('data/input/excel/Polifonia_lexicon_Total_V1_final.xlsx', 'data/input/csv_to_compare/final_csv/')

# Function to compare 2 CSV files of the Lexicon (The 'initial' and the 'final' one) to separate
# the lexicon entries that have been automatically inherited from BabelNet and
# the lexicon entries that have been manually entered by Polifonia internships
def compare_lexicon_files(first_csv, final_csv, language):
    # Prepare the column name based on the language
    lemma_column = f'lemmata {language.upper()}'

    # Read the first and final CSV files
    first_df = pd.concat(map(pd.read_csv, [first_csv]))
    final_df = pd.concat(map(pd.read_csv, [final_csv]))

    # Process the first DataFrame
    first_df[lemma_column] = first_df[lemma_column].str.split(',')
    first_df = first_df.explode(lemma_column)
    first_df[lemma_column] = first_df[lemma_column].str.strip()
    first_df.drop_duplicates(inplace=True)

    # Process the final DataFrame
    final_df[lemma_column] = final_df[lemma_column].str.split(',')
    final_df = final_df.explode(lemma_column)
    final_df[lemma_column] = final_df[lemma_column].str.strip()
    final_df.drop_duplicates(inplace=True)

    # Create the automatic and manual DataFrames
    automatic_df = final_df[final_df[lemma_column].isin(first_df[lemma_column])]
    manual_df = final_df[~final_df[lemma_column].isin(first_df[lemma_column])]

    # Save the automatic and manual DataFrames to CSV and Excel files
    automatic_df.to_csv(f'data/input/csv_for_rdf/automatic_{language.upper()}.csv', index=False)
    automatic_df.to_excel(f'data/input/csv_for_rdf/automatic_{language.upper()}.xlsx', index=False)
    manual_df.to_csv(f'data/input/csv_for_rdf/manual_{language.upper()}.csv', index=False)
    manual_df.to_excel(f'data/input/csv_for_rdf/manual_{language.upper()}.xlsx', index=False)

compare_lexicon_files('/home/arianna/PycharmProjects/PolifoniaLexicon/data/input_2705/initial_csv/output_NL.csv', '/home/arianna/PycharmProjects/PolifoniaLexicon/data/input_2705/final_csv/output_NL.csv', 'NL')

# Function to filter CSV files by a specific column name and value
# Needed to filter out terms that are not related to music, according to manual validation
def filter_csv(directory, column_name, value):
    # Loop through all files in the directory using scandir
    for entry in os.scandir(directory):
        # Check if the entry is a file and ends with '.csv'
        if entry.is_file() and entry.name.endswith('.csv'):
            # Construct full file path
            file_path = entry.path

            # If dealing with large files, read and filter the CSV in chunks
            chunksize = 10 ** 6  # adjust this value to your needs
            chunks = []
            for chunk in pd.read_csv(file_path, chunksize=chunksize):
                filtered_chunk = chunk[chunk[column_name].notna() & (chunk[column_name] != value)]
                chunks.append(filtered_chunk)

            df = pd.concat(chunks, ignore_index=True)

            # Construct the output file path (appends '_filtered' to original file name)
            output_file_path = os.path.splitext(file_path)[0] + '_filtered.csv'

            # Save the DataFrame back to a CSV
            df.to_csv(output_file_path, index=False)

filter_csv('data/input/csv_for_rdf', 'is it related to music?', 'NO')

# Not used anymore
#def filter_csv_columns(file_path, columns_to_keep):
#    # If dealing with large files, read and filter the CSV in chunks
#    chunksize = 10 ** 6  # adjust this value to your needs
#    chunks = []
#    for chunk in pd.read_csv(file_path, chunksize=chunksize):
#        filtered_chunk = chunk[columns_to_keep]
#        chunks.append(filtered_chunk)

#    df = pd.concat(chunks, ignore_index=True)

    # Construct the output file path (appends '_filtered' to original file name)
#    output_file_path = file_path.replace('.csv', '_filtered.csv')

    # Save the DataFrame back to a CSV
#    df.to_csv(output_file_path, index=False)


'''
FIX GERMAN LEXICON FILES
Report PoS information for German files
'''

#
def update_csv_with_matching_values(csv_a_file, csv_b_file, output_file):
    # Read CSV A and CSV B
    df_a = pd.read_csv(csv_a_file)
    df_b = pd.read_csv(csv_b_file)

    # Merge CSV A and CSV B based on 'bn:id' column
    merged_df = pd.merge(df_a, df_b[['bn:id', 'pos']], how='left', left_on='bn:id', right_on='bn:id')

    # Add a new 'pos' column to CSV A and populate it with values from CSV B
    df_a['pos'] = merged_df['pos']

    # Save the updated DataFrame to a new CSV file
    df_a.to_csv(output_file, index=False)

    print("CSV file updated successfully.")

# Example usage
csv_a_file = '/home/arianna/PycharmProjects/PolifoniaLexicon/data/input_csv_for_rdf/automatic_DE_filtered.csv'
csv_b_file = '/home/arianna/PycharmProjects/PolifoniaLexicon/data/input_2705/initial_csv/output_DE.csv'
output_file = '/home/arianna/PycharmProjects/PolifoniaLexicon/data/input_csv_for_rdf/automatic_DE_filtered_fixed.csv'
update_csv_with_matching_values(csv_a_file, csv_b_file, output_file)