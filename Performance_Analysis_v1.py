# write a performance evaluation script
import numpy as np
def performance(data, open_price, buy_column, sell_column, long_result_col, short_result_col, total_result_col):

    # variable holding period
    for i in range(len(data)):
        try:
            if data[i, buy_column] == 1:
                for a in range(i + 1, i+1000):
                    if data[a, buy_column] == 1 or data[a, sell_column] == -1:
                        data[a, long_result_col] = data[a, open_price] - data[i, open_price]
                        break
                    else:
                        continue
            else:
                continue
        except IndexError:
            pass
    
    for i in range(len(data)):
        try:
            if data[i, sell_column] == -1:
                for a in range(i+1, i+1000):
                    if data[a, buy_column] == 1 or data[a, sell_column] == -1:
                            data[a, short_result_col] = data[i, open_price] - data[a, open_price]
                            break
                    else:
                        continue
            else:
                continue

        except IndexError:
            pass
    
    # aggregating the long and short results into one column:

    data[:, total_result_col] = data[:, long_result_col] + data[:, short_result_col]

    # profit factor

    total_net_profits = data[data[:, total_result_col] > 0, total_result_col]

    total_net_losses = data[data[:, total_result_col] < 0 , total_result_col]
    total_net_losses = abs(total_net_losses)
    
    profit_factor = round(np.sum(total_net_profits) / np.sum(total_net_losses), 2)

    # Hit Ratio
    hit_ratio = len(total_net_profits) / (len(total_net_losses) + len(total_net_profits))
    hit_ratio = hit_ratio * 100

    # risk - reward ratio
    average_gain = total_net_profits.mean()
    average_loss = total_net_losses.mean()
    realized_risk_reward = round(average_gain / average_loss, 3)


    # number of trades

    trades = len(total_net_losses) + len(total_net_profits)

    print(f'Hit Ratio              = {hit_ratio}')
    print(f'Profit Factor          = {profit_factor}')
    print(f'Realized Risk-Reward   = {realized_risk_reward}')
    print(f'Number of Trades       = {trades}')