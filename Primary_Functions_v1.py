import numpy as np

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

