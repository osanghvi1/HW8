#!/usr/bin/env python3
"""
Assembly Testing

This tests the assembly pipeline with different parameters and compares
results to Lander-Waterman predictions.

Tests:
1. Varying genome lengths
2. Varying coverage
3. Varying error rates
"""

import os
import random
import pandas as pd
from run_assembly import run_complete_assembly


def test_genome_lengths():
    """
    Test assembly with different genome lengths.
    """
    print("\n" + "=" * 70)
    print("TEST 1: VARYING GENOME LENGTHS")
    print("=" * 70)

    # Parameters
    genome_lengths = [500, 1000, 2000, 5000]
    coverage = 10.0
    read_length = 100
    kmer_length = 21
    error_rate = 0.0
    replicates = 5

    results = []

    for length in genome_lengths:
        print(f"\nTesting genome length: {length}")
        print("-" * 70)

        for rep in range(replicates):
            output_dir = f"test_results/length_{length}_rep_{rep+1}"
            seed = length * 1000 + rep

            result = run_complete_assembly(
                genome_length=length,
                coverage=coverage,
                read_length=read_length,
                kmer_length=kmer_length,
                error_rate=error_rate,
                output_dir=output_dir,
                seed=seed
            )

            result['replicate'] = rep + 1
            results.append(result)

    # Save results
    df = pd.DataFrame(results)
    df.to_csv('test_results/genome_length_test.csv', index=False)

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY: Genome Length Test")
    print("=" * 70)
    summary = df.groupby('genome_length').agg({
        'num_contigs': ['mean', 'std'],
        'lw_expected_contigs': 'mean',
        'n50': ['mean', 'std']
    })
    print(summary)

    return df


def test_coverage_levels():
    """
    Test assembly with different coverage levels.
    """
    print("\n" + "=" * 70)
    print("TEST 2: VARYING COVERAGE LEVELS")
    print("=" * 70)

    # Parameters
    genome_length = 2000
    coverages = [5.0, 10.0, 20.0, 30.0]
    read_length = 100
    kmer_length = 21
    error_rate = 0.0
    replicates = 5

    results = []

    for cov in coverages:
        print(f"\nTesting coverage: {cov}x")
        print("-" * 70)

        for rep in range(replicates):
            output_dir = f"test_results/coverage_{cov}_rep_{rep+1}"
            seed = int(cov * 1000) + rep

            result = run_complete_assembly(
                genome_length=genome_length,
                coverage=cov,
                read_length=read_length,
                kmer_length=kmer_length,
                error_rate=error_rate,
                output_dir=output_dir,
                seed=seed
            )

            result['replicate'] = rep + 1
            results.append(result)

    # Save results
    df = pd.DataFrame(results)
    df.to_csv('test_results/coverage_test.csv', index=False)

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY: Coverage Test")
    print("=" * 70)
    summary = df.groupby('coverage').agg({
        'num_contigs': ['mean', 'std'],
        'lw_expected_contigs': 'mean',
        'n50': ['mean', 'std']
    })
    print(summary)

    return df


def test_error_rates():
    """
    Test assembly with different sequencing error rates.
    """
    print("\n" + "=" * 70)
    print("TEST 3: VARYING ERROR RATES")
    print("=" * 70)

    # Parameters
    genome_length = 2000
    coverage = 10.0
    read_length = 100
    kmer_length = 21
    error_rates = [0.0, 0.001, 0.005, 0.01]
    replicates = 5

    results = []

    for err in error_rates:
        print(f"\nTesting error rate: {err}")
        print("-" * 70)

        for rep in range(replicates):
            output_dir = f"test_results/error_{err}_rep_{rep+1}"
            seed = int(err * 10000) + rep

            result = run_complete_assembly(
                genome_length=genome_length,
                coverage=coverage,
                read_length=read_length,
                kmer_length=kmer_length,
                error_rate=err,
                output_dir=output_dir,
                seed=seed
            )

            result['replicate'] = rep + 1
            results.append(result)

    # Save results
    df = pd.DataFrame(results)
    df.to_csv('test_results/error_rate_test.csv', index=False)

    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY: Error Rate Test")
    print("=" * 70)
    summary = df.groupby('error_rate').agg({
        'num_contigs': ['mean', 'std'],
        'lw_expected_contigs': 'mean',
        'n50': ['mean', 'std']
    })
    print(summary)

    return df


def generate_final_report(df_lengths, df_coverage, df_errors):
    """
    Generate a comprehensive test report.
    """
    report_file = 'test_results/TEST_REPORT.txt'

    with open(report_file, 'w') as f:
        f.write("ASSEMBLY TESTING REPORT\n")
        f.write("=" * 70 + "\n\n")

        # Test 1: Genome Lengths
        f.write("TEST 1: VARYING GENOME LENGTHS\n")
        f.write("-" * 70 + "\n")
        f.write("Question: How does genome length affect assembly quality?\n\n")

        summary = df_lengths.groupby('genome_length').agg({
            'num_contigs': ['mean', 'std'],
            'lw_expected_contigs': 'mean',
            'n50': ['mean', 'std'],
            'total_length': ['mean', 'std']
        })

        f.write("Results:\n")
        f.write(str(summary) + "\n\n")

        # Calculate accuracy
        for length in df_lengths['genome_length'].unique():
            subset = df_lengths[df_lengths['genome_length'] == length]
            obs_mean = subset['num_contigs'].mean()
            pred_mean = subset['lw_expected_contigs'].mean()
            ratio = obs_mean / pred_mean if pred_mean > 0 else 0
            f.write(f"  Length {length}: Observed/Expected = {ratio:.2f}\n")

        f.write("\n")

        # Test 2: Coverage
        f.write("\nTEST 2: VARYING COVERAGE LEVELS\n")
        f.write("-" * 70 + "\n")
        f.write("Question: How does coverage affect assembly quality?\n\n")

        summary = df_coverage.groupby('coverage').agg({
            'num_contigs': ['mean', 'std'],
            'lw_expected_contigs': 'mean',
            'n50': ['mean', 'std']
        })

        f.write("Results:\n")
        f.write(str(summary) + "\n\n")

        for cov in df_coverage['coverage'].unique():
            subset = df_coverage[df_coverage['coverage'] == cov]
            obs_mean = subset['num_contigs'].mean()
            pred_mean = subset['lw_expected_contigs'].mean()
            ratio = obs_mean / pred_mean if pred_mean > 0 else 0
            f.write(f"  Coverage {cov}x: Observed/Expected = {ratio:.2f}\n")

        f.write("\n")

        # Test 3: Error Rates
        f.write("\nTEST 3: VARYING ERROR RATES\n")
        f.write("-" * 70 + "\n")
        f.write("Question: Does error rate affect Lander-Waterman accuracy?\n\n")

        summary = df_errors.groupby('error_rate').agg({
            'num_contigs': ['mean', 'std'],
            'lw_expected_contigs': 'mean',
            'n50': ['mean', 'std']
        })

        f.write("Results:\n")
        f.write(str(summary) + "\n\n")

        for err in df_errors['error_rate'].unique():
            subset = df_errors[df_errors['error_rate'] == err]
            obs_mean = subset['num_contigs'].mean()
            pred_mean = subset['lw_expected_contigs'].mean()
            ratio = obs_mean / pred_mean if pred_mean > 0 else 0
            f.write(f"  Error rate {err}: Observed/Expected = {ratio:.2f}\n")

        f.write("\n\n")

        # Conclusions
        f.write("CONCLUSIONS\n")
        f.write("-" * 70 + "\n\n")

        f.write("1. Genome Length:\n")
        f.write("   The Lander-Waterman equation predicts that longer genomes will have\n")
        f.write("   proportionally more contigs at the same coverage level.\n\n")

        f.write("2. Coverage:\n")
        f.write("   Higher coverage leads to fewer contigs and better assemblies.\n")
        f.write("   The Lander-Waterman prediction improves at higher coverage.\n\n")

        f.write("3. Error Rate:\n")
        f.write("   Sequencing errors increase the number of contigs because they create\n")
        f.write("   false branch points in the De Bruijn graph. The Lander-Waterman\n")
        f.write("   equation does not account for errors, so its predictions become less\n")
        f.write("   accurate as error rate increases.\n\n")

    print(f"\nFinal report saved to {report_file}")


def main():
    # Create results directory
    os.makedirs('test_results', exist_ok=True)

    print("\n" + "=" * 70)
    print("COMPREHENSIVE ASSEMBLY TESTING")
    print("=" * 70)
    print("\nThis will run multiple tests with varying parameters.")
    print("Each test uses 5 replicates to get reliable statistics.")
    print()

    # Run tests
    df_lengths = test_genome_lengths()
    df_coverage = test_coverage_levels()
    df_errors = test_error_rates()

    # Generate final report
    generate_final_report(df_lengths, df_coverage, df_errors)

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETE!")
    print("=" * 70)
    print("\nResults saved to test_results/")
    print("  - genome_length_test.csv")
    print("  - coverage_test.csv")
    print("  - error_rate_test.csv")
    print("  - TEST_REPORT.txt")


if __name__ == '__main__':
    main()
