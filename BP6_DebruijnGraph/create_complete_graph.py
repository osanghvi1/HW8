#!/usr/bin/env python3
"""
Create the complete De Bruijn graph Excel file
Similar to debruijn_graph_complete.xlsx from the old homework
"""
import pandas as pd
from collections import defaultdict

# Load the edges and contigs
edges_df = pd.read_csv('kmer_edges.txt', sep='\t')
contigs_df = pd.read_excel('contigs.xlsx')

# Build node mappings
nodes_in = defaultdict(list)
nodes_out = defaultdict(list)
kmer_to_edge_info = {}

for _, row in edges_df.iterrows():
    kmer = row['KMER']
    source = row['SOURCE']
    dest = row['DEST']
    count = row['COUNT']

    nodes_out[source].append({'kmer': kmer, 'dest': dest, 'count': count})
    nodes_in[dest].append({'kmer': kmer, 'source': source, 'count': count})
    kmer_to_edge_info[kmer] = {'source': source, 'dest': dest, 'count': count}

# Get all unique nodes
all_nodes = set()
for _, row in edges_df.iterrows():
    all_nodes.add(row['SOURCE'])
    all_nodes.add(row['DEST'])

all_nodes = sorted(list(all_nodes))

# Create node to number mapping
node_to_num = {node: i for i, node in enumerate(all_nodes)}

# Create the De Bruijn graph table
graph_data = []

# First, create a mapping of nodes to their contig sequences
node_to_contig = {}
for _, contig in contigs_df.iterrows():
    seq = contig['sequence']
    # The contig sequence contains 4-mer nodes
    # For a contig sequence, the first node is the first 4 characters
    for i in range(len(seq) - 3):
        node = seq[i:i+4]
        if node in all_nodes:
            # This node is part of this contig
            # Find the full path from this node
            if node not in node_to_contig:
                node_to_contig[node] = seq

for node in all_nodes:
    node_num = node_to_num[node]

    # Get incoming edges
    incoming = nodes_in.get(node, [])
    incoming_nodes = [node_to_num[e['source']] for e in incoming]
    incoming_str = ','.join(map(str, incoming_nodes)) if incoming_nodes else ''

    # Get outgoing edges
    outgoing = nodes_out.get(node, [])
    outgoing_nodes = [node_to_num[e['dest']] for e in outgoing]
    outgoing_str = ','.join(map(str, outgoing_nodes)) if outgoing_nodes else ''

    # Get the merged node (contig sequence)
    merged_node = node_to_contig.get(node, node)

    graph_data.append({
        'kmers': node,
        'incoming edge': incoming_str,
        'node number': node_num,
        'merged node': merged_node,
        'outgoing edge': outgoing_str
    })

# Create DataFrame
graph_df = pd.DataFrame(graph_data)

# Create the full Excel file with a header row
output_data = []

# Add header row
output_data.append({
    'index': '',
    'kmers': 'kmers',
    'incoming edge': 'incoming edge',
    'node number': 'node number',
    'merged node': 'merged node',
    'outgoing edge': 'outgoing edge'
})

# Add all nodes
for _, row in graph_df.iterrows():
    output_data.append({
        'index': '',
        'kmers': row['kmers'],
        'incoming edge': row['incoming edge'],
        'node number': row['node number'],
        'merged node': row['merged node'],
        'outgoing edge': row['outgoing edge']
    })

output_df = pd.DataFrame(output_data)

# Save to Excel
output_df.to_excel('debruijn_graph_complete.xlsx', index=False, header=False)

print(f"Created De Bruijn graph Excel file with {len(graph_df)} nodes")
print(f"Saved: debruijn_graph_complete.xlsx")

# Also create a simpler version for review
graph_df.to_excel('debruijn_graph_nodes.xlsx', index=False)
print(f"Also saved: debruijn_graph_nodes.xlsx (without header row)")
