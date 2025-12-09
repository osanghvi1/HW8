#!/usr/bin/env python3
"""
Lander-Waterman Statistics

This calculates the expected number of contigs based on the Lander-Waterman equation.

The Lander-Waterman model predicts genome assembly statistics based on:
- Genome length (G)
- Read length (L)
- Coverage (c)

Key formula:
Expected number of contigs = e^(-c) * (number of reads)

Where coverage c = (number of reads * read length) / genome length
"""

import math
import argparse


def calculate_lander_waterman(genome_length, read_length, coverage):
    """
    Calculate expected assembly statistics using Lander-Waterman model.

    Parameters:
    -----------
    genome_length : int
        Length of the genome being sequenced
    read_length : int
        Length of each sequencing read
    coverage : float
        Sequencing coverage (e.g., 10x)

    Returns:
    --------
    dict : Statistics including expected number of contigs
    """

    # Number of reads
    num_reads = int((coverage * genome_length) / read_length)

    # Expected number of gaps (regions not covered by any read)
    # This is: G * e^(-c)
    expected_gaps = genome_length * math.exp(-coverage)

    # Expected number of contigs
    # Each gap creates a break, so contigs = gaps + 1
    # But more accurately: expected_contigs ≈ e^(-c) * num_reads
    expected_contigs = math.exp(-coverage) * num_reads

    # If coverage is high enough, we expect 1 contig
    if coverage >= 10:
        # At high coverage, we usually get near-complete assembly
        expected_contigs = max(1, int(expected_contigs))

    # Expected coverage at each position
    # This follows a Poisson distribution with mean = coverage
    # Probability a position is covered at least once: 1 - e^(-c)
    prob_covered = 1 - math.exp(-coverage)

    # Expected fraction of genome assembled
    expected_fraction_assembled = prob_covered

    return {
        'num_reads': num_reads,
        'expected_gaps': expected_gaps,
        'expected_contigs': expected_contigs,
        'prob_covered': prob_covered,
        'expected_fraction_assembled': expected_fraction_assembled
    }


def main():
    parser = argparse.ArgumentParser(description='Calculate Lander-Waterman statistics')
    parser.add_argument('--genome_length', type=int, required=True,
                       help='Length of genome')
    parser.add_argument('--read_length', type=int, required=True,
                       help='Length of each read')
    parser.add_argument('--coverage', type=float, required=True,
                       help='Sequencing coverage')

    args = parser.parse_args()

    print("Lander-Waterman Statistics")
    print("=" * 60)
    print(f"Genome length: {args.genome_length}")
    print(f"Read length: {args.read_length}")
    print(f"Coverage: {args.coverage}x")
    print()

    stats = calculate_lander_waterman(args.genome_length, args.read_length, args.coverage)

    print("Expected assembly statistics:")
    print(f"  Number of reads: {stats['num_reads']}")
    print(f"  Expected gaps: {stats['expected_gaps']:.2f}")
    print(f"  Expected number of contigs: {stats['expected_contigs']:.2f}")
    print(f"  Probability each base is covered: {stats['prob_covered']:.4f}")
    print(f"  Expected fraction assembled: {stats['expected_fraction_assembled']:.4f}")


if __name__ == '__main__':
    main()
