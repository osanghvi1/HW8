#!/usr/bin/env python3
"""
DNA Sequence Generator

This creates random DNA sequences for testing assembly algorithms.
You can control the letter frequencies and add repeats to make it more realistic.
"""

import random
import argparse


def generate_dna(length, frequencies=None, repeats=None):
    """
    Generate a random DNA sequence.

    Parameters:
    -----------
    length : int
        How long the DNA sequence should be
    frequencies : dict
        How often each letter appears. Example: {'A': 0.3, 'T': 0.3, 'G': 0.2, 'C': 0.2}
        If None, all letters appear equally (25% each)
    repeats : list of dict
        List of repetitive sequences to add. Each dict has:
        - 'sequence': the DNA string to repeat
        - 'count': how many times to include it
        Example: [{'sequence': 'ATGATG', 'count': 5}]

    Returns:
    --------
    str : The generated DNA sequence
    """

    # If no frequencies given, use equal frequencies
    if frequencies is None:
        frequencies = {'A': 0.25, 'T': 0.25, 'G': 0.25, 'C': 0.25}

    # Make sure frequencies add up to 1.0
    total = sum(frequencies.values())
    if abs(total - 1.0) > 0.001:
        print(f"Warning: frequencies sum to {total}, normalizing to 1.0")
        frequencies = {base: freq/total for base, freq in frequencies.items()}

    # Start with empty sequence
    dna = []

    # Add repeated sequences first (if any)
    repeat_length = 0
    if repeats:
        for repeat_info in repeats:
            seq = repeat_info['sequence']
            count = repeat_info['count']
            for i in range(count):
                dna.append(seq)
            repeat_length += len(seq) * count

    # How much random DNA do we need to add?
    remaining = length - repeat_length
    if remaining < 0:
        print(f"Warning: repeats are longer than target length. Trimming to {length}")
        dna_str = ''.join(dna)[:length]
        return dna_str

    # Generate random DNA for the rest
    bases = list(frequencies.keys())
    weights = list(frequencies.values())

    for i in range(remaining):
        # Pick a random base according to the frequencies
        base = random.choices(bases, weights=weights)[0]
        dna.append(base)

    # Shuffle everything together so repeats aren't all at the start
    random.shuffle(dna)

    return ''.join(dna)


def save_fasta(sequence, filename, description="Generated DNA sequence"):
    """
    Save DNA sequence in FASTA format.

    FASTA format looks like:
    >description
    ATGCATGC...
    """
    with open(filename, 'w') as f:
        f.write(f">{description}\n")
        # Write sequence in lines of 80 characters (standard FASTA format)
        for i in range(0, len(sequence), 80):
            f.write(sequence[i:i+80] + '\n')


def main():
    parser = argparse.ArgumentParser(description='Generate random DNA sequences')
    parser.add_argument('--length', type=int, default=1000,
                       help='Length of DNA sequence (default: 1000)')
    parser.add_argument('--output', type=str, default='generated_dna.fasta',
                       help='Output filename (default: generated_dna.fasta)')
    parser.add_argument('--freq_a', type=float, default=0.25,
                       help='Frequency of A (default: 0.25)')
    parser.add_argument('--freq_t', type=float, default=0.25,
                       help='Frequency of T (default: 0.25)')
    parser.add_argument('--freq_g', type=float, default=0.25,
                       help='Frequency of G (default: 0.25)')
    parser.add_argument('--freq_c', type=float, default=0.25,
                       help='Frequency of C (default: 0.25)')
    parser.add_argument('--repeat_seq', type=str, default=None,
                       help='Sequence to repeat (e.g., ATGATG)')
    parser.add_argument('--repeat_count', type=int, default=0,
                       help='How many times to include the repeat')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility')

    args = parser.parse_args()

    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)

    # Build frequencies dictionary
    frequencies = {
        'A': args.freq_a,
        'T': args.freq_t,
        'G': args.freq_g,
        'C': args.freq_c
    }

    # Build repeats list
    repeats = None
    if args.repeat_seq and args.repeat_count > 0:
        repeats = [{'sequence': args.repeat_seq, 'count': args.repeat_count}]

    # Generate the DNA
    print("Generating DNA sequence...")
    print(f"  Length: {args.length}")
    print(f"  Frequencies: A={args.freq_a}, T={args.freq_t}, G={args.freq_g}, C={args.freq_c}")
    if repeats:
        print(f"  Repeats: {args.repeat_seq} x {args.repeat_count}")

    dna = generate_dna(args.length, frequencies, repeats)

    # Count actual frequencies
    counts = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
    for base in dna:
        if base in counts:
            counts[base] += 1

    print("\nActual composition:")
    for base in ['A', 'T', 'G', 'C']:
        freq = counts[base] / len(dna)
        print(f"  {base}: {counts[base]} ({freq:.3f})")

    # Save to file
    save_fasta(dna, args.output, f"Generated DNA - length {len(dna)}")
    print(f"\nSaved to {args.output}")


if __name__ == '__main__':
    main()
