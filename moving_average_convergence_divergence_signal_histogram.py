from pyti.exponential_moving_average import exponential_moving_average as ema
import numpy as np


def macd_signal(data):
    # data is macd
    signal = ema(data, 9)
    return signal


def macd_histogram(data1, data2):
    # data1 - macd
    # data2 - macds
    hist = list(np.array(data1) - np.array(data2))
    return hist
