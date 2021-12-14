import pandas as pd

pd.options.display.max_rows = 2

df = pd.read_csv("dataset_cardiff.csv")



print(df.columns) 

print(df.nod.value_counts())


"""
0    135984
1      6458
"""