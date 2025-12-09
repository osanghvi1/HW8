#!/usr/bin/env python3
"""
Complete Assembly Pipeline

This runs the entire process from DNA generation through assembly.

Steps:
1. Generate random DNA
2. Simulate sequencing (create reads)
3. Extract k-mers
4. Build De Bruijn graph and assemble contigs
5. Calculate statistics and compare to Lander-Waterman prediction
"""

import argparse
import os
import random
from dna_generator import generate_dna, save_fasta
from sequencing_simulator import generate_reads, save_reads
from kmer_generator import generate_kmers_from_reads, save_kmers
from debruijn_assembler import DeBruijnGraph, calculate_n50, save_contigs, save_contig_info
from lander_waterman import calculate_lander_waterman


def run_complete_assembly(genome_length, coverage, read_length, kmer_length, error_rate, output_dir, seed=None):
    """
    Run the complete assembly pipeline.

    Parameters:
    -----------
    genome_length : int
        Length of genome to generate
    coverage : float
        Sequencing coverage
    read_length : int
        Length of each read
    kmer_length : int
        K-mer length for assembly
    error_rate : float
        Sequencing error rate
    output_dir : str
        Directory for output files
    seed : int
        Random seed for reproducibility

    Returns:
    --------
    dict : Results including observed and predicted statistics
    """

    if seed is not None:
        random.seed(seed)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 70)
    print("COMPLETE ASSEMBLY PIPELINE")
    print("=" * 70)
    print(f"Parameters:")
    print(f"  Genome length: {genome_length}")
    print(f"  Coverage: {coverage}x")
    print(f"  Read length: {read_length}")
    print(f"  K-mer length: {kmer_length}")
    print(f"  Error rate: {error_rate}")
    print(f"  Output directory: {output_dir}")
    print()

    # Step 1: Generate DNA
    print("STEP 1: Generating random DNA...")
    print("-" * 70)
    dna = generate_dna(genome_length)
    dna_file = os.path.join(output_dir, "genome.fasta")
    save_fasta(dna, dna_file, f"Generated genome - {genome_length}bp")
    print(f"Generated {len(dna)} bp genome")
    print(f"Saved to {dna_file}")
    print()

    # Step 2: Simulate sequencing
    print("STEP 2: Simulating sequencing...")
    print("-" * 70)
    reads = generate_reads(dna, read_length, coverage, error_rate)
    reads_file = os.path.join(output_dir, "reads.txt")
    save_reads(reads, reads_file)
    print(f"Saved to {reads_file}")
    print()

    # Step 3: Generate k-mers
    print("STEP 3: Generating k-mers...")
    print("-" * 70)
    kmer_counts = generate_kmers_from_reads(reads, kmer_length)
    kmers_file = os.path.join(output_dir, "kmers.txt")
    save_kmers(kmer_counts, kmers_file)

    total_kmers = sum(kmer_counts.values())
    unique_kmers = len(kmer_counts)
    print(f"Total k-mers: {total_kmers}")
    print(f"Unique k-mers: {unique_kmers}")
    print(f"Saved to {kmers_file}")
    print()

    # Step 4: Build graph and assemble
    print("STEP 4: Building De Bruijn graph and assembling...")
    print("-" * 70)
    graph = DeBruijnGraph(kmer_counts, kmer_length)
    contigs = graph.find_contigs()

    contigs_file = os.path.join(output_dir, "contigs.fasta")
    info_file = os.path.join(output_dir, "contig_info.txt")
    save_contigs(contigs, contigs_file)
    save_contig_info(contigs, info_file)

    lengths = [c['length'] for c in contigs]
    total_length = sum(lengths)
    n50 = calculate_n50(lengths)
    num_contigs = len(contigs)

    print(f"Assembled {num_contigs} contigs")
    print(f"Total length: {total_length}")
    print(f"N50: {n50}")
    print(f"Saved to {contigs_file}")
    print()

    # Step 5: Calculate Lander-Waterman prediction
    print("STEP 5: Comparing to Lander-Waterman prediction...")
    print("-" * 70)
    lw_stats = calculate_lander_waterman(genome_length, read_length, coverage)

    print(f"Lander-Waterman predicted contigs: {lw_stats['expected_contigs']:.2f}")
    print(f"Observed contigs: {num_contigs}")
    print(f"Difference: {num_contigs - lw_stats['expected_contigs']:.2f}")
    print()

    # Save summary
    summary_file = os.path.join(output_dir, "assembly_summary.txt")
    with open(summary_file, 'w') as f:
        f.write("ASSEMBLY SUMMARY\n")
        f.write("=" * 70 + "\n\n")
        f.write("Parameters:\n")
        f.write(f"  Genome length: {genome_length}\n")
        f.write(f"  Coverage: {coverage}x\n")
        f.write(f"  Read length: {read_length}\n")
        f.write(f"  K-mer length: {kmer_length}\n")
        f.write(f"  Error rate: {error_rate}\n\n")

        f.write("Results:\n")
        f.write(f"  Number of reads: {len(reads)}\n")
        f.write(f"  Unique k-mers: {unique_kmers}\n")
        f.write(f"  Number of contigs: {num_contigs}\n")
        f.write(f"  Total assembly length: {total_length}\n")
        f.write(f"  N50: {n50}\n")
        f.write(f"  Longest contig: {max(lengths)}\n\n")

        f.write("Lander-Waterman Prediction:\n")
        f.write(f"  Expected contigs: {lw_stats['expected_contigs']:.2f}\n")
        f.write(f"  Observed contigs: {num_contigs}\n")
        f.write(f"  Difference: {num_contigs - lw_stats['expected_contigs']:.2f}\n")
        f.write(f"  Ratio (observed/expected): {num_contigs / lw_stats['expected_contigs']:.2f}\n")

    print(f"Summary saved to {summary_file}")
    print()
    print("=" * 70)
    print("ASSEMBLY COMPLETE!")
    print("=" * 70)

    return {
        'genome_length': genome_length,
        'coverage': coverage,
        'read_length': read_length,
        'kmer_length': kmer_length,
        'error_rate': error_rate,
        'num_reads': len(reads),
        'unique_kmers': unique_kmers,
        'num_contigs': num_contigs,
        'total_length': total_length,
        'n50': n50,
        'longest_contig': max(lengths),
        'lw_expected_contigs': lw_stats['expected_contigs'],
        'lw_prob_covered': lw_stats['prob_covered']
    }


def main():
    parser = argparse.ArgumentParser(description='Run complete assembly pipeline')
    parser.add_argument('--length', type=int, default=1000,
                       help='Genome length (default: 1000)')
    parser.add_argument('--coverage', type=float, default=10.0,
                       help='Sequencing coverage (default: 10x)')
    parser.add_argument('--read_length', type=int, default=100,
                       help='Read length (default: 100)')
    parser.add_argument('--kmer', type=int, default=21,
                       help='K-mer length (default: 21)')
    parser.add_argument('--error_rate', type=float, default=0.0,
                       help='Sequencing error rate (default: 0.0)')
    parser.add_argument('--output', type=str, default='assembly_output',
                       help='Output directory (default: assembly_output)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility')

    args = parser.parse_args()

    run_complete_assembly(
        genome_length=args.length,
        coverage=args.coverage,
        read_length=args.read_length,
        kmer_length=args.kmer,
        error_rate=args.error_rate,
        output_dir=args.output,
        seed=args.seed
    )


if __name__ == '__main__':
    main()
