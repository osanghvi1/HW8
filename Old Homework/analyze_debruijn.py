#!/usr/bin/env python3
"""
Analyze and complete the De Bruijn graph Excel file
"""
import pandas as pd
import openpyxl

# Read the Excel file
file_path = 'debruijn_graph_complete.xlsx'
df = pd.read_excel(file_path)

print("Current De Bruijn Graph Data:")
print("="*80)
print(df.to_string())
print("\n")

# Show column names
print("Columns:", df.columns.tolist())
print("\n")

# Show shape
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
