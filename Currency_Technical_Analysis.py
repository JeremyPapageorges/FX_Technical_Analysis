import pytz
import datetime
import pandas as pd
import numpy as np
print(np.__version__)
import streamlit as st
import MetaTrader5 as mt5
import matplotlib.pyplot as plt
from datetime import timedelta


###################################################
# import different timeframes
###################################################

frame_M15 = mt5.TIMEFRAME_M15 # 15 - minute time
frame_M30 = mt5.TIMEFRAME_M30
frame_H1 = mt5.TIMEFRAME_H1
frame_H4 = mt5.TIMEFRAME_H4
frame_D1 = mt5.TIMEFRAME_D1
frame_W1 = mt5.TIMEFRAME_W1
frame_M1 = mt5.TIMEFRAME_MN1


# set the current date and time
now = datetime.datetime.now()

###################################################
# Complete list of currencies
###################################################

assets = [
    'EURUSD', 'GBPUSD', 'USDCHF', 'USDJPY', 'USDCNH', 'AUDUSD', 'NZDUSD', 
    'USDCAD', 'USDSEK', 'SEKNOK', 'SGDHKD', 'SGDJPY', 'TRYJPY', 'USDARS', 
    'USDBRL', 'USDCLP', 'USDCOP', 'USDCRE', 'USDCZK', 'USDDKK', 'USDGEL', 
    'USDHKD', 'USDHUF', 'USDILS', 'USDMXN', 'USDNOK', 'USDPLN', 'USDRMB', 
    'USDRUB', 'USDRUR', 'USDSGD', 'USDTHB', 'USDTRY', 'USDZAR', 'ZARJPY', 
    'XAUUSD', 'XAUEUR', 'XAUAUD', 'XAGUSD', 'XAGEUR', 'XPDUSD', 'XPTUSD', 
    'XAGAUD', 'EURZAR', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPCZK', 'GBPDKK', 
    'GBPHKD', 'GBPHUF', 'GBPMXN', 'GBPNOK', 'GBPNZD', 'GBPPLN', 'GBPSEK', 
    'GBPSGD', 'GBPTRY', 'GBPZAR', 'HKDJPY', 'MXNJPY', 'NOKDKK', 'NOKJPY', 
    'NOKSEK', 'NZDCAD', 'NZDCHF', 'NZDDKK', 'NZDHUF', 'NZDJPY', 'NZDMXN', 
    'NZDNOK', 'NZDSEK', 'NZDSGD', 'PLNJPY', 'SEKJPY', 'CHFHUF', 'CHFJPY', 
    'CHFMXN', 'CHFNOK', 'CHFPLN', 'CHFSEK', 'CHFSGD', 'CHFTRY', 'CHFZAR', 
    'CNHJPY', 'DKKJPY', 'DKKNOK', 'DKKSEK', 'EURAUD', 'EURCAD', 'EURCHF', 
    'EURCNH', 'EURCZK', 'EURDKK', 'EURGBP', 'EURHKD', 'EURHUF', 'EURILS', 
    'EURJPY', 'EURMXN', 'EURNOK', 'EURNZD', 'EURPLN', 'EURRUB', 'EURRUR', 
    'EURSEK', 'EURSGD', 'EURTRY', 'EURZAR'
]

frequency = ['D1', 'H1', 'M30', 'M15']
plotting_time_frame = ['YTD', 'Last 3 Months', 'Last Month', 'Last Week', 'Full History']


###################################################
# Build basic functions
###################################################

# Primal functions

def add_columns(data, times):
    for i in range(1, times + 1):
        new = np.zeros((len(data), 1), dtype = float)
        data = np.append(data, new, axis = 1)
    return data    

def delete_columns(data, index, times):
    for i in range (1, times+ 1):
        data = np.delete(data, index, axis = 1)
    
    return data

def add_rows(data,times):
    for i in range(1, times +1):
        columns = np.shape(data)[1]
        new = np.zeros((1, columns), dtype = float)
        data = np.append(data, new, axis = 0)
    return data

def delete_row(data, number):
    data = data[number:,]
    return data

def rounding(data, how_far):
    data = data.round(decimal = how_far)

    return data

###################################################
# Build data import functions
###################################################

def get_quotes(time_frame, year = '2014' , month = 1, day = 1, asset = 'EURUSD'):
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    timezone = pytz.timezone("Europe/Paris")
    time_from = datetime.datetime(year, month, day, tzinfo= timezone)
    time_to = datetime.datetime.now(timezone) + datetime.timedelta(days=1)

    rates = mt5.copy_rates_range(asset, time_frame, time_from, time_to)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')  # Convert time to DateTime
    return rates_frame

def mass_import(asset_ticker, time_frame):
    if time_frame == 'H1':
        data = get_quotes(frame_H1, 2018,1,1, asset = asset_ticker)
        print(data.head(5))
        time_labels = data['time'].to_numpy()

        data = data[['open', 'high', 'low', 'close']].to_numpy() # transforms into a numpy array
        data = data.round(decimals = 5)
    
    if time_frame =='M30':
        data = get_quotes(frame_M30, 2023,1,1, asset = asset_ticker)
        print(data.head(5))
        time_labels = data['time'].to_numpy()
        data = data[['open', 'high', 'low', 'close']].to_numpy() # transforms into a numpy array
        data = data.round(decimals = 5)

    if time_frame =='M15':
        data = get_quotes(frame_M15, 2024,1,1, asset = asset_ticker)
        print(data.head(5))
        time_labels = data['time'].to_numpy()
        data = data[['open', 'high', 'low', 'close']].to_numpy() # transforms into a numpy array
        data = data.round(decimals = 5)

    if time_frame == 'D1':
        data = get_quotes(frame_D1, 2014,1,1, asset = asset_ticker)
        print(data.head(5))
        time_labels = data['time'].to_numpy()
        data = data[['open', 'high', 'low', 'close']].to_numpy() # transforms into a numpy array
        data = data.round(decimals = 5)
    return data, time_labels


###################################################
# Technical analysis functions
###################################################

def ma(data, lookback, close, position):
    data = add_columns(data,1)

    for i in range(len(data)):
        try:
            data[i, position] = (data[i- lookback + 1: i + 1, close].mean())
        except IndexError:
            pass
    data = delete_row(data, lookback)

    return data

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

###################################################
# import the chosen dataset through ST functionality
###################################################


st.title("Currency Technical Analysis")
st.write("A simple app to download and apply technical analysis indicators to currency crosses")
st.sidebar.header("Display Parameters")


ticker = st.sidebar.selectbox(
    "Ticker", assets
)

frequency_pick = st.sidebar.selectbox(
    "Data frequency", frequency
)

dataset, time_labels = mass_import(ticker, frequency_pick)

dataset_print = pd.DataFrame(dataset, columns=[f'{ticker} Open', f'{ticker} High', f'{ticker} Low', f'{ticker} Close'])
dataset_print['Date'] = pd.to_datetime(time_labels)  # Convert time labels back to DateTime
dataset_print.set_index('Date', inplace=True)

st.write("OHLC Stock data for ", ticker, " given ", frequency_pick ,' frequency')
st.dataframe(dataset_print)

st.write(f"{frequency_pick} data for {ticker}")

###################################################
# Code moving averages
###################################################

if frequency_pick == "D1":
    # Get the current date
    current_date = datetime.datetime.now()
    # define plotting options when dealing with daily datasets
    plot_parameter = st.sidebar.selectbox(
    "Plotting Timeframe", ['YTD', 'Last 10 Years', 'Last 5 Years', 'Last 3 Years']
    )
    
    timeframe_delta = st.selectbox(
        "Moving Average horizon delta", ['Monthly - Trimester', 'Weekly - Monthly']
    )

    if timeframe_delta == 'Monthly - Trimester':
        lookback_ST = 31
        lookback_LT = 150
        # were focusing on Monthly and trimester horizons when computing the moving averages
        ma_ST = ma(dataset, lookback_ST, 3, 4)
        ma_LT = ma(dataset, lookback_LT, 3, 4)

    elif timeframe_delta == 'Weekly - Monthly':
        lookback_ST = 7
        lookback_LT = 31
        # were focusing on Weekly and Monthly horizons when computing the moving averages
        ma_ST = ma(dataset, lookback_ST, 3, 4)
        ma_LT = ma(dataset, lookback_LT, 3, 4)
    
    ma_ST = pd.DataFrame(ma_ST, columns = ['Open', 'High', 'Low', 'Close', f'{ticker} ST Moving Average'])
    ma_ST['Date'] = pd.to_datetime(time_labels[lookback_ST:])
    ma_ST.set_index('Date', inplace=True)

    ma_LT = pd.DataFrame(ma_LT, columns = ['Open', 'High', 'Low', f'{ticker} Close', f'{ticker} LT Moving Average'])
    ma_LT['Date'] = pd.to_datetime(time_labels[lookback_LT:])
    ma_LT.set_index('Date', inplace=True)

    # Define the start dates for different plotting ranges
    if plot_parameter == 'YTD':
        start_date = datetime.datetime(current_date.year, 1, 1)
        filtered_data = dataset_print.loc[start_date:, f'{ticker} Close']
        filtered_ma_ST = ma_ST.loc[start_date:, f'{ticker} ST Moving Average']
        filtered_ma_LT = ma_LT.loc[start_date:, f'{ticker} LT Moving Average']

    elif plot_parameter == 'Last 10 Years':
        start_date = current_date - timedelta(days=365 * 10)  # Approx. 10 years
        filtered_data = dataset_print.loc[start_date:, f'{ticker} Close']
        filtered_ma_ST = ma_ST.loc[start_date:, f'{ticker} ST Moving Average']
        filtered_ma_LT = ma_LT.loc[start_date:, f'{ticker} LT Moving Average']

    elif plot_parameter == 'Last 5 Years':
        start_date = current_date - timedelta(days=365 * 5)  # Approx. 5 years
        filtered_data = dataset_print.loc[start_date:, f'{ticker} Close']
        filtered_ma_ST = ma_ST.loc[start_date:, f'{ticker} ST Moving Average']
        filtered_ma_LT = ma_LT.loc[start_date:, f'{ticker} LT Moving Average']

    elif plot_parameter == 'Last 3 Years':
        start_date = current_date - timedelta(days=365 * 3)  # Approx. 3 years
        filtered_data = dataset_print.loc[start_date:, f'{ticker} Close']
        filtered_ma_ST = ma_ST.loc[start_date:, f'{ticker} ST Moving Average']
        filtered_ma_LT = ma_LT.loc[start_date:, f'{ticker} LT Moving Average']

# Plot the filtered data
st.write(f"{ticker} Time Series")
st.line_chart(filtered_data)
st.write("Moving average analysis")
ma_dataframe = pd.concat([filtered_ma_ST, filtered_ma_LT], axis = 1)
st.dataframe(ma_dataframe)
st.line_chart(ma_dataframe)

