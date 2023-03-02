import numpy as np

def create_heatmap_array(df):
    #to create a waffle chart we need to do a hack-y workaround on the heatmap function
    #create a 10 x 10 array where each value in the array will represent a different brand, and the number of values for each brand will be equivalent to the market share %
    brand_squares = [int(perc * 100) for perc in df["MarketShareReformat"]]
    brand_array = [np.ones(squares) * (i+1) for i, squares in enumerate(brand_squares)]

    data = np.concatenate(brand_array)
    data = data.reshape(10, 10)
    data = data.transpose() # Transpose the array

    return data
