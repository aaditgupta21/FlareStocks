import os
import pickle
import threading

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def meta_data():
    data = []
    if os.path.exists("data/tickers.pkl"):
        with open("data/tickers.pkl", "rb") as f:
            symbols = pickle.load(f)

    for symbol in symbols:
        if os.path.exists('data/stocks/{}'.format(symbol)) and not os.path.isfile('data/stocks/{}'.format(symbol)):
            if os.listdir('data/stocks/{}'.format(symbol)):
                with open('data/stocks/{}/desc.pkl'.format(symbol), "rb") as f:
                    meta = pickle.load(f)
                data.append(meta)

    return data


def names():
    _names = []
    for meta in meta_data():
        _names.append(meta.get('name'))
    return _names


@app.route('/')
def home():
    return render_template('index.html', names=names())


@app.route('/company')
def company():
    return render_template('company.html', names=names())



@app.route('/select', methods=['POST'])
def select():
    name = request.form['name']
    for meta in meta_data():
        if meta.get('name') == name:
            return jsonify(meta)
    return jsonify({'name': name, 'description': 'error'})


@app.route('/graph', methods=['POST'])
def graph():
    data_symbol = ''
    for meta in meta_data():
        if meta.get('name') == request.form['name']:
            data_symbol = meta.get('ticker')

    x = [['Date', 'Stock Price', 'Predictions']]
    with open('data/stocks/{}/{}.pkl'.format(data_symbol, data_symbol), "rb") as f:
        data = pickle.load(f)
    for day in data:
        x.append([day.get('date')[:day.get('date').index('T')],
                  day.get('close'), None])

    if os.path.exists('AI/trained/{}.pkl'.format(data_symbol)):
        with open('AI/trained/{}.pkl'.format(data_symbol), "rb") as f:
            prediction = pickle.load(f)
        x.append([prediction[0].get('date'), prediction[0].get(
            'close'), prediction[0].get('close')])
        for day in prediction:
            x.append([day.get('date'), None, day.get('close')])

    return jsonify({'x': x})


@app.route('/search', methods=['POST'])
def search():
    name = request.form['name']
    for meta in meta_data():
        if meta.get('name') == name:
            return jsonify({'name': meta.get('name')})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5005)

