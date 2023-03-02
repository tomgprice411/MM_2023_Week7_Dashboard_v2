import pandas as pd

#import data
df = pd.read_csv("Global Electric Vehicle Market Share.csv")

#make the dataframe long so it's easier to work with
df = pd.melt(df, id_vars = ["Brands"], value_vars = ["Q2 2021", "Q3 2021", "Q4 2021", "Q1 2022", "Q2 2022", "Q3 2022"],
            value_name = "MarketShare", var_name = "Quarter")

#add on the quarter start date for each quarter
df["QuarterStartDate"] = df["Quarter"].map({"Q2 2021": "2021-04-01", "Q3 2021": "2021-07-01", "Q4 2021": "2021-10-01", "Q1 2022": "2022-01-01", "Q2 2022": "2022-04-01",
"Q3 2022": "2022-10-01"})

#convert the market share into a decimal from a string
df["MarketShareReformat"] = df["MarketShare"].str.replace("%", "").astype(int).div(100)

