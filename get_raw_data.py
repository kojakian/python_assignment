from datetime import datetime, timedelta
import sqlite3
import requests
import sys

print("Setting database")

with open('apikey.txt') as f:
    data = f.read()
    if "replace" in data:
        sys.exit("no API key set in apikey.txt")
    apikey = data.strip()

con = sqlite3.connect("schema.sql")
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS financial_data (
    symbol TEXT, 
    date TEXT,
    open_price REAL,
    close_price REAL,
    volume INTEGER );''')

symbol = ["IBM","AAPL"]
for stockname in symbol:
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+stockname+'&interval=5min&apikey='+apikey
    r = requests.get(url)
    data = r.json()

    start= datetime.today().strftime('%Y-%m-%d')
    end= (datetime.now() - timedelta(14)).strftime('%Y-%m-%d')

    try:
        stock = list(data.values())[1]
    except IndexError:
        print(data.values())
        break
    output = []
    for key, value in stock.items():
        # ['1. open', '2. high', '3. low', '4. close', '5. adjusted close', '6. volume', '7. dividend amount', '8. split coefficient']
        day_stock = list(value.values())
        res = cur.execute('''SELECT * FROM financial_data 
                WHERE symbol = '{}' AND date = '{}' '''.format(stockname,key))
        if res.fetchone():
            pass
        else:
            cur.execute("""
                INSERT INTO financial_data VALUES
                    ('{}', '{}', {}, {}, {})
                """.format(stockname, key, day_stock[0], day_stock[3], day_stock[5] ))
            con.commit()
        if (key == end):
            break
con.close()
print("Database set")