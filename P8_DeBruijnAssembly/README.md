# P8: De Bruijn Graph Assembly

## Project Overview

This project simulates the complete DNA sequencing and assembly pipeline using De Bruijn graphs. It demonstrates how modern DNA sequencers break up genomes into short reads, and how we can reassemble the original sequence from these fragments.

## What This Does

1. **Generates** a random DNA sequence
2. **Simulates** a sequencing machine that breaks it into short reads
3. **Builds** k-mers from the reads
4. **Assembles** the original sequence using a De Bruijn graph
5. **Tests** how different parameters affect assembly quality

## Quick Start

```bash
# Run a simple assembly example
python3 run_assembly.py --length 1000 --coverage 10 --read_length 100 --kmer 21

# Run comprehensive tests
python3 simple_test.py
```

## Files

### Core Programs (no dependencies needed)
- `dna_generator.py` - Creates random DNA sequences
- `sequencing_simulator.py` - Simulates a sequencing machine
- `kmer_generator.py` - Extracts k-mers from reads
- `debruijn_assembler.py` - Builds graph and assembles contigs
- `lander_waterman.py` - Calculates expected number of contigs

### Complete Pipeline
- `run_assembly.py` - Runs entire pipeline from DNA generation through assembly
- `simple_test.py` - Tests with different parameters (no extra packages needed)

### Advanced Testing (requires pandas, matplotlib)
- `test_assembly.py` - Comprehensive testing with statistics
- `visualize_results.py` - Generate plots (bonus)

### Results
- `simple_test_results/` - Test outputs and summary report
- `test_example/` - Example assembly output
- `P8_REPORT.md` - Complete project report with analysis

## How to Use

### Option 1: Run Complete Pipeline

This runs everything in one command:

```bash
python3 run_assembly.py --length 1000 --coverage 10 --read_length 100 --kmer 21 --output my_assembly
```

Output files will be in the `my_assembly/` directory:
- `genome.fasta` - The generated DNA sequence
- `reads.txt` - Simulated sequencing reads
- `kmers.txt` - Extracted k-mers with counts
- `contigs.fasta` - Assembled contigs
- `assembly_summary.txt` - Statistics and results

### Option 2: Run Each Step Separately

```bash
# Step 1: Generate DNA
python3 dna_generator.py --length 1000 --output genome.fasta

# Step 2: Simulate sequencing
python3 sequencing_simulator.py --input genome.fasta --coverage 10 --read_length 100 --output reads.txt

# Step 3: Extract k-mers
python3 kmer_generator.py --input reads.txt --k 21 --output kmers.txt

# Step 4: Assemble
python3 debruijn_assembler.py --input kmers.txt --output contigs.fasta
```

### Option 3: Run Tests

Run the simple test suite (no extra packages needed):

```bash
python3 simple_test.py
```

This tests:
- Different genome lengths (500, 1000, 2000 bp)
- Different coverage levels (5x, 10x, 20x)
- Different error rates (0%, 0.1%, 1%)

Results are saved to `simple_test_results/SUMMARY_REPORT.txt`

## Parameters Explained

- `--length` - How long the DNA sequence should be (e.g., 1000 bp)
- `--coverage` - How many times each base gets sequenced on average (e.g., 10x)
- `--read_length` - Length of each sequencing read (e.g., 100 bp)
- `--kmer` or `--k` - K-mer size for assembly (e.g., 21)
- `--error_rate` - Sequencing error probability (e.g., 0.01 for 1% errors)
- `--seed` - Random seed for reproducible results

## Requirements

### Basic Use (no installation needed)
The core programs work with just Python 3.6+. No extra packages required.

### Advanced Testing and Visualization
```bash
pip3 install pandas matplotlib numpy openpyxl
```

or

```bash
pip3 install -r requirements.txt
```

## Understanding the Output

### Assembly Statistics

**Number of contigs:** How many separate DNA fragments were assembled. Fewer is better (ideally 1).

**N50:** A measure of assembly quality. If N50 = 500, that means half your assembly is in pieces 500bp or longer. Higher is better.

**Total length:** Sum of all contig lengths. Should be close to the original genome length.

### Lander-Waterman Prediction

This is a mathematical prediction of how many contigs you should get based on coverage.

- If observed matches predicted, assembly worked as expected
- If observed >> predicted, there may be issues (errors, repeats, etc.)

## Example Results

With 1000bp genome, 10x coverage, no errors:
```
Number of contigs: 1
Total length: 984 bp
N50: 984 bp
Lander-Waterman predicted: 1.00 contigs
```

With same setup but 1% error rate:
```
Number of contigs: 285
Total length: 7873 bp
N50: 27 bp
Lander-Waterman predicted: 1.00 contigs
```

The error rate dramatically fragments the assembly!

## Project Report

See **P8_REPORT.md** for:
- Detailed methodology
- Complete test results
- Analysis and discussion
- Answers to assignment questions

## Assignment Deliverables

This project fulfills P8 requirements:

**50 points - Program that:**
- ✅ Generates random DNA text with letter frequencies
- ✅ Simulates sequencing with read_length, coverage, error rate
- ✅ Generates k-mers from reads
- ✅ Constructs De Bruijn graph and traces contigs
- ✅ Reports sequence fragments and connections

**50 points - Testing:**
- ✅ Tests sequences of varying lengths
- ✅ Compares to Lander-Waterman equation
- ✅ Analyzes error rate effect on predictions

**Bonus features:**
- Graph visualization script included (visualize_results.py)
- Repetitive sequence support in DNA generator (--repeat_seq option)
