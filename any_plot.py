import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return it.zip_longest(fillvalue=0, *args)

# [sum(x) for x in grouper(L, 10)]

df=pd.read_csv("C:/Users/mraha/Documents/BinPacking/CHCPythonGA 2022/CHC_data.csv")
df1=df.groupby('0').mean()
df1.plot.line(figsize=(10,10))


# df = pd.read_csv("C:/Users/mraha/Documents/BinPacking/CHCPythonGA 2022/CHC_data.csv")
# # Drop first row 
# # by selecting all rows from first row onwards
# # df = df.iloc[1: , :]
# print(df)

# new = df.groupby(np.arange(len(df)) // 30).mean() 
# print("new",new)

# # print("new",new.iloc[0:20])

# lines = new.plot.line(figsize=(10, 10))
df1.to_csv('data_table.csv')
plt.show()