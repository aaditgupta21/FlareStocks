import warnings
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    warnings.filterwarnings('ignore', category=FutureWarning)
    import tensorflow as tf
    import numpy as np
    import pandas as pd
    from sklearn import preprocessing
    import sys
    import os
    import time
    import pickle



os.chdir('../')
sys.path.append(os.getcwd())

tf.compat.v1.enable_eager_execution()

def load_data(company):
    data = pd.DataFrame()
    if os.path.exists(f'data/stocks/{company}/{company}.pkl'):
        data_ = pd.read_pickle(f'data/stocks/{company}/{comapny}.pkl')
        data = pd.DataFrame(data_)
        data.set_index('date', inplace=True)
        data.drop(columns=['volume', 'adjClose', 'adjHigh', 'adjLow', 'adjOpen', 'adjVolume', 'divCash', 'splitFactor'], inplace=True)
    return data

def create_model(company, x, y, x_val, y_val): 
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(64, activation='linear'))
    model.add(tf.keras.layers.Dense(32, activation='linear'))
    model.add(tf.keras.layers.Dense(16, activation='linear'))
    lower_rate = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.9, patience=0, min_lr=0.00001, mode='min', verbose=1)
    checkpoint = tf.keras.callbacks.ModelCheckpoint(f'ai/models/{company}.h5', save_best_only=True, verbose=1)
    early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=8, baseline=0.1)
    board = tf.keras.callbacks.TensorBoard(log_dir='logs', histogram_freq='0', write_graph="True", write_images='False', update_Freq="epoch",profil_batch='2', embeddings_freq='20', embeddings_metadata=None)
    model.compile(optimizer=tf.keras.optimizers.Adam(0.1), loss='mean_absolute_error')
    model.fit(x=x, y=y, validation_data=(x_val, y_val), epochs=100, callbacks=[lower_rate, checkpoint, early, board], verbose=1)
    return model

def train():
    start = time.time()
    


if __name__ == "__main__":
    train()