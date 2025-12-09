#!/usr/bin/env python3
"""
Visualize Assembly Results

Creates plots showing:
1. Observed vs Predicted contigs
2. Effect of coverage on assembly quality
3. Effect of error rate on assembly quality
"""

import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_genome_length_results():
    """Plot results for varying genome lengths."""
    df = pd.read_csv('test_results/genome_length_test.csv')

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Number of contigs
    summary = df.groupby('genome_length').agg({
        'num_contigs': ['mean', 'std'],
        'lw_expected_contigs': 'mean'
    })

    lengths = summary.index
    obs_mean = summary[('num_contigs', 'mean')]
    obs_std = summary[('num_contigs', 'std')]
    pred = summary[('lw_expected_contigs', 'mean')]

    axes[0].errorbar(lengths, obs_mean, yerr=obs_std, marker='o', label='Observed', capsize=5)
    axes[0].plot(lengths, pred, marker='s', label='Lander-Waterman', linestyle='--')
    axes[0].set_xlabel('Genome Length (bp)')
    axes[0].set_ylabel('Number of Contigs')
    axes[0].set_title('Contigs vs Genome Length')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: N50
    summary_n50 = df.groupby('genome_length')['n50'].agg(['mean', 'std'])
    axes[1].errorbar(lengths, summary_n50['mean'], yerr=summary_n50['std'], marker='o', capsize=5)
    axes[1].set_xlabel('Genome Length (bp)')
    axes[1].set_ylabel('N50')
    axes[1].set_title('N50 vs Genome Length')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('test_results/genome_length_plot.png', dpi=300)
    print("Saved: test_results/genome_length_plot.png")


def plot_coverage_results():
    """Plot results for varying coverage levels."""
    df = pd.read_csv('test_results/coverage_test.csv')

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Number of contigs
    summary = df.groupby('coverage').agg({
        'num_contigs': ['mean', 'std'],
        'lw_expected_contigs': 'mean'
    })

    coverages = summary.index
    obs_mean = summary[('num_contigs', 'mean')]
    obs_std = summary[('num_contigs', 'std')]
    pred = summary[('lw_expected_contigs', 'mean')]

    axes[0].errorbar(coverages, obs_mean, yerr=obs_std, marker='o', label='Observed', capsize=5)
    axes[0].plot(coverages, pred, marker='s', label='Lander-Waterman', linestyle='--')
    axes[0].set_xlabel('Coverage')
    axes[0].set_ylabel('Number of Contigs')
    axes[0].set_title('Contigs vs Coverage')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: N50
    summary_n50 = df.groupby('coverage')['n50'].agg(['mean', 'std'])
    axes[1].errorbar(coverages, summary_n50['mean'], yerr=summary_n50['std'], marker='o', capsize=5)
    axes[1].set_xlabel('Coverage')
    axes[1].set_ylabel('N50')
    axes[1].set_title('N50 vs Coverage')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('test_results/coverage_plot.png', dpi=300)
    print("Saved: test_results/coverage_plot.png")


def plot_error_rate_results():
    """Plot results for varying error rates."""
    df = pd.read_csv('test_results/error_rate_test.csv')

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Number of contigs
    summary = df.groupby('error_rate').agg({
        'num_contigs': ['mean', 'std'],
        'lw_expected_contigs': 'mean'
    })

    error_rates = summary.index
    obs_mean = summary[('num_contigs', 'mean')]
    obs_std = summary[('num_contigs', 'std')]
    pred = summary[('lw_expected_contigs', 'mean')]

    axes[0].errorbar(error_rates, obs_mean, yerr=obs_std, marker='o', label='Observed', capsize=5)
    axes[0].plot(error_rates, pred, marker='s', label='Lander-Waterman', linestyle='--')
    axes[0].set_xlabel('Error Rate')
    axes[0].set_ylabel('Number of Contigs')
    axes[0].set_title('Contigs vs Error Rate')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: Ratio (observed/expected)
    ratio = obs_mean / pred
    axes[1].plot(error_rates, ratio, marker='o')
    axes[1].axhline(y=1.0, color='r', linestyle='--', label='Perfect prediction')
    axes[1].set_xlabel('Error Rate')
    axes[1].set_ylabel('Observed / Expected')
    axes[1].set_title('Lander-Waterman Accuracy vs Error Rate')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('test_results/error_rate_plot.png', dpi=300)
    print("Saved: test_results/error_rate_plot.png")


def main():
    print("Generating visualization plots...")

    if not os.path.exists('test_results/genome_length_test.csv'):
        print("Error: Test results not found. Run test_assembly.py first.")
        return

    plot_genome_length_results()
    plot_coverage_results()
    plot_error_rate_results()

    print("\nAll plots generated!")


if __name__ == '__main__':
    main()
