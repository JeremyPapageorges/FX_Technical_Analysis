import pytz
import datetime
import pandas as pd
import MetaTrader5 as mt5


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

