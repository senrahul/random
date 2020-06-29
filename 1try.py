import pandas as pd
from bs4 import BeautifulSoup
import requests
import wget
import re
import pdb
import os
#### db file
# 

####  

def get_name(string):
    name = ""
    result = re.search(r"\/([^\/]+)-.+\#download$", string)
    if result:
        name = result.group(1).lower().strip()
    return name


def get_db_names():
    db_df = pd.read_excel("Product_Name_exclusion.xlsx")
    all_names = list(db_df['product_name'])
    #removing leading or trailing spaces and converting all names to lowercase
    all_names = [str(name).lower().strip() for name in all_names]
    return all_names

def lookup_software_names(software_name, all_names):
    match_found = False
    software_name = software_name.lower().strip()
    print(software_name)
    if any(software_name in db_software_name for db_software_name in all_names):
        match_found = True
    print(software_name, match_found)
    return match_found


def main():
    URL = 'https://www.softexia.com/windows/antivirus/zonealarm-free#download'
    current_product_name = get_name(URL)
    all_names = get_db_names()
    
    print("*"*30)
    print("Current Product Name:::", current_product_name)
    print("*"*30)

    present_in_db = lookup_software_names(current_product_name, all_names)
    print("present_in_db ::: ", present_in_db)
    
    r  = requests.get(URL)
    data = r.text
    soup = BeautifulSoup(data,'lxml')

    b=soup.find('div',id="tab-download")
    #extension to download
    extensions = ['.exe','.rar','.zip','.msi']

    for c in b.find_all('a',href=True):
        d=(c['href'])
        #print(d)
        #checking if those extension in urls
        if any(x in d for x in extensions):
            download_url=d
            print(download_url)
            if present_in_db:
                download_path = "present_in_db/"
            else:
                download_path = "not_in_db/"
            if not os.path.exists(download_path):
                os.mkdir(download_path)
            wget.download(download_url, download_path)

     
if __name__ == "__main__":
    main()