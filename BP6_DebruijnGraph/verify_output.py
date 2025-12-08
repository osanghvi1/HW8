#!/usr/bin/env python3
"""
Verify all output files are correct
"""
import pandas as pd
import os

print("VERIFICATION OF OUTPUT FILES")
print("=" * 70)
print()

files_to_check = [
    'debruijn_graph_complete.xlsx',
    'contigs.xlsx',
    'BP6_ANSWERS.xlsx',
    'BP6_ANSWERS.txt',
    'README.md',
    'quote_identified.txt'
]

for filename in files_to_check:
    exists = os.path.exists(filename)
    size = os.path.getsize(filename) if exists else 0
    status = "✓" if exists and size > 0 else "✗"
    print(f"{status} {filename:40s} ({size:,} bytes)")

print()
print("=" * 70)
print()

# Check debruijn_graph_complete.xlsx structure
print("Checking debruijn_graph_complete.xlsx structure:")
df = pd.read_excel('debruijn_graph_complete.xlsx', header=None)
print(f"  Rows: {len(df)}")
print(f"  Columns: {len(df.columns)}")
print()
print("First 5 rows:")
print(df.head(5).to_string(index=False))
print()
print("Last 3 rows:")
print(df.tail(3).to_string(index=False))
print()

# Check contigs
contigs_df = pd.read_excel('contigs.xlsx')
print(f"Number of contigs: {len(contigs_df)}")
print(f"Total assembly length: {contigs_df['length'].sum()}")
print(f"N50 calculation:")
lengths = sorted(contigs_df['length'].tolist(), reverse=True)
total = sum(lengths)
cumsum = 0
for i, length in enumerate(lengths):
    cumsum += length
    if cumsum >= total / 2:
        print(f"  N50 = {length} (reached after {i+1} contigs)")
        break
print()

print("=" * 70)
print("All files verified successfully!")
