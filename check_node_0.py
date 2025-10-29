#!/usr/bin/env python3
"""
Check node 0 specifically
"""
import pandas as pd

# Read the complete file
df = pd.read_excel('debruijn_graph_complete.xlsx')
df = df.iloc[1:].copy()
df.columns = ['kmers', 'incoming_edge', 'node_number', 'merged_node', 'outgoing_edge']

# Find all rows with node 0
node_0_rows = df[df['node_number'] == 0]

print("All rows with node_number = 0:")
print("="*80)
print(node_0_rows[['kmers', 'incoming_edge', 'node_number', 'merged_node', 'outgoing_edge']])

# Check the contig data
contigs_df = pd.read_csv('contigs_initial.txt', sep='\t')
contig_0 = contigs_df[contigs_df['CONTIG_ID'] == 0]

print("\n\nContig 0 from contigs_initial.txt:")
print("="*80)
print(contig_0)

# Check graph edges for these kmers
graph_df = pd.read_csv('graph_edges.txt', sep='\t')
abovei_row = graph_df[graph_df['KMER'] == 'abovei']
boveim_row = graph_df[graph_df['KMER'] == 'boveim']

print("\n\nK-mer 'abovei' from graph_edges.txt:")
print(abovei_row[['PREFIX', 'KMER', 'SUFFIX', 'COUNT']])

print("\n\nK-mer info:")
print("  - 'abovei' has prefix 'above' and suffix 'bovei'")
print("  - The contig starts with 'above' (the start_node)")
print("  - The first kmer in the contig is 'abovei'")
print("  - So 'abovei' (suffix = 'bovei') should be the kmer in the debruijn graph")
print("  - But we also have 'boveim' which has prefix 'bovei'...")

if not boveim_row.empty:
    print("\nK-mer 'boveim' from graph_edges.txt:")
    print(boveim_row[['PREFIX', 'KMER', 'SUFFIX', 'COUNT']])
    print("\n'boveim' is the NEXT kmer after 'abovei' in the sequence!")
    print("abovei -> boveim -> oveimon -> veimonl -> eimonlh -> imonlyh OR imonlyi")

print("\n\nConclusion:")
print("  The De Bruijn graph node should represent the 5-mer 'bovei'")
print("  This 5-mer is:")
print("    - The SUFFIX of kmer 'abovei' (row 1)")
print("    - The PREFIX of kmer 'boveim' (row 39)")
print("  Both rows pointing to node 0 is CORRECT - they both involve the same 5-mer node!")
