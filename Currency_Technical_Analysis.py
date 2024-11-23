import pytz
import datetime
import pandas as pd
import numpy as np
print(np.__version__)
import streamlit as st
import matplotlib.pyplot as plt
from datetime import timedelta
import importlib
import MetaTrader5 as mt5


import Primary_Functions_v1
importlib.reload(Primary_Functions_v1)
from Primary_Functions_v1 import add_columns, add_rows, delete_columns, delete_row, rounding

import Simple_Moving_Average_v1
importlib.reload(Simple_Moving_Average_v1)
from Simple_Moving_Average_v1 import moving_average, ma

import Data_Download_v1
importlib.reload(Data_Download_v1)
from Data_Download_v1 import get_quotes, mass_import

import Performance_Analysis_v1
importlib.reload(Performance_Analysis_v1)
from Performance_Analysis_v1 import performance

import Relative_Strength_Index_v1
importlib.reload(Relative_Strength_Index_v1)
from Relative_Strength_Index_v1 import relative_strength_index


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

frequency = ['D1', 'H1', 'M15']
plotting_time_frame = ['YTD', 'Last 3 Months', 'Last Month', 'Last Week', 'Full History']

st.title("Currency Technical Analysis")
st.markdown("#### A simple app to download and apply technical analysis indicators to currency crosses")
st.sidebar.header("Display Parameters")



#######################################################
# Build user options
########################################################
ticker = st.sidebar.selectbox(
    "Ticker", assets
)

frequency_pick = st.sidebar.selectbox(
    "Data frequency", frequency
)

#######################################################
# import the chosen dataset through ST functionality
#######################################################

dataset, time_labels = mass_import(ticker, frequency_pick)

# Build DataFrame for ease of display
dataset_print = pd.DataFrame(dataset, columns=[f'{ticker} Open', f'{ticker} High', f'{ticker} Low', f'{ticker} Close'])
dataset_print['Date'] = pd.to_datetime(time_labels)  # Convert time labels back to DateTime
dataset_print.set_index('Date', inplace=True)


###################################################
# Show results
###################################################

st.write("OHLC Stock data for ", ticker, " given ", frequency_pick ,' frequency')
st.dataframe(dataset_print)
st.write(f'{ticker} Timeseries')
st.line_chart(dataset_print[f'{ticker} Close'])

###################################################
# Apply Indicator analyses
###################################################

st.markdown(f'### Technical analysis for {ticker} given {frequency_pick} frequency')
indicator_analysis = st.selectbox(
    "Technical Analysis", ['Simple Moving Average', 'Relative Strength Index']
)

if indicator_analysis == 'Simple Moving Average':
    moving_average(dataset, dataset_print, time_labels, frequency_pick, ticker)

elif indicator_analysis == 'Relative Strength Index':
    relative_strength_index(dataset, time_labels, ticker)