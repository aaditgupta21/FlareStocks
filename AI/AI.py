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



