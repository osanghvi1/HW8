#!/usr/bin/env python3
"""
K-mer Generator

This extracts all k-mers from sequencing reads.
A k-mer is a substring of length k.

For example, from the read "ATGCA" with k=3, we get:
- ATG
- TGC
- GCA
"""

import argparse
from collections import Counter


def extract_kmers(sequence, k):
    """
    Extract all k-mers from a sequence.

    Parameters:
    -----------
    sequence : str
        DNA sequence
    k : int
        Length of k-mers

    Returns:
    --------
    list : List of k-mers
    """
    kmers = []

    # Slide a window of size k along the sequence
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k]
        kmers.append(kmer)

    return kmers


def generate_kmers_from_reads(reads, k):
    """
    Extract all k-mers from a list of reads.

    Parameters:
    -----------
    reads : list
        List of read sequences
    k : int
        Length of k-mers

    Returns:
    --------
    Counter : Dictionary mapping each k-mer to how many times it appears
    """
    all_kmers = []

    for read in reads:
        kmers = extract_kmers(read, k)
        all_kmers.extend(kmers)

    # Count how many times each k-mer appears
    kmer_counts = Counter(all_kmers)

    return kmer_counts


def read_reads_file(filename):
    """
    Read reads from a text file (one read per line).
    """
    reads = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and FASTA headers
            if line and not line.startswith('>'):
                reads.append(line)
    return reads


def save_kmers(kmer_counts, filename):
    """
    Save k-mers and their counts to a file.

    Format: kmer\tcount
    """
    with open(filename, 'w') as f:
        f.write("kmer\tcount\n")
        # Sort by k-mer alphabetically
        for kmer in sorted(kmer_counts.keys()):
            count = kmer_counts[kmer]
            f.write(f"{kmer}\t{count}\n")


def main():
    parser = argparse.ArgumentParser(description='Generate k-mers from sequencing reads')
    parser.add_argument('--input', type=str, required=True,
                       help='Input reads file')
    parser.add_argument('--output', type=str, default='kmers.txt',
                       help='Output k-mers file (default: kmers.txt)')
    parser.add_argument('--k', type=int, default=21,
                       help='K-mer length (default: 21)')

    args = parser.parse_args()

    # Read the reads
    print(f"Reading reads from {args.input}...")
    reads = read_reads_file(args.input)
    print(f"Loaded {len(reads)} reads")

    if len(reads) == 0:
        print("Error: No reads found!")
        return

    # Show read length info
    read_lengths = [len(r) for r in reads]
    print(f"Read length range: {min(read_lengths)} to {max(read_lengths)}")

    # Generate k-mers
    print(f"\nGenerating {args.k}-mers...")
    kmer_counts = generate_kmers_from_reads(reads, args.k)

    # Print statistics
    total_kmers = sum(kmer_counts.values())
    unique_kmers = len(kmer_counts)

    print(f"\nK-mer statistics:")
    print(f"  Total k-mers: {total_kmers}")
    print(f"  Unique k-mers: {unique_kmers}")
    print(f"  Average coverage per k-mer: {total_kmers / unique_kmers:.2f}x")

    # Show most common k-mers
    print(f"\nMost common {args.k}-mers:")
    for kmer, count in kmer_counts.most_common(10):
        print(f"  {kmer}: {count}")

    # Save k-mers
    save_kmers(kmer_counts, args.output)
    print(f"\nSaved {unique_kmers} unique k-mers to {args.output}")


if __name__ == '__main__':
    main()
