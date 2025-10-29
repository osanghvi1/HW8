#!/usr/bin/env python3
"""
Fill in missing node information by using the contig data
"""
import pandas as pd

# Read the contig data which has the merged nodes
contigs_df = pd.read_csv('contigs_initial.txt', sep='\t')
print("Contigs loaded:")
print(f"Total contigs: {len(contigs_df)}")

# Read the current debruijn file
debruijn_df = pd.read_excel('debruijn_graph_complete.xlsx')

# Skip the header row and extract actual data
debruijn_df = debruijn_df.iloc[1:].copy()
debruijn_df.columns = ['index', 'kmers', 'incoming_edge', 'node_number', 'merged_node', 'outgoing_edge']
debruijn_df = debruijn_df[['kmers', 'incoming_edge', 'node_number', 'merged_node', 'outgoing_edge']]

# Read contig graph to get incoming/outgoing edge information
contig_graph_df = pd.read_csv('contig_graph.txt', sep='\t')
print("\nContig graph loaded:")
print(f"Total contig graph rows: {len(contig_graph_df)}")

# Create a mapping from contig_id to contig info
contig_info = {}
for idx, row in contigs_df.iterrows():
    contig_id = row['CONTIG_ID']
    contig_info[contig_id] = {
        'start_node': row['START_NODE'],  # This is the 5-mer kmer suffix
        'end_node': row['END_NODE'],
        'sequence': row['SEQUENCE'],
        'length': row['LENGTH']
    }

# Create a mapping from contig_id to edge info
edge_info = {}
for idx, row in contig_graph_df.iterrows():
    contig_id = row['CONTIG_ID']
    incoming = str(row['INCOMING_CONTIGS']) if not pd.isna(row['INCOMING_CONTIGS']) else ''
    outgoing = str(row['OUTGOING_CONTIGS']) if not pd.isna(row['OUTGOING_CONTIGS']) else ''

    edge_info[contig_id] = {
        'incoming': incoming,
        'outgoing': outgoing,
        'sequence': row['SEQUENCE']
    }

print("\nMapping contigs to debruijn nodes...")
print(f"Total contigs in info: {len(contig_info)}")
print(f"Total edge info: {len(edge_info)}")

# Create a new mapping: start_node (5-mer suffix) -> contig_id
start_node_to_contig = {}
for contig_id, info in contig_info.items():
    start_node = info['start_node']
    start_node_to_contig[start_node] = contig_id

# Now update the debruijn dataframe
for idx, row in debruijn_df.iterrows():
    if pd.isna(row['kmers']):
        continue

    kmer_suffix = row['kmers']

    # Check if this suffix is a start node of any contig
    if kmer_suffix in start_node_to_contig:
        contig_id = start_node_to_contig[kmer_suffix]

        # Get contig info
        c_info = contig_info[contig_id]
        e_info = edge_info[contig_id]

        # Check if node is already filled
        current_node_num = row['node_number']

        if pd.isna(current_node_num):
            # Node not filled - fill it with contig ID
            debruijn_df.at[idx, 'node_number'] = int(contig_id)
            debruijn_df.at[idx, 'merged_node'] = c_info['sequence']
            debruijn_df.at[idx, 'incoming_edge'] = e_info['incoming']
            debruijn_df.at[idx, 'outgoing_edge'] = e_info['outgoing']
            print(f"Filled node {contig_id} for kmer {kmer_suffix}")
        else:
            # Node already filled - verify it matches
            if int(current_node_num) == contig_id:
                # Update any missing fields
                if pd.isna(row['merged_node']):
                    debruijn_df.at[idx, 'merged_node'] = c_info['sequence']
                if pd.isna(row['incoming_edge']):
                    debruijn_df.at[idx, 'incoming_edge'] = e_info['incoming']
                if pd.isna(row['outgoing_edge']):
                    debruijn_df.at[idx, 'outgoing_edge'] = e_info['outgoing']
                print(f"Updated node {contig_id} for kmer {kmer_suffix}")
            else:
                print(f"WARNING: Node mismatch for {kmer_suffix}: expected {contig_id}, got {int(current_node_num)}")

# Count filled nodes now
filled_nodes = debruijn_df[debruijn_df['node_number'].notna()]
print(f"\nTotal filled nodes after update: {len(filled_nodes)}")

# Save the updated file
# First, add back the header row
header_row = pd.DataFrame({
    'kmers': ['kmers'],
    'incoming_edge': ['incoming edge'],
    'node_number': ['node number'],
    'merged_node': ['merged node'],
    'outgoing_edge': ['outgoing edge']
})

# Combine header and data
final_df = pd.concat([header_row, debruijn_df], ignore_index=True)

# Write to Excel
final_df.to_excel('debruijn_graph_complete_updated.xlsx', index=False, header=False)
print("\nUpdated file saved as: debruijn_graph_complete_updated.xlsx")
