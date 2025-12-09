#!/usr/bin/env python3
"""
De Bruijn Graph Assembler

This builds a De Bruijn graph from k-mers and assembles contigs.

How it works:
1. Build a graph where each k-mer is an edge
2. Nodes are (k-1)-mers (one letter shorter)
3. Walk through the graph to find continuous paths (contigs)
"""

import argparse
from collections import defaultdict, Counter


def read_kmers(filename):
    """
    Read k-mers from a file.

    Format: kmer\tcount
    """
    kmer_counts = {}
    with open(filename, 'r') as f:
        # Skip header
        next(f)
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                kmer = parts[0]
                count = int(parts[1])
                kmer_counts[kmer] = count
    return kmer_counts


class DeBruijnGraph:
    """
    A De Bruijn graph for genome assembly.

    For a k-mer like "ATGC":
    - It creates an edge from "ATG" to "TGC"
    - "ATG" is the source node (first k-1 letters)
    - "TGC" is the destination node (last k-1 letters)
    """

    def __init__(self, kmers, k):
        """
        Build the graph from k-mers.

        Parameters:
        -----------
        kmers : dict
            Dictionary mapping k-mer to count
        k : int
            K-mer length
        """
        self.k = k
        self.kmers = kmers

        # Graph structure
        # nodes_out[node] = list of (kmer, dest_node, count)
        self.nodes_out = defaultdict(list)
        # nodes_in[node] = list of (kmer, source_node, count)
        self.nodes_in = defaultdict(list)

        # Build the graph
        for kmer, count in kmers.items():
            # For k-mer "ATGC", nodes are 3-mers
            source = kmer[:k-1]  # "ATG"
            dest = kmer[1:]      # "TGC"

            self.nodes_out[source].append((kmer, dest, count))
            self.nodes_in[dest].append((kmer, source, count))

        # Find all nodes
        self.all_nodes = set()
        for kmer in kmers.keys():
            self.all_nodes.add(kmer[:k-1])
            self.all_nodes.add(kmer[1:])

    def get_node_info(self):
        """
        Get information about each node.

        Returns a list of dicts with:
        - node: the (k-1)-mer
        - in_degree: number of incoming edges
        - out_degree: number of outgoing edges
        - type: START, END, BRANCH, MERGE, or LINEAR
        """
        nodes_info = []

        for node in sorted(self.all_nodes):
            in_deg = len(self.nodes_in.get(node, []))
            out_deg = len(self.nodes_out.get(node, []))

            node_type = []
            if in_deg == 0:
                node_type.append('START')
            if out_deg == 0:
                node_type.append('END')
            if in_deg > 1:
                node_type.append('MERGE')
            if out_deg > 1:
                node_type.append('BRANCH')
            if in_deg == 1 and out_deg == 1:
                node_type.append('LINEAR')

            nodes_info.append({
                'node': node,
                'in_degree': in_deg,
                'out_degree': out_deg,
                'type': ','.join(node_type) if node_type else 'ISOLATED'
            })

        return nodes_info

    def find_contigs(self):
        """
        Find contigs (unbranched paths) in the graph.

        Returns a list of contigs. Each contig is a dict with:
        - sequence: the assembled DNA sequence
        - length: length of sequence
        - kmers: list of k-mers in this contig
        """
        used_kmers = set()
        contigs = []

        # Helper function to extend a path from a starting k-mer
        def extend_path(start_kmer):
            """
            Extend a path starting from a k-mer.
            """
            # Start the sequence
            sequence = start_kmer
            path_kmers = [start_kmer]
            used_kmers.add(start_kmer)

            current_node = start_kmer[1:]  # Last (k-1) letters

            # Keep extending forward
            while True:
                # What are the outgoing edges we haven't used?
                outgoing = [(km, dest, cnt) for km, dest, cnt in self.nodes_out.get(current_node, [])
                           if km not in used_kmers]

                # Stop if no outgoing edges or multiple choices (branch point)
                if len(outgoing) != 1:
                    break

                next_kmer, next_dest, count = outgoing[0]

                # Check if destination is a merge point (multiple incoming edges)
                incoming_to_dest = [(km, src, cnt) for km, src, cnt in self.nodes_in.get(next_dest, [])
                                   if km not in used_kmers]

                # If it's a merge point, stop here
                if len(incoming_to_dest) > 1:
                    break

                # Extend the sequence
                # We add only the last letter of the k-mer (others overlap)
                sequence += next_kmer[-1]
                path_kmers.append(next_kmer)
                used_kmers.add(next_kmer)
                current_node = next_dest

            return {
                'sequence': sequence,
                'length': len(sequence),
                'kmers': path_kmers
            }

        # Find starting points for contigs
        # Start from:
        # 1. Tips (nodes with no incoming edges)
        # 2. Branch points (nodes with multiple outgoing edges)
        # 3. Merge points (nodes with multiple incoming edges)

        for kmer in sorted(self.kmers.keys()):
            if kmer in used_kmers:
                continue

            source = kmer[:self.k-1]

            # Should we start a contig here?
            should_start = False

            # Tip (no incoming edges)
            if source not in self.nodes_in:
                should_start = True
            # Branch point (multiple outgoing)
            elif len(self.nodes_out.get(source, [])) > 1:
                should_start = True
            # Merge point (multiple incoming)
            elif len(self.nodes_in.get(source, [])) > 1:
                should_start = True

            if should_start:
                contig = extend_path(kmer)
                contigs.append(contig)

        # Pick up any remaining unused k-mers
        for kmer in sorted(self.kmers.keys()):
            if kmer not in used_kmers:
                contig = extend_path(kmer)
                contigs.append(contig)

        # Sort contigs by length (longest first)
        contigs.sort(key=lambda x: x['length'], reverse=True)

        return contigs


def calculate_n50(contig_lengths):
    """
    Calculate N50 statistic.

    N50 is the length where 50% of the total assembly is in contigs
    of that length or longer.
    """
    if not contig_lengths:
        return 0

    # Sort lengths (longest first)
    lengths = sorted(contig_lengths, reverse=True)
    total_length = sum(lengths)
    target = total_length / 2

    cumsum = 0
    for length in lengths:
        cumsum += length
        if cumsum >= target:
            return length

    return 0


def save_contigs(contigs, filename):
    """
    Save contigs to a FASTA file.
    """
    with open(filename, 'w') as f:
        for i, contig in enumerate(contigs):
            f.write(f">contig_{i+1} length={contig['length']}\n")
            # Write sequence in lines of 80 characters
            seq = contig['sequence']
            for j in range(0, len(seq), 80):
                f.write(seq[j:j+80] + '\n')


def save_contig_info(contigs, filename):
    """
    Save contig information to a text file.
    """
    with open(filename, 'w') as f:
        f.write("contig_id\tlength\tnum_kmers\tsequence\n")
        for i, contig in enumerate(contigs):
            f.write(f"{i+1}\t{contig['length']}\t{len(contig['kmers'])}\t{contig['sequence']}\n")


def main():
    parser = argparse.ArgumentParser(description='Assemble contigs from k-mers using De Bruijn graph')
    parser.add_argument('--input', type=str, required=True,
                       help='Input k-mers file')
    parser.add_argument('--output', type=str, default='contigs.fasta',
                       help='Output contigs file (default: contigs.fasta)')
    parser.add_argument('--info', type=str, default='contig_info.txt',
                       help='Output contig info file (default: contig_info.txt)')

    args = parser.parse_args()

    # Read k-mers
    print(f"Reading k-mers from {args.input}...")
    kmer_counts = read_kmers(args.input)
    print(f"Loaded {len(kmer_counts)} unique k-mers")

    if len(kmer_counts) == 0:
        print("Error: No k-mers found!")
        return

    # Determine k
    k = len(list(kmer_counts.keys())[0])
    print(f"K-mer length: {k}")

    # Build De Bruijn graph
    print("\nBuilding De Bruijn graph...")
    graph = DeBruijnGraph(kmer_counts, k)
    print(f"  Nodes: {len(graph.all_nodes)}")
    print(f"  Edges: {len(kmer_counts)}")

    # Get node statistics
    nodes_info = graph.get_node_info()
    start_tips = sum(1 for n in nodes_info if 'START' in n['type'])
    end_tips = sum(1 for n in nodes_info if 'END' in n['type'])
    branch_points = sum(1 for n in nodes_info if 'BRANCH' in n['type'])
    merge_points = sum(1 for n in nodes_info if 'MERGE' in n['type'])

    print(f"\nGraph structure:")
    print(f"  Start tips: {start_tips}")
    print(f"  End tips: {end_tips}")
    print(f"  Branch points: {branch_points}")
    print(f"  Merge points: {merge_points}")

    # Find contigs
    print("\nFinding contigs...")
    contigs = graph.find_contigs()
    print(f"Found {len(contigs)} contigs")

    # Calculate statistics
    lengths = [c['length'] for c in contigs]
    total_length = sum(lengths)
    n50 = calculate_n50(lengths)

    print(f"\nAssembly statistics:")
    print(f"  Number of contigs: {len(contigs)}")
    print(f"  Total length: {total_length}")
    print(f"  N50: {n50}")
    print(f"  Longest contig: {max(lengths)}")
    print(f"  Shortest contig: {min(lengths)}")

    # Show top 5 contigs
    print(f"\nTop 5 longest contigs:")
    for i, contig in enumerate(contigs[:5]):
        seq = contig['sequence']
        if len(seq) > 50:
            seq = seq[:50] + "..."
        print(f"  {i+1}. Length {contig['length']}: {seq}")

    # Save contigs
    save_contigs(contigs, args.output)
    save_contig_info(contigs, args.info)
    print(f"\nSaved contigs to {args.output}")
    print(f"Saved contig info to {args.info}")


if __name__ == '__main__':
    main()
