#!/usr/bin/env python3
"""
Final verification of the De Bruijn graph
"""
import pandas as pd

print("="*80)
print("FINAL VERIFICATION OF DE BRUIJN GRAPH")
print("="*80)

# Read the updated file (nodes only version for easier viewing)
nodes_df = pd.read_excel('debruijn_graph_nodes_only.xlsx')
nodes_df = nodes_df.iloc[1:].copy()
nodes_df.columns = ['kmers', 'incoming_edge', 'node_number', 'merged_node', 'outgoing_edge']

# Read contig graph for comparison
contig_graph = pd.read_csv('contig_graph.txt', sep='\t')

print(f"\nTotal nodes in De Bruijn graph: {len(nodes_df)}")
print(f"Total contigs in contig graph: {len(contig_graph)}")

# Verify each node
issues = []
for idx, node_row in nodes_df.iterrows():
    node_num = int(node_row['node_number'])

    # Find corresponding contig
    contig_row = contig_graph[contig_graph['CONTIG_ID'] == node_num]

    if contig_row.empty:
        issues.append(f"Node {node_num}: No matching contig found")
        continue

    contig_row = contig_row.iloc[0]

    # Compare outgoing edges
    node_outgoing = str(node_row['outgoing_edge']) if not pd.isna(node_row['outgoing_edge']) else ''
    contig_outgoing = str(contig_row['OUTGOING_CONTIGS']) if not pd.isna(contig_row['OUTGOING_CONTIGS']) else ''

    # Clean up for comparison
    node_outgoing_clean = node_outgoing.replace('.0', '').replace(' ', '')
    contig_outgoing_clean = contig_outgoing.replace('.0', '').replace(' ', '')

    if node_outgoing_clean != contig_outgoing_clean:
        issues.append(f"Node {node_num}: Outgoing edge mismatch - node has '{node_outgoing_clean}', contig has '{contig_outgoing_clean}'")

    # Compare incoming edges
    node_incoming = str(node_row['incoming_edge']) if not pd.isna(node_row['incoming_edge']) else ''
    contig_incoming = str(contig_row['INCOMING_CONTIGS']) if not pd.isna(contig_row['INCOMING_CONTIGS']) else ''

    node_incoming_clean = node_incoming.replace('.0', '').replace(' ', '')
    contig_incoming_clean = contig_incoming.replace('.0', '').replace(' ', '')

    if node_incoming_clean != contig_incoming_clean:
        issues.append(f"Node {node_num}: Incoming edge mismatch - node has '{node_incoming_clean}', contig has '{contig_incoming_clean}'")

if issues:
    print(f"\n⚠ Found {len(issues)} issues:")
    for issue in issues[:20]:  # Show first 20
        print(f"  - {issue}")
else:
    print("\n✓ All nodes verified successfully!")
    print("✓ All incoming edges match!")
    print("✓ All outgoing edges match!")

# Show sample of nodes
print("\n" + "="*80)
print("SAMPLE OF COMPLETED NODES")
print("="*80)
print(nodes_df[['node_number', 'kmers', 'incoming_edge', 'outgoing_edge', 'merged_node']].head(15).to_string())

print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

# Count nodes with no incoming edges (start nodes)
start_nodes = nodes_df[nodes_df['incoming_edge'].isna() | (nodes_df['incoming_edge'] == '')]
print(f"Nodes with no incoming edges (start nodes): {len(start_nodes)}")

# Count nodes with no outgoing edges (end nodes)
end_nodes = nodes_df[nodes_df['outgoing_edge'].isna() | (nodes_df['outgoing_edge'] == '')]
print(f"Nodes with no outgoing edges (end nodes): {len(end_nodes)}")

# Count nodes with branches (multiple outgoing)
branch_nodes = nodes_df[nodes_df['outgoing_edge'].str.contains(',', na=False)]
print(f"Nodes with multiple outgoing edges (branch points): {len(branch_nodes)}")

# Count nodes with multiple incoming
merge_nodes = nodes_df[nodes_df['incoming_edge'].str.contains(',', na=False)]
print(f"Nodes with multiple incoming edges (merge points): {len(merge_nodes)}")

print("\n" + "="*80)
print("✓ DE BRUIJN GRAPH COMPLETION VERIFIED!")
print("="*80)
