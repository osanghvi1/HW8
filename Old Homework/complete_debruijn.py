#!/usr/bin/env python3
"""
Complete the De Bruijn graph by filling in missing information
"""
import pandas as pd
import openpyxl
from collections import defaultdict

# Read the k-mer graph data
graph_df = pd.read_csv('graph_edges.txt', sep='\t')
print("K-mer graph data loaded")
print(f"Total k-mers: {len(graph_df)}")

# Read the current debruijn file
debruijn_df = pd.read_excel('debruijn_graph_complete.xlsx')

# Skip the header row and extract actual data
debruijn_df = debruijn_df.iloc[1:].copy()  # Skip first row which contains column names
debruijn_df.columns = ['index', 'kmers', 'incoming_edge', 'node_number', 'merged_node', 'outgoing_edge']

# Drop the index column
debruijn_df = debruijn_df[['kmers', 'incoming_edge', 'node_number', 'merged_node', 'outgoing_edge']]

print("\nCurrent debruijn data:")
print(f"Total rows: {len(debruijn_df)}")

# Count nodes that are already filled
filled_nodes = debruijn_df[debruijn_df['node_number'].notna()]
print(f"Filled nodes: {len(filled_nodes)}")

# Create a mapping from kmer suffix (last 5 letters) to list of kmers with that prefix
kmer_to_info = {}
suffix_to_kmers = defaultdict(list)

for idx, row in graph_df.iterrows():
    kmer = row['KMER']
    prefix = row['PREFIX']  # first 5 letters
    suffix = row['SUFFIX']  # last 5 letters

    kmer_to_info[suffix] = {
        'kmer': kmer,
        'prefix': prefix,
        'suffix': suffix
    }
    suffix_to_kmers[prefix].append(kmer)

print(f"\nUnique suffixes (5-mers): {len(kmer_to_info)}")

# For each k-mer in the debruijn file, check the outgoing edges
print("\nChecking outgoing edges...")
issues_found = []

for idx, row in debruijn_df.iterrows():
    if pd.isna(row['kmers']):
        continue

    kmer_suffix = row['kmers']

    # Check if this suffix exists in our graph
    if kmer_suffix not in kmer_to_info:
        continue

    # Get the full kmer info
    kmer = kmer_to_info[kmer_suffix]['kmer']
    suffix = kmer_to_info[kmer_suffix]['suffix']

    # Find what this kmer connects to (the suffix becomes the prefix of next kmers)
    outgoing_kmers = suffix_to_kmers[suffix]

    if len(outgoing_kmers) > 0:
        # Map these kmers to node numbers
        outgoing_nodes = []
        for out_kmer in outgoing_kmers:
            # Get the suffix of this outgoing kmer
            out_suffix = out_kmer[-5:]
            # Find which node has this suffix as its kmer
            node_row = debruijn_df[debruijn_df['kmers'] == out_suffix]
            if not node_row.empty and not pd.isna(node_row.iloc[0]['node_number']):
                outgoing_nodes.append(str(int(node_row.iloc[0]['node_number'])))

        if outgoing_nodes:
            expected_outgoing = ','.join(outgoing_nodes)
            current_outgoing = str(row['outgoing_edge']) if not pd.isna(row['outgoing_edge']) else ''

            if current_outgoing != expected_outgoing:
                issues_found.append({
                    'kmer': kmer_suffix,
                    'node': row['node_number'],
                    'current_outgoing': current_outgoing,
                    'expected_outgoing': expected_outgoing
                })

if issues_found:
    print(f"\nFound {len(issues_found)} potential issues with outgoing edges:")
    for issue in issues_found[:10]:  # Show first 10
        print(f"  Node {issue['node']} ({issue['kmer']}): current='{issue['current_outgoing']}' expected='{issue['expected_outgoing']}'")
else:
    print("\nNo issues found with outgoing edges!")

print("\nAnalysis complete!")
