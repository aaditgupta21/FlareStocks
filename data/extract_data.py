import os
import requests
import sys
import pickle
import bs4

def get_ticker():
    req = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    table = bs4.BeautifulSoup(req.text, 'lxml').find('table', {'class': 'wikitable sortable'})

    tickers = []
    for row in table.findAll('tr')[1:]:
        symbol = row.findAll('td')[0].text
        tickers.append(symbol.replace('\n', ''))
    with open("tickers.pkl", "wb") as f:
        pickle.dump(tickers,f)
    return tickers

def get_data():
    if not os.path.exists("tickers.pkl"):
        tickers = get_ticker()
    else:
        with open("tickers.pkl", "wb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stocks'):
        os.makedirs('stocks')

    for ticker in tickers:
        



if __name__ == '__main__':
    get_data()