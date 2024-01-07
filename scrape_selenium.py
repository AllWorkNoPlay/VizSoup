import json
import os
from trade_signal import TradeSignal

import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime

# Create a new Chrome browser instance
driver = webdriver.Chrome()
driver.get("https://finviz.com/")
driver.implicitly_wait(1)

# Find all tables with id containing 'signals' or has class 'signal-table'
volume_signal_tables = driver.find_elements(By.CSS_SELECTOR, 'table[id*="signals"]')
pattern_signal_tables = driver.find_elements(By.CSS_SELECTOR, 'table.hp_signal-table') 

# for each table, read the header and data rows
# store the data in TradeSignal objects
# the TradeSignal object's type is 'Volume' or 'Pattern' depending on the table type
# the TradeSignal object's properties are the table header names
# the TradeSignal object's values are the table data row values
# store the TradeSignal objects in a list
# each data row in the table will be a TradeSignal object in the list
# the list will contain TradeSignal objects for all data rows in all tables

# Create a list of TradeSignal objects
trade_signals = []

# iterate through the tables
# for each table, read the header and data rows
for table in volume_signal_tables:
    # read the header row
    headers = [th.text.strip() for th in table.find_element(By.CSS_SELECTOR, "thead").find_elements(By.TAG_NAME, "th")]
    # read the data rows
    data_rows = table.find_elements(By.TAG_NAME, 'tr')[1:]

    for row in data_rows:
        print(row.text)

    # iterate through the data rows
    for row in data_rows:
        # read the data cells
        data_cells = row.find_elements(By.TAG_NAME, "td")
        # create a TradeSignal object
        trade_signal = TradeSignal("volume", headers)
        # set the TradeSignal object's property values
        for i, cell in enumerate(data_cells):
            # set the property value, unless it is empty
            if cell.text.strip() != "":
                setattr(trade_signal, headers[i], cell.text.strip())
        # append the TradeSignal object to the list
        trade_signals.append(trade_signal)

for table in pattern_signal_tables:
    # read the header row
    headers = [th.text.strip() for th in table.find_element(By.CSS_SELECTOR, "thead").find_elements(By.TAG_NAME, "th")]
    
    print ("headers: ", headers)

    # read the data rows
    data_rows = table.find_elements(By.TAG_NAME, 'tr')[1:]
    # iterate through the data rows
    for row in data_rows:

        print("data: ", row.text)

        data_cells = row.find_elements(By.TAG_NAME, "td")
        
        # every row contains 4 tickers and a pattern, should be split into 4 rows
        for i in range(4):    
            # create a TradeSignal object
            trade_signal = TradeSignal("pattern", headers)
            setattr(trade_signal, headers[0], data_cells[i].text.strip())
            setattr(trade_signal, headers[1], data_cells[4].text.strip())
            # append the TradeSignal object to the list
            trade_signals.append(trade_signal)

 
# write the list of TradeSignal objects to a file, in a directory named 'output'
path = 'output/'

#for each type of table:
for type in ['volume', 'pattern']:
    # ensure a folder named 'output' exists
    if not os.path.exists(path):
        os.makedirs(path)
    
    filename = 'signal_' + type + '_' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
    with open(os.path.join(path, filename), 'w') as outfile:
        #select signals of that type
        signals = [signal for signal in trade_signals if signal.type == type]
        
        content = json.dumps(signals, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        outfile.write(content)


# Close the browser window
driver.quit()
