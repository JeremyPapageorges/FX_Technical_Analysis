import importlib
import pandas as pd
import streamlit as st

import Primary_Functions_v1
importlib.reload(Primary_Functions_v1)
from Primary_Functions_v1 import add_columns, add_rows, delete_columns, delete_row, rounding

import Simple_Moving_Average_v1
importlib.reload(Simple_Moving_Average_v1)
from Simple_Moving_Average_v1 import moving_average, ma

def smoothed_ma(data, alpha, lookback, close, position):

    lookback = (2* lookback) - 1

    alpha = alpha / (lookback + 1.0)

    beta = 1- alpha

    data = ma(data, lookback, close, position)

    data[lookback + 1, position] = (data[lookback + 1, close] * alpha) + (data[lookback, position] * beta)


    for i in range(lookback + 2, len(data)):
        try:
            data[i, position] = (data[i, close] * alpha) + (data[i - 1, position] * beta)
        except IndexError:
            pass
    return data


def rsi(data, lookback, close, position):

    data = add_columns(data, 5)

    for i in range(len(data)):
        data[i, position] = data[i, close] - data[i-1, close]

    for i in range(len(data)):
        if data[i, position] > 0:
            data[i, position + 1] = data[i, position]
        elif data[i, position] < 0:
            data[i, position + 2] = abs(data[i, position])

    data = smoothed_ma(data, 2, lookback, position+ 1, position + 3)
    data = smoothed_ma(data, 2, lookback, position+ 2, position + 4)

    data[:, position + 5] = data[:, position + 3] / data[:, position + 4]
    data[:, position + 6] = (100 - (100/ (1 + data[:, position +5])))

    data = delete_columns(data, position, 6)
    data = delete_row(data, lookback)

    return data


def relative_strength_index(dataset, time_labels, ticker):

    lookback = 14
    data = rsi(dataset, lookback,3,4)

    # Adjust the time labels dynamically to match the number of rows in `data`
    adjusted_time_labels = time_labels[-len(data):]  # Take only the last `len(data)` entries

    rsi_data = pd.DataFrame(data, columns = [f'{ticker} Open', f'{ticker} High', f'{ticker} Low', f'{ticker} Close', f'{ticker} RSI'])
    rsi_data['Date'] = pd.to_datetime(adjusted_time_labels)
    rsi_data.set_index('Date', inplace = True)

    st.dataframe(rsi_data)
    st.write(f'{ticker} Relative Strength Index')
    st.line_chart(rsi_data[f'{ticker} RSI'])