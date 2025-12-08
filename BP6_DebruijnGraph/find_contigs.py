#!/usr/bin/env python3
"""
Find contigs (unbranched paths) in the De Bruijn graph
"""
import pandas as pd
from collections import defaultdict

# Load the edges
edges_df = pd.read_csv('kmer_edges.txt', sep='\t')

# Build adjacency lists
nodes_out = defaultdict(list)
nodes_in = defaultdict(list)
kmer_info = {}

for _, row in edges_df.iterrows():
    kmer = row['KMER']
    source = row['SOURCE']
    dest = row['DEST']
    count = row['COUNT']

    nodes_out[source].append((kmer, dest, count))
    nodes_in[dest].append((kmer, source, count))
    kmer_info[kmer] = {'source': source, 'dest': dest, 'count': count}

# Find all nodes
all_nodes = set()
for _, row in edges_df.iterrows():
    all_nodes.add(row['SOURCE'])
    all_nodes.add(row['DEST'])

print(f"Total nodes: {len(all_nodes)}")
print(f"Total edges (kmers): {len(edges_df)}")

# Find contigs
# A contig is a maximal unbranched path
# Start from nodes that are:
# - Start tips (no incoming edges)
# - Branch points (multiple incoming or outgoing edges)

used_kmers = set()
contigs = []

def extend_contig(start_node, initial_kmer=None):
    """
    Extend a contig from the start node
    """
    contig_sequence = start_node  # Start with the 4-mer node
    current_node = start_node
    path_kmers = []

    if initial_kmer:
        # If we have an initial kmer, use it
        path_kmers.append(initial_kmer)
        kmer_obj = kmer_info[initial_kmer]
        current_node = kmer_obj['dest']
        contig_sequence += initial_kmer[-1]  # Add the last letter of the kmer

    # Keep extending while we can
    while True:
        outgoing = [k for k, _, _ in nodes_out.get(current_node, []) if k not in used_kmers]

        # Stop if no outgoing edges or multiple outgoing edges (branch point)
        if len(outgoing) == 0:
            break
        if len(outgoing) > 1:
            break

        # Check if the destination has multiple incoming edges (merge point)
        next_kmer = outgoing[0]
        dest_node = kmer_info[next_kmer]['dest']
        incoming_to_dest = [k for k, _, _ in nodes_in.get(dest_node, []) if k not in used_kmers]

        if len(incoming_to_dest) > 1:
            # This is a merge point, include this kmer but stop here
            path_kmers.append(next_kmer)
            used_kmers.add(next_kmer)
            contig_sequence += next_kmer[-1]
            break

        # Add this kmer to the path
        path_kmers.append(next_kmer)
        used_kmers.add(next_kmer)
        contig_sequence += next_kmer[-1]
        current_node = dest_node

    return contig_sequence, path_kmers, current_node

# Process all kmers to find contigs
for kmer in sorted(edges_df['KMER']):
    if kmer in used_kmers:
        continue

    source = kmer_info[kmer]['source']
    dest = kmer_info[kmer]['dest']

    # Check if this is a start of a contig
    # Start if:
    # - Source has no incoming edges (tip)
    # - Source has multiple incoming edges (merge point)
    # - Source has multiple outgoing edges (branch point)

    should_start = False

    if source not in nodes_in:  # Tip
        should_start = True
    elif len(nodes_out.get(source, [])) > 1:  # Branch point
        should_start = True
    elif len(nodes_in.get(source, [])) > 1:  # Merge point
        should_start = True

    if should_start:
        contig_seq, contig_kmers, end_node = extend_contig(source, kmer)
        used_kmers.add(kmer)

        if len(contig_seq) >= 5:  # Only save contigs of reasonable length
            contigs.append({
                'contig_id': len(contigs) + 1,
                'sequence': contig_seq,
                'length': len(contig_seq),
                'start_node': source,
                'end_node': end_node,
                'num_kmers': len(contig_kmers),
                'kmers': ','.join(contig_kmers)
            })

# Check for any remaining unused kmers and make small contigs
for kmer in sorted(edges_df['KMER']):
    if kmer not in used_kmers:
        source = kmer_info[kmer]['source']
        dest = kmer_info[kmer]['dest']
        contig_seq = source + kmer[-1]
        used_kmers.add(kmer)

        contigs.append({
            'contig_id': len(contigs) + 1,
            'sequence': contig_seq,
            'length': len(contig_seq),
            'start_node': source,
            'end_node': dest,
            'num_kmers': 1,
            'kmers': kmer
        })

# Sort contigs by length (descending)
contigs.sort(key=lambda x: x['length'], reverse=True)

# Reassign contig IDs after sorting
for i, contig in enumerate(contigs):
    contig['contig_id'] = i + 1

print(f"\nContigs found: {len(contigs)}")
print(f"Kmers used: {len(used_kmers)} out of {len(edges_df)}")

# Calculate statistics
total_length = sum(c['length'] for c in contigs)
print(f"Total assembly length: {total_length}")

# Calculate N50
lengths = sorted([c['length'] for c in contigs], reverse=True)
cumsum = 0
n50 = 0
for length in lengths:
    cumsum += length
    if cumsum >= total_length / 2:
        n50 = length
        break

print(f"N50: {n50}")
print(f"Longest contig: {lengths[0]}")
print(f"Shortest contig: {lengths[-1]}")

# Show top 10 contigs
print("\nTop 10 longest contigs:")
for i, contig in enumerate(contigs[:10]):
    print(f"{i+1}. Length {contig['length']}: {contig['sequence']}")

# Save contigs
contigs_df = pd.DataFrame(contigs)
contigs_df.to_excel('contigs.xlsx', index=False)
contigs_df.to_csv('contigs.txt', sep='\t', index=False)

# Also save just the sequences for easier reading
with open('contigs_sequences.txt', 'w') as f:
    f.write("ASSEMBLED CONTIGS\n")
    f.write("=" * 60 + "\n\n")
    for contig in contigs:
        f.write(f"Contig {contig['contig_id']} (length {contig['length']}):\n")
        f.write(f"{contig['sequence']}\n\n")

print("\nSaved: contigs.xlsx, contigs.txt, contigs_sequences.txt")
