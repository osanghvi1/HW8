#!/usr/bin/env python3
"""
Sequencing Simulator

This simulates a DNA sequencing machine. It takes a long DNA sequence and
breaks it into many short "reads" just like a real sequencer would.

You can control:
- read_length: how long each read is
- coverage: how many times each position gets sequenced (on average)
- error_rate: how often a wrong base gets called
"""

import random
import argparse


def read_fasta(filename):
    """
    Read a DNA sequence from a FASTA file.

    FASTA format looks like:
    >description
    ATGCATGC...
    """
    sequence = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip the description line (starts with >)
            if line.startswith('>'):
                continue
            # Add sequence data
            sequence.append(line)
    return ''.join(sequence)


def introduce_error(base):
    """
    Change a DNA base to a different random base.

    Example: 'A' might become 'T', 'G', or 'C'
    """
    bases = ['A', 'T', 'G', 'C']
    # Remove the current base from options
    bases.remove(base)
    # Pick one of the other three bases
    return random.choice(bases)


def generate_reads(dna_sequence, read_length, coverage, error_rate):
    """
    Simulate sequencing by generating random reads from the DNA.

    Parameters:
    -----------
    dna_sequence : str
        The original DNA sequence to sequence
    read_length : int
        Length of each read (e.g., 100 bases)
    coverage : float
        How many times to sequence each position on average (e.g., 10x means each base
        gets sequenced about 10 times)
    error_rate : float
        Probability of a sequencing error (e.g., 0.01 means 1% error rate)

    Returns:
    --------
    list : List of read sequences (strings)
    """

    # Calculate how many reads we need
    # Coverage = (number_of_reads * read_length) / genome_length
    # So: number_of_reads = (coverage * genome_length) / read_length
    genome_length = len(dna_sequence)
    num_reads = int((coverage * genome_length) / read_length)

    print(f"Generating {num_reads} reads...")
    print(f"  Genome length: {genome_length}")
    print(f"  Read length: {read_length}")
    print(f"  Target coverage: {coverage}x")
    print(f"  Error rate: {error_rate}")

    reads = []

    for i in range(num_reads):
        # Pick a random starting position
        # Make sure we don't go past the end
        max_start = genome_length - read_length
        if max_start <= 0:
            print("Warning: read_length is longer than genome!")
            break

        start_pos = random.randint(0, max_start)
        end_pos = start_pos + read_length

        # Extract the read
        read = dna_sequence[start_pos:end_pos]

        # Add sequencing errors
        read_with_errors = []
        for base in read:
            # Should we introduce an error?
            if random.random() < error_rate:
                # Yes, make an error
                base = introduce_error(base)
            read_with_errors.append(base)

        reads.append(''.join(read_with_errors))

    print(f"Generated {len(reads)} reads")

    # Calculate actual coverage
    total_bases_sequenced = len(reads) * read_length
    actual_coverage = total_bases_sequenced / genome_length
    print(f"Actual coverage: {actual_coverage:.2f}x")

    return reads


def save_reads(reads, filename):
    """
    Save reads to a text file (one read per line).
    """
    with open(filename, 'w') as f:
        for i, read in enumerate(reads):
            f.write(f"{read}\n")


def save_reads_fasta(reads, filename):
    """
    Save reads in FASTA format.
    """
    with open(filename, 'w') as f:
        for i, read in enumerate(reads):
            f.write(f">read_{i+1}\n")
            f.write(f"{read}\n")


def main():
    parser = argparse.ArgumentParser(description='Simulate DNA sequencing')
    parser.add_argument('--input', type=str, required=True,
                       help='Input DNA sequence (FASTA format)')
    parser.add_argument('--output', type=str, default='reads.txt',
                       help='Output filename (default: reads.txt)')
    parser.add_argument('--read_length', type=int, default=100,
                       help='Length of each read (default: 100)')
    parser.add_argument('--coverage', type=float, default=10.0,
                       help='Sequencing coverage (default: 10x)')
    parser.add_argument('--error_rate', type=float, default=0.0,
                       help='Sequencing error rate (default: 0.0)')
    parser.add_argument('--format', type=str, default='txt', choices=['txt', 'fasta'],
                       help='Output format (default: txt)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility')

    args = parser.parse_args()

    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)

    # Read the input DNA
    print(f"Reading DNA from {args.input}...")
    dna = read_fasta(args.input)
    print(f"Loaded {len(dna)} bases")

    # Generate reads
    reads = generate_reads(dna, args.read_length, args.coverage, args.error_rate)

    # Save reads
    if args.format == 'fasta':
        save_reads_fasta(reads, args.output)
    else:
        save_reads(reads, args.output)

    print(f"\nSaved {len(reads)} reads to {args.output}")


if __name__ == '__main__':
    main()
