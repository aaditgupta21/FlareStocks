import os
import requests
import bs4
import pickle
import time
print("Starting")
start = time.time()


def get_tickers():
    resp = requests.get(
        'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    table = bs4.BeautifulSoup(resp.text, 'lxml').find(
        'table', {'class': 'wikitable sortable'})

    symbols = []
    for row in table.findAll('tr')[1:]:
        symbol = row.findAll('td')[0].text
        symbols.append(symbol.replace('\n', ''))

    with open("tickers.pkl", "wb") as f:
        pickle.dump(symbols, f)
    return symbols


def get_data():
    if not os.path.exists("tickers.pkl"):
        symbols = get_tickers()
    else:
        with open("tickers.pkl", "rb") as f:
            symbols = pickle.load(f)

    if not os.path.exists('stocks'):
        os.makedirs('stocks')

    for symbol in symbols:
        if not os.path.exists('stocks/{}'.format(symbol)):
            os.makedirs('stocks/{}'.format(symbol))

        if not os.path.exists('stocks/{}/meta.csv'.format(symbol)):
            try:
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token 31db9807b1b41a9e85229876c01472b6a4f263ed'
                }
                desc = requests.get(
                    "https://api.tiingo.com/tiingo/daily/{}?".format(symbol.replace('.', '-')), headers=headers)
                with open('stocks/{}/desc.pkl'.format(symbol), "wb") as f:
                    pickle.dump(desc.json(), f)
                    print(symbol + ' dumping')
            except Exception:
                print(symbol + ' not found')

        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Token 31db9807b1b41a9e85229876c01472b6a4f263ed'
            }
            eod = requests.get("https://api.tiingo.com/tiingo/daily/{}/prices?startDate=2019-01-02".format(
                symbol.replace('.', '-')), headers=headers)
            with open('stocks/{}/{}.pkl'.format(symbol, symbol), "wb") as f:
                pickle.dump(eod.json(), f)
        except Exception:
            print(symbol + ' not found')


if __name__ == '__main__':
    get_data()
    file_list = os.listdir("./stocks")
    sorted(file_list)
    print(f'Total time = {(time.time() - start) / 60} minutes')
    print("Done")
