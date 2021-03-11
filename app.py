import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import datetime

def get_soup(url):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    # make the request
    html = urlopen(url).read()
    # return the soup
    return bs(html, "html.parser")

def get_all_tables(soup):
    """Extracts and returns all tables in a soup object"""
    return soup.find_all("table")

def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    return headers

def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        # grab all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            # if no td tags, search for th tags
            # can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            # use regular td tags
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    return rows


def save_as_csv(table_name, headers, rows):
    path = r'C:\Users\Ashhar\Desktop\Quality Stock Selector Project\output\\'
    pd.DataFrame(rows, columns=headers).to_csv( path + f"{table_name}.csv")

def main(url):
    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    tables = get_all_tables(soup)
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers
        headers = get_table_headers(table)
        # get all the rows of the table
        rows = get_table_rows(table)
        # save table as csv file
        table_name = "Quality Stocks "+ str(datetime.datetime.now().date())
        print(f"[+] Saving {table_name}")
        save_as_csv(table_name, headers, rows)



url = "https://www.screener.in/screens/340704/Value-Investing/"
main(url)