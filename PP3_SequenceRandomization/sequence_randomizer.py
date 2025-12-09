#!/usr/bin/env python3
"""
Sequence Randomizer

Randomizes sequences while preserving k-mer content.

Two methods:
1. Sampling: Simple shuffling (k-mer content will be approximate)
2. Euler: Exact k-mer preservation using Eulerian path (bonus)
"""

import random
import argparse
from collections import Counter, defaultdict


def read_fasta(filename):
    """Read a sequence from FASTA file."""
    sequence = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('>'):
                sequence.append(line.upper())
    return ''.join(sequence)


def count_kmers(sequence, k):
    """Count all k-mers in a sequence."""
    kmers = []
    for i in range(len(sequence) - k + 1):
        kmers.append(sequence[i:i+k])
    return Counter(kmers)


def randomize_sampling(sequence):
    """
    Simple randomization by shuffling.
    K-mer content will be approximate, not exact.
    """
    seq_list = list(sequence)
    random.shuffle(seq_list)
    return ''.join(seq_list)


def randomize_euler(sequence, k):
    """
    Exact k-mer preservation using Eulerian path.

    This builds a De Bruijn graph from k-mers and finds an Eulerian path.
    Since the path uses each k-mer exactly once (with multiplicity),
    the randomized sequence has exactly the same k-mer content.
    """
    if k < 1:
        return randomize_sampling(sequence)

    # Get all k-mers
    kmers = []
    for i in range(len(sequence) - k + 1):
        kmers.append(sequence[i:i+k])

    # Build De Bruijn graph
    # For each k-mer, create edge from first (k-1) letters to last (k-1) letters
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)

    for kmer in kmers:
        if k == 1:
            # Special case: 1-mers just shuffle
            continue
        source = kmer[:k-1]
        dest = kmer[1:]
        graph[source].append(dest)
        out_degree[source] += 1
        in_degree[dest] += 1

    # For k=1, just shuffle
    if k == 1:
        return randomize_sampling(sequence)

    # Find all nodes
    all_nodes = set(graph.keys()) | set(in_degree.keys())

    # Find starting node (has more outgoing than incoming edges)
    start_node = None
    for node in all_nodes:
        if out_degree[node] > in_degree[node]:
            start_node = node
            break

    # If no unbalanced node, start anywhere
    if start_node is None and graph:
        start_node = list(graph.keys())[0]

    if start_node is None:
        # No graph built, fall back to sampling
        return randomize_sampling(sequence)

    # Find Eulerian path using Hierholzer's algorithm
    path = []
    stack = [start_node]
    current_graph = {node: edges[:] for node, edges in graph.items()}  # Copy

    while stack:
        curr = stack[-1]
        if curr in current_graph and current_graph[curr]:
            # Randomly pick next edge (this is where randomization happens)
            next_node = random.choice(current_graph[curr])
            current_graph[curr].remove(next_node)
            stack.append(next_node)
        else:
            path.append(stack.pop())

    path.reverse()

    # Build sequence from path
    if not path:
        return randomize_sampling(sequence)

    # Start with first node
    result = path[0]
    # Add last character of each subsequent node
    for i in range(1, len(path)):
        result += path[i][-1]

    # If result is too short, pad with random letters
    if len(result) < len(sequence):
        alphabet = list(set(sequence))
        while len(result) < len(sequence):
            result += random.choice(alphabet)

    return result[:len(sequence)]


def compare_kmers(original_counts, randomized_counts):
    """
    Compare k-mer counts between original and randomized sequences.
    Returns a dictionary with comparison statistics.
    """
    all_kmers = set(original_counts.keys()) | set(randomized_counts.keys())

    exact_matches = 0
    total_kmers = len(all_kmers)

    differences = []
    for kmer in all_kmers:
        orig = original_counts.get(kmer, 0)
        rand = randomized_counts.get(kmer, 0)
        diff = abs(orig - rand)
        differences.append(diff)
        if diff == 0:
            exact_matches += 1

    return {
        'total_unique_kmers': total_kmers,
        'exact_matches': exact_matches,
        'match_percentage': (exact_matches / total_kmers * 100) if total_kmers > 0 else 0,
        'max_difference': max(differences) if differences else 0,
        'avg_difference': sum(differences) / len(differences) if differences else 0
    }


def save_fasta(sequence, filename, description):
    """Save sequence in FASTA format."""
    with open(filename, 'w') as f:
        f.write(f">{description}\n")
        for i in range(0, len(sequence), 80):
            f.write(sequence[i:i+80] + '\n')


def main():
    parser = argparse.ArgumentParser(description='Randomize sequence preserving k-mer content')
    parser.add_argument('--input', type=str, required=True,
                       help='Input sequence (FASTA format)')
    parser.add_argument('--output', type=str, default='randomized.fasta',
                       help='Output randomized sequence (default: randomized.fasta)')
    parser.add_argument('--k', type=int, default=2,
                       help='K-mer size (default: 2)')
    parser.add_argument('--method', type=str, default='sampling',
                       choices=['sampling', 'euler'],
                       help='Randomization method: sampling (approximate) or euler (exact)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility')
    parser.add_argument('--report', type=str, default='kmer_comparison.txt',
                       help='K-mer comparison report file')

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    print(f"Reading sequence from {args.input}...")
    original_seq = read_fasta(args.input)
    print(f"Sequence length: {len(original_seq)}")

    # Count original k-mers
    print(f"\nCounting {args.k}-mers in original sequence...")
    original_kmers = count_kmers(original_seq, args.k)
    print(f"Unique {args.k}-mers: {len(original_kmers)}")
    print(f"Total {args.k}-mers: {sum(original_kmers.values())}")

    # Randomize
    print(f"\nRandomizing using {args.method} method...")
    if args.method == 'sampling':
        randomized_seq = randomize_sampling(original_seq)
    else:
        randomized_seq = randomize_euler(original_seq, args.k)

    print(f"Randomized sequence length: {len(randomized_seq)}")

    # Count randomized k-mers
    print(f"\nCounting {args.k}-mers in randomized sequence...")
    randomized_kmers = count_kmers(randomized_seq, args.k)
    print(f"Unique {args.k}-mers: {len(randomized_kmers)}")
    print(f"Total {args.k}-mers: {sum(randomized_kmers.values())}")

    # Compare
    print("\nComparing k-mer content...")
    comparison = compare_kmers(original_kmers, randomized_kmers)

    print(f"  Total unique k-mers: {comparison['total_unique_kmers']}")
    print(f"  Exact matches: {comparison['exact_matches']}")
    print(f"  Match percentage: {comparison['match_percentage']:.2f}%")
    print(f"  Max difference: {comparison['max_difference']}")
    print(f"  Avg difference: {comparison['avg_difference']:.2f}")

    # Save randomized sequence
    save_fasta(randomized_seq, args.output,
               f"Randomized sequence (k={args.k}, method={args.method})")
    print(f"\nSaved randomized sequence to {args.output}")

    # Save detailed comparison report
    with open(args.report, 'w') as f:
        f.write("K-MER COMPARISON REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Original sequence: {args.input}\n")
        f.write(f"K-mer size: {args.k}\n")
        f.write(f"Randomization method: {args.method}\n")
        f.write(f"Sequence length: {len(original_seq)}\n\n")

        f.write("SUMMARY\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total unique k-mers: {comparison['total_unique_kmers']}\n")
        f.write(f"Exact matches: {comparison['exact_matches']}\n")
        f.write(f"Match percentage: {comparison['match_percentage']:.2f}%\n")
        f.write(f"Max difference: {comparison['max_difference']}\n")
        f.write(f"Avg difference: {comparison['avg_difference']:.2f}\n\n")

        f.write("K-MER COUNTS (showing differences)\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'K-mer':<15} {'Original':<12} {'Randomized':<12} {'Difference':<12}\n")
        f.write("-" * 70 + "\n")

        all_kmers = sorted(set(original_kmers.keys()) | set(randomized_kmers.keys()))
        for kmer in all_kmers:
            orig = original_kmers.get(kmer, 0)
            rand = randomized_kmers.get(kmer, 0)
            diff = abs(orig - rand)
            if diff > 0 or args.method == 'euler':  # Show all for euler, only diffs for sampling
                f.write(f"{kmer:<15} {orig:<12} {rand:<12} {diff:<12}\n")

    print(f"Saved comparison report to {args.report}")


if __name__ == '__main__':
    main()
