#!/usr/bin/env python3
"""
Create a clean version showing only the actual graph nodes
"""
import pandas as pd
import shutil

# Read the updated file
df = pd.read_excel('debruijn_graph_complete_updated.xlsx')

# Skip header row and set column names
df = df.iloc[1:].copy()
df.columns = ['kmers', 'incoming_edge', 'node_number', 'merged_node', 'outgoing_edge']

# Filter to only show rows with node numbers (the actual graph nodes)
nodes_only = df[df['node_number'].notna()].copy()

# Sort by node number
nodes_only = nodes_only.sort_values('node_number')

# Create header row
header_row = pd.DataFrame({
    'kmers': ['kmers'],
    'incoming_edge': ['incoming edge'],
    'node_number': ['node number'],
    'merged_node': ['merged node'],
    'outgoing_edge': ['outgoing edge']
})

# Combine
final_df = pd.concat([header_row, nodes_only], ignore_index=True)

# Save as a clean version (nodes only)
final_df.to_excel('debruijn_graph_nodes_only.xlsx', index=False, header=False)
print(f"Clean version (nodes only) saved: debruijn_graph_nodes_only.xlsx")
print(f"Total nodes: {len(nodes_only)}")

# Also backup and replace the original
shutil.copy('debruijn_graph_complete.xlsx', 'debruijn_graph_complete_backup.xlsx')
print("\nBackup created: debruijn_graph_complete_backup.xlsx")

shutil.copy('debruijn_graph_complete_updated.xlsx', 'debruijn_graph_complete.xlsx')
print("Original file updated: debruijn_graph_complete.xlsx")

print("\n✓ All done!")
print("\nFiles created:")
print("  - debruijn_graph_complete.xlsx (updated with all kmers)")
print("  - debruijn_graph_nodes_only.xlsx (clean version with 70 nodes)")
print("  - debruijn_graph_complete_backup.xlsx (backup of original)")
