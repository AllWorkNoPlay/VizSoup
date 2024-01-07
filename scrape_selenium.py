import json
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime

# Create a new Chrome browser instance
driver = webdriver.Chrome()
driver.get("https://finviz.com/")
driver.implicitly_wait(1)

mytables = []

# Find all tables with id containing 'signals' or has class 'signal-table'
vol_signal_tables = driver.find_elements(By.CSS_SELECTOR, 'table[id*="signals"]')
pattern_signal_tables = driver.find_elements(By.CSS_SELECTOR, 'table.signal-table')

# verify that we found 2 volume signal tables and 2 pattern signal tables
assert len(vol_signal_tables) == 2, "Expected 2 tables, found " + str(len(vol_signal_tables)) + " tables"
assert len(pattern_signal_tables) == 2, "Expected 2 tables, found " + str(len(pattern_signal_tables)) + " tables"

# verify that same type of tables have the same headers
assert vol_signal_tables[0].find_element(By.CSS_SELECTOR, "thead").text == vol_signal_tables[1].find_element(By.CSS_SELECTOR, "thead").text, "Volume Signal tables have different headers"
assert pattern_signal_tables[0].find_element(By.CSS_SELECTOR, "thead").text == pattern_signal_tables[1].find_element(By.CSS_SELECTOR, "thead").text, "Pattern Signal tables have different headers"


# Extract the data from the tables
# Ensure there will be one table for each type of signal, having one header row and all data rows from the corresponding tables


def extract_and_append_table_data(table, table_type):
    mytable = next((item for item in mytables if item["type"] == table_type), None)
    if mytable is None:
        headers = [th.text.strip() for th in table.find_element(By.CSS_SELECTOR, "thead").find_elements(By.TAG_NAME, "th")]
        mytable = {"type": table_type, "headers": headers, "data": []}
        mytables.append(mytable)
    data_rows = table.find_elements(By.TAG_NAME, 'tr')[1:]
    mytable["data"].append( [[td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")] for row in data_rows])

table_types_and_tables = {"volume_signal": vol_signal_tables, "pattern_signal": pattern_signal_tables}

for table_type, tables in table_types_and_tables.items():
    for i, table in enumerate(tables):
        if i == 0:
            extract_and_append_table_data(table, table_type)
        else:
            # select the mytables entry with the same type as the current table
            mytable = next((item for item in mytables if item["type"] == table_type), None)
            table["data"].extend(mytable["data"])
 
for table in mytables:
    filename = table["type"] + '_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    with open(filename, 'w') as outfile:
        json.dump(table, outfile, indent=4)

# Close the browser window
driver.quit()
