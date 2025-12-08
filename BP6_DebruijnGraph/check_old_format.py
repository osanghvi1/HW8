#!/usr/bin/env python3
import pandas as pd

# Read the old homework Excel file to see the structure
df = pd.read_excel('../Old Homework/debruijn_graph_complete.xlsx')
print('Columns:', df.columns.tolist())
print('\nShape:', df.shape)
print('\nFirst 20 rows:')
print(df.head(20).to_string())
