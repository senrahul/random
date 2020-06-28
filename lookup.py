import pandas as pd
from pandas import ExcelWriter
import argparse
import pdb

parser = argparse.ArgumentParser()
parser.add_argument('--crawled_filepath', required=True,
                    help='Please provide the crawled file path')
parser.add_argument('--db_filepath', required=True,
                    help='Please provide the crawled file path')

args, unknown_args = parser.parse_known_args()
db_filepath = args.db_filepath
crawled_filepath = args.crawled_filepath





def read_file_as_df(filepath):
    df = pd.read_excel(filepath)
    return df


def lookup_software_names(software_name, all_names):
    match_found = False
    software_name = software_name.lower().strip()
    print(software_name)
    if any(software_name in db_software_name for db_software_name in all_names):
        match_found = True
    print(software_name, match_found)
    return match_found

def write_df_to_excel(df, output_filepath):
    writer = ExcelWriter(output_filepath)
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()

def start():
    # reading files into pandas DataFrame
    crawled_df = read_file_as_df(crawled_filepath)
    db_df = read_file_as_df(db_filepath)
    print(crawled_df)
    print(db_df)

    all_names = list(db_df['software_name'])

    #removing leading or trailing spaces and converting all names to lowercase
    all_names = [name.lower().strip() for name in all_names]


    #adding a new column 'found_in_db' in crawl_df initialize all rows with 'False'
    crawled_df['found_in_db'] = False

    # Storing the flag, weather the software found in db or not
    for index, row in crawled_df.iterrows():
        print(row)
        crawled_df.at[index, 'found_in_db'] = lookup_software_names(row["software_name"], all_names)
    #write df to new excel
    write_df_to_excel(crawled_df, 'crawled_output.xlsx')

if __name__ == "__main__":
    start()