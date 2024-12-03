import os
import pandas as pd

path = os.path.dirname(__file__)
data_path = os.path.join(path, "dz.csv")

df = pd.read_csv(data_path)
print(df.head())

group = df.groupby('City')['Salary'].mean()
print(group)
