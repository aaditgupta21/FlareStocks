import tempfile
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    warnings.filterwarnings('ignore', category=FutureWarning)
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    import tensorflow as tf
    import numpy as np
    import pandas as pd
    from sklearn import preprocessing
    import sys
    import os
    import pickle
    import time


os.chdir('../')
sys.path.append(os.getcwd())

tf.compat.v1.enable_eager_execution()


def load_data(symbol):
    df = pd.DataFrame()
    if os.path.exists(f'data/stocks/{symbol}/{symbol}.pkl'):
        df_ = pd.read_pickle(f'data/stocks/{symbol}/{symbol}.pkl')
        df = pd.DataFrame(df_)
        df.set_index('date', inplace=True)
        df.drop(columns=['volume', 'adjClose', 'adjHigh', 'adjLow',
                         'adjOpen', 'adjVolume', 'divCash', 'splitFactor'], inplace=True)
    return df


def make_model(symbol, x, y, val_x, val_y):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(32, activation='linear'))
    model.add(tf.keras.layers.Dense(64, activation='linear'))
    model.add(tf.keras.layers.Dense(4, activation='linear'))
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', factor=0.8, patience=0, min_lr=0.00001, mode='min', verbose=1)
    check = tf.keras.callbacks.ModelCheckpoint(
        f'ai/models/{symbol}.h5', save_best_only=True, verbose=1)
    early = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=10, baseline=0.1)
    model.compile(optimizer=tf.keras.optimizers.Adam(
        0.1), loss='mean_absolute_error')
    model.fit(x=x, y=y, validation_data=(val_x, val_y), epochs=100,
              callbacks=[reduce_lr, check, early], verbose=1)
    return model


if __name__ == "__main__":

    start = time.time()

    if not os.path.exists('ai/models'):
        os.mkdir('ai/models')
    if not os.path.exists('data/stocks'):
        os.mkdir('data/stock_data')
    if not os.path.exists('ai/trained'):
        os.mkdir('ai/trained')
    if not os.path.exists("data/tickers.pkl"):
        print('Run "extract_data.py" first to populate stock data')
        exit()
    else:
        with open("data/tickers.pkl", "rb") as f:
            symbols = pickle.load(f)
    if len(os.listdir('data/stocks')) == 0:
        print('Run "data.py" first to populate stock data')
        exit()

    for symbol in symbols:
        df = load_data(symbol).tail(1500)
        if df.empty:
            print(f'{symbol} is not availible at this time')
            continue
        if df.shape[0] < 300:
            print(f'{symbol} does not have enough data')
            continue

        date = df.index.astype('datetime64[ns]')

        normalizer = preprocessing.MinMaxScaler()
        df = normalizer.fit_transform(df)

        a = int(-df.shape[0] * .2)

        train = df[:a]
        val = df[a:]

        x = train[:-1]
        y = train[1:]

        val_x = val[:-1]
        val_y = val[1:]

        model = make_model(symbol, x, y, val_x, val_y)
        try:
            predict = model.predict(np.array([df[-1]]))
        except:
            print(sys.exc_info[0])

        days = 99
        pred_dates = pd.date_range(
            start=date[-1]+pd.DateOffset(1), periods=days+1)

        for x in range(days):
            predict = np.append(predict, model.predict(
                np.array([predict[x]])), axis=0)

        df = normalizer.inverse_transform(df)
        predict = normalizer.inverse_transform(predict)

        predictions_ = pd.DataFrame(
            predict, columns=['close', 'high', 'low', 'open'])
        pred_dates = pred_dates.to_frame(index=False).rename(
            columns={0: 'date'}).astype('str')
        predictions = pred_dates.join(predictions_)
        predictions.drop(columns=['high', 'low', 'open'], inplace=True)

        with open(f'ai/trained/{symbol}.pkl', 'wb') as f:
            pickle.dump(predictions.to_dict(orient='records'), f)

        print(f'finished {symbol}')

    print(f'Total time = {(time.time() - start) / 60} minutes')
