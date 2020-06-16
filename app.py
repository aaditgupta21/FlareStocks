import os
from flask import Flask, render_template, make_response, request, jsonify
import threading
import pickle

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route('/')
def index():
    return render_template('index.html', names=get_names())

def get_desc():
    data = []
    if os.path.exists('data/tickers.pkl'):
        with open('data/tickers.pkl', 'rb') as f:
            tickers = pickle.load(f)

    for ticker in tickers:
        if os.path.exists('data/stocks/{}'.format(ticker)) and not os.path.isfile('/data/stocks/{}'.format(ticker)):
            if os.listdir('data/stocks/{}'.format(ticker)):
                with open('data/stocks/{}'.format(ticker)) as f:
                    desc = pickle.load(f)
                data.append(desc)
    
    return data

def get_names():
    name = []
    for desc in get_desc():
        name.append(desc.get('name'))
    return name


@app.route('/graph', methods=['POST'])
def graph():
    data_symbol = ''
    for desc in get_desc():
        if desc.get('name') == request.form['name']:
            data_symbol = desc.get('ticker')

    x = [['Date', 'Stock Price', 'Predictions']]
    with open('data/stocks/{}/{}.pkl'.format(data_symbol, data_symbol), "rb") as f:
        data = pickle.load(f)
    for day in data:
        x.append([day.get('date')[:day.get('date').index('T')], day.get('close'), None])

    if os.path.exists('AI/trained/{}.pkl'.format(data_symbol)):
        with open('AI/trained/{}.pkl'.format(data_symbol), "rb") as f:
            trained = pickle.load(f)
        x.append([trained[0].get('date'), trained[0].get('close'), trained[0].get('close')])
        for day in trained:
            x.append([day.get('date'), None, day.get('close')])

    return jsonify({'x': x})
