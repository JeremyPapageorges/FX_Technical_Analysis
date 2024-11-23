import datetime
import pandas as pd
from datetime import timedelta
import streamlit as st
import importlib

import Primary_Functions_v1
importlib.reload(Primary_Functions_v1)
from Primary_Functions_v1 import add_columns, add_rows, delete_columns, delete_row, rounding

def ma(data, lookback, close, position):
    data = add_columns(data,1)

    for i in range(len(data)):
        try:
            data[i, position] = (data[i- lookback + 1: i + 1, close].mean())
        except IndexError:
            pass
    data = delete_row(data, lookback)

    return data

def moving_average(dataset,dataset_print,time_labels, frequency_pick, ticker):
    


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

        # Build Short term and long termm dataframes
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


    elif frequency_pick == 'H1':
        # Get the current date
        current_date = datetime.datetime.now()

        # define plotting options when dealing with hourly datasets
        plot_parameter = st.sidebar.selectbox(
        "Plotting Timeframe", ['YTD', 'Last 6 Months', 'Last 3 Months', 'Last Month']
        )
        
        timeframe_delta = st.selectbox(
            "Moving Average horizon delta", ['Weekly - Monthly', 'Daily - weekly']
        )

        if timeframe_delta == 'Weekly - Monthly':
            lookback_ST = 168
            lookback_LT = 730
            # were focusing on Monthly and trimester horizons when computing the moving averages
            ma_ST = ma(dataset, lookback_ST, 3, 4)
            ma_LT = ma(dataset, lookback_LT, 3, 4)

        elif timeframe_delta == 'Daily - weekly':
            lookback_ST = 24
            lookback_LT = 168
            # were focusing on Weekly and Monthly horizons when computing the moving averages
            ma_ST = ma(dataset, lookback_ST, 3, 4)
            ma_LT = ma(dataset, lookback_LT, 3, 4)
        
        # Build Short term and long termm dataframes
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

        elif plot_parameter == 'Last 6 Months':
            start_date = current_date - timedelta(days = 31 * 6)  # Approx. 10 years
            filtered_data = dataset_print.loc[start_date:, f'{ticker} Close']
            filtered_ma_ST = ma_ST.loc[start_date:, f'{ticker} ST Moving Average']
            filtered_ma_LT = ma_LT.loc[start_date:, f'{ticker} LT Moving Average']

        elif plot_parameter == 'Last 3 Months':
            start_date = current_date - timedelta(days = 31 * 3)  # Approx. 5 years
            filtered_data = dataset_print.loc[start_date:, f'{ticker} Close']
            filtered_ma_ST = ma_ST.loc[start_date:, f'{ticker} ST Moving Average']
            filtered_ma_LT = ma_LT.loc[start_date:, f'{ticker} LT Moving Average']

        elif plot_parameter == 'Last Month':
            start_date = current_date - timedelta(days= 31 * 1)  # Approx. 3 years
            filtered_data = dataset_print.loc[start_date:, f'{ticker} Close']
            filtered_ma_ST = ma_ST.loc[start_date:, f'{ticker} ST Moving Average']
            filtered_ma_LT = ma_LT.loc[start_date:, f'{ticker} LT Moving Average']

    elif frequency_pick == 'M15':
        # Get the current date
        current_date = datetime.datetime.now()

        # define plotting options when dealing with hourly datasets
        plot_parameter = st.sidebar.selectbox(
        "Plotting Timeframe", ['Last Month', 'Last Week', 'Last Day', 'Last 6 Hours']
        )
        
        timeframe_delta = st.selectbox(
            "Moving Average horizon delta", ['Daily - weekly', '6-hourly - Daily']
        )

        if timeframe_delta == 'Daily - weekly':
            lookback_ST = 96
            lookback_LT = 672
            # were focusing on Monthly and trimester horizons when computing the moving averages
            ma_ST = ma(dataset, lookback_ST, 3, 4)
            ma_LT = ma(dataset, lookback_LT, 3, 4)

        elif timeframe_delta == '6-hourly - Daily':
            lookback_ST = 24
            lookback_LT = 96
            # were focusing on Weekly and Monthly horizons when computing the moving averages
            ma_ST = ma(dataset, lookback_ST, 3, 4)
            ma_LT = ma(dataset, lookback_LT, 3, 4)
        
        # Build Short term and long termm dataframes
        ma_ST = pd.DataFrame(ma_ST, columns = ['Open', 'High', 'Low', 'Close', f'{ticker} ST Moving Average'])
        ma_ST['Date'] = pd.to_datetime(time_labels[lookback_ST:])
        ma_ST.set_index('Date', inplace=True)

        ma_LT = pd.DataFrame(ma_LT, columns = ['Open', 'High', 'Low', f'{ticker} Close', f'{ticker} LT Moving Average'])
        ma_LT['Date'] = pd.to_datetime(time_labels[lookback_LT:])
        ma_LT.set_index('Date', inplace=True)

        # Define the start dates for different plotting ranges
        if plot_parameter == 'Last Month':
            start_date = current_date - timedelta(days = 31)
            filtered_data = dataset_print.loc[start_date:, f'{ticker} Close']
            filtered_ma_ST = ma_ST.loc[start_date:, f'{ticker} ST Moving Average']
            filtered_ma_LT = ma_LT.loc[start_date:, f'{ticker} LT Moving Average']

        elif plot_parameter == 'Last Week':
            start_date = current_date - timedelta(days = 7)  # Approx. 10 years
            filtered_data = dataset_print.loc[start_date:, f'{ticker} Close']
            filtered_ma_ST = ma_ST.loc[start_date:, f'{ticker} ST Moving Average']
            filtered_ma_LT = ma_LT.loc[start_date:, f'{ticker} LT Moving Average']

        elif plot_parameter == 'Last Day':
            start_date = current_date - timedelta(hours = 24)  # Approx. 5 years
            filtered_data = dataset_print.loc[start_date:, f'{ticker} Close']
            filtered_ma_ST = ma_ST.loc[start_date:, f'{ticker} ST Moving Average']
            filtered_ma_LT = ma_LT.loc[start_date:, f'{ticker} LT Moving Average']

        elif plot_parameter == 'Last 6 Hours':
            start_date = current_date - timedelta(hours = 6)  # Approx. 3 years
            filtered_data = dataset_print.loc[start_date:, f'{ticker} Close']
            filtered_ma_ST = ma_ST.loc[start_date:, f'{ticker} ST Moving Average']
            filtered_ma_LT = ma_LT.loc[start_date:, f'{ticker} LT Moving Average']


    # Plot the filtered data
    st.write("Moving average analysis")
    ma_dataframe = pd.concat([filtered_ma_ST, filtered_ma_LT], axis = 1)
    st.dataframe(ma_dataframe)
    st.line_chart(ma_dataframe)