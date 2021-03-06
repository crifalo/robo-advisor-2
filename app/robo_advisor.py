# app/robo_advisor.py

#imported modules and packages

import time
import requests
import json
import csv
import os
from dotenv import load_dotenv
load_dotenv()

#function

def moneyformat(price):
    return '${:,.2f}'.format(price) 

#URLs: adapted from https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response

while True:
    try:
        api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
        stock_symbol = input("Please input the stock ticker you would like information on: ")
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock_symbol}&apikey={api_key}"
        user_input = requests.get(url)
        parsed_response = json.loads(user_input.text)
        last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    except KeyError:
            if len(stock_symbol) >=5:
                print("You entered the ticker incorrectly with too many characters. Expecting a properly-formed stock symbol like 'MSFT'. Please try again: ")
                continue
            elif not stock_symbol.isalpha():
                print("You entered the ticker incorrectly with a number. Expecting a properly-formed stock symbol like 'MSFT'. Please try again: ")
                continue
          
    else:
        break

#Info Inputs

parsed_response = json.loads(user_input.text)
time_series = parsed_response["Time Series (Daily)"]
date = list(time_series.keys())
last_day = date[0]
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
latest_close = time_series[last_day]["4. close"]

large_prices = []
small_prices = []

for chosen_date in date:
    large_price = time_series[chosen_date]["2. high"]
    large_prices.append(float(large_price))
    small_price = time_series[chosen_date]["3. low"]
    small_prices.append(float(small_price))

latest_high = max(large_prices)
latest_low = min(small_prices)

#Info Outputs

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "stock_prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file: 
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() 
    
    for chosen_date in date:
        everyday_prices = time_series[chosen_date]
        writer.writerow({
            "timestamp": chosen_date, 
            "open": everyday_prices["1. open"], 
            "high": everyday_prices["2. high"], 
            "low": everyday_prices["3. low"], 
            "close": everyday_prices["4. close"], 
            "volume": everyday_prices["5. volume"] 
            })

print("-------------------------")
print(f"SELECTED SYMBOL: {stock_symbol}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: ", time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"))
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {moneyformat(float(latest_close))}")
print(f"RECENT HIGH: {moneyformat(float(latest_high))}")
print(f"RECENT LOW: {moneyformat(float(latest_low))}")
print("-------------------------")

potential_buy = 1.15*float(latest_low)

if potential_buy > float(latest_close):
    print("RECOMMENDATION: BUY!")
    print("RECOMMENDATION REASON: The latest closing price is less than '15%' of the recent low.")
else:
    print("DO NOT BUY!")
    print("RECOMMENDATION REASON: The latest closing price is greater than '15%' of the recent low.")

print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
