#!/usr/bin/env python3
"""
Verify the completed De Bruijn graph
"""
import pandas as pd

# Read the updated file
df = pd.read_excel('debruijn_graph_complete_updated.xlsx')

# Skip header row
df = df.iloc[1:].copy()
df.columns = ['kmers', 'incoming_edge', 'node_number', 'merged_node', 'outgoing_edge']

print("Updated De Bruijn Graph Summary")
print("="*80)

# Count filled vs empty
total_rows = len(df)
filled_nodes = df[df['node_number'].notna()]
empty_nodes = df[df['node_number'].isna()]

print(f"Total kmers: {total_rows}")
print(f"Filled nodes: {len(filled_nodes)}")
print(f"Empty nodes: {len(empty_nodes)}")

# Show filled nodes
print("\nFilled Nodes:")
print(filled_nodes[['kmers', 'incoming_edge', 'node_number', 'merged_node', 'outgoing_edge']].head(20))

if len(empty_nodes) > 0:
    print("\nEmpty nodes (first 10):")
    print(empty_nodes[['kmers']].head(10))
else:
    print("\nAll nodes are filled!")

# Check for duplicate node numbers
node_numbers = filled_nodes['node_number'].dropna()
duplicates = node_numbers[node_numbers.duplicated()]
if len(duplicates) > 0:
    print(f"\nWARNING: Found {len(duplicates)} duplicate node numbers")
    print(duplicates)
else:
    print("\nNo duplicate node numbers found!")

# Show node number range
print(f"\nNode numbers range: {int(node_numbers.min())} to {int(node_numbers.max())}")
print(f"Total unique nodes: {len(node_numbers.unique())}")
