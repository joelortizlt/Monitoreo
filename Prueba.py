import pandas as pd
csv_REAL = '/Users/renzomartinch/Downloads/GAHI/INPUTS_REAL.csv'

a = pd.read_csv(csv_REAL)

b=pd.read_csv(a)

print(b)