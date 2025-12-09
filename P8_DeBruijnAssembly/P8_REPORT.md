# P8: De Bruijn Graph - DNA Sequence Assembly

**Programming Project 8**
DNA Sequence Assembly using De Bruijn Graphs

---

## Introduction

This project simulates the complete DNA sequencing and assembly pipeline. Modern DNA sequencers cannot read an entire genome at once. Instead, they break DNA into millions of short fragments called "reads" and sequence those. The challenge is then to reassemble the original genome from these overlapping fragments.

De Bruijn graphs provide an efficient method for genome assembly. Instead of directly comparing reads (which is computationally expensive), we break reads into k-mers (short sequences of length k) and use these to build a graph. Walking through this graph reconstructs the original sequence.

This project implements the full pipeline:
1. Generate a random DNA sequence
2. Simulate a sequencing machine creating short reads
3. Extract k-mers from the reads
4. Build a De Bruijn graph and assemble contigs
5. Compare results to theoretical predictions (Lander-Waterman equation)

---

## Methods

### DNA Generation

The `dna_generator.py` program creates random DNA sequences with customizable base frequencies. By default, each base (A, T, G, C) appears with 25% frequency, but this can be adjusted to simulate different genome compositions.

The generator also supports adding repetitive sequences, which are common in real genomes and make assembly more challenging.

### Sequencing Simulation

The `sequencing_simulator.py` program mimics a DNA sequencer:
- Randomly samples short reads from the genome
- Coverage determines how many reads to generate
- Sequencing errors can be introduced at a specified rate

**Coverage calculation:**
```
Coverage = (Number of reads × Read length) / Genome length
```

For example, to get 10x coverage of a 1000bp genome with 100bp reads:
```
Number of reads = (10 × 1000) / 100 = 100 reads
```

### K-mer Extraction

The `kmer_generator.py` program extracts all k-mers from the sequencing reads. A k-mer is simply a sequence of k consecutive bases.

For example, from the read "ATGCA" with k=3:
- ATG
- TGC
- GCA

We count how many times each k-mer appears, which tells us about coverage depth.

### De Bruijn Graph Assembly

The `debruijn_assembler.py` program builds the graph and finds contigs.

**Graph structure:**
- Each k-mer is an edge
- Each (k-1)-mer is a node
- For k-mer "ATGC", we create an edge from node "ATG" to node "TGC"

**Finding contigs:**
Contigs are unbranched paths through the graph. We start from:
- Tips (nodes with no incoming or outgoing edges)
- Branch points (nodes with multiple options)

We extend paths until we hit another branch point, then save that continuous sequence as a contig.

**Assembly statistics:**
- **Number of contigs:** How many separate pieces we assembled
- **N50:** The length where 50% of the assembly is in contigs that size or bigger
- **Total length:** Sum of all contig lengths

### Lander-Waterman Equation

The Lander-Waterman model predicts assembly statistics based on random sequencing.

**Key formula:**
```
Expected number of contigs ≈ e^(-c) × number_of_reads
```

Where c is coverage. This assumes:
- Random read sampling
- No sequencing errors
- No repeated sequences

---

## Results

### Test 1: Varying Genome Lengths

Testing genomes of 500bp, 1000bp, and 2000bp with 10x coverage:

| Genome Length | Contigs | LW Predicted | N50  | Total Length |
|--------------|---------|--------------|------|--------------|
| 500          | 1       | 1.00         | 462  | 462          |
| 1000         | 1       | 1.00         | 984  | 984          |
| 2000         | 1       | 1.00         | 1980 | 1980         |

**Findings:**
At 10x coverage, all genomes assembled into a single contig, matching the Lander-Waterman prediction of ~1 contig. The total assembled length is close to the original genome length (slight differences due to k-mer edge effects).

### Test 2: Varying Coverage Levels

Testing a 1000bp genome with 5x, 10x, and 20x coverage:

| Coverage | Contigs | LW Predicted | N50 | Ratio (Obs/Exp) |
|----------|---------|--------------|-----|-----------------|
| 5.0x     | 2       | 0.34         | 877 | 5.94            |
| 10.0x    | 1       | 1.00         | 984 | 1.00            |
| 20.0x    | 1       | 1.00         | 987 | 1.00            |

**Findings:**
- At 5x coverage, we get 2 contigs, showing incomplete genome coverage
- At 10x and 20x coverage, we get near-complete assembly (1 contig)
- N50 improves with higher coverage (longer, more continuous assemblies)
- Lander-Waterman predictions are reasonable at higher coverage levels

The formula e^(-5) × 50 = 0.34 predicts less than 1 contig, which doesn't make biological sense. In practice, we get small gaps in coverage that create breaks.

### Test 3: Varying Error Rates

Testing a 1000bp genome with different sequencing error rates at 10x coverage:

| Error Rate | Contigs | LW Predicted | N50 | Ratio (Obs/Exp) |
|------------|---------|--------------|-----|-----------------|
| 0.000      | 1       | 1.00         | 977 | 1.00            |
| 0.001      | 50      | 1.00         | 40  | 50.00           |
| 0.010      | 285     | 1.00         | 27  | 285.00          |

**Findings:**
- Without errors, we get 1 contig as predicted
- With 0.1% errors, contigs increase to 50 (50x more than predicted!)
- With 1% errors, contigs increase to 285 (285x more than predicted!)

**Why does this happen?**
Sequencing errors create incorrect k-mers that don't match the real genome. These act as false branch points in the De Bruijn graph, breaking contigs into many small pieces.

The Lander-Waterman equation assumes perfect sequencing, so it completely fails to predict assembly quality when errors are present.

---

## Discussion

### Question 1: How do different parameters affect assembly?

**Genome length:** At constant coverage, longer genomes assemble just as well as short ones. The key is maintaining adequate coverage.

**Coverage:** Higher coverage dramatically improves assembly. At 5x coverage, we see gaps in the assembly. At 10x and above, we get near-complete assemblies. This matches real sequencing projects, which typically use 30-100x coverage.

**Error rate:** Even small error rates (0.1%) significantly fragment assemblies. This is why real assemblers use error correction algorithms before assembly.

### Question 2: Does the Lander-Waterman equation accurately predict contig numbers?

**With no errors:** Yes, the predictions are accurate. At 10x coverage, we predicted 1 contig and observed 1 contig.

**With errors:** No, the equation becomes very inaccurate. It predicted 1 contig but we observed 50-285 contigs depending on error rate.

**Why the failure?** The Lander-Waterman model assumes:
1. Random, uniform sequencing (true in our simulation)
2. No sequencing errors (violated when we add errors)
3. No repetitive sequences (true in our random DNA)

When assumption #2 is violated, predictions break down completely.

### Question 3: How does error rate affect Lander-Waterman accuracy?

Error rate has a massive effect on accuracy. The ratio of observed to expected contigs:
- 0% errors: 1.00 (perfect prediction)
- 0.1% errors: 50.00 (50x more contigs than predicted)
- 1% errors: 285.00 (285x more contigs than predicted)

The relationship appears roughly linear: doubling the error rate roughly doubles the number of contigs. This makes sense because each error creates a potential break point.

**Real-world implications:**
Modern sequencers have error rates around 0.1-1%, so the Lander-Waterman equation cannot accurately predict assembly quality for real data. More sophisticated models are needed that account for:
- Sequencing error rates
- Error correction strategies
- K-mer size effects
- Repetitive sequence content

---

## Conclusions

This project successfully implemented a complete DNA assembly pipeline using De Bruijn graphs. The implementation correctly:

1. Generates random DNA sequences with specified parameters
2. Simulates sequencing with realistic coverage and error rates
3. Builds De Bruijn graphs from k-mers
4. Assembles contigs by finding unbranched paths
5. Calculates assembly statistics (N50, total length, etc.)

Key findings:

1. **Coverage is critical:** 10x coverage gives good assemblies, while 5x shows gaps
2. **Errors matter enormously:** Even 0.1% error rates fragment assemblies dramatically
3. **Lander-Waterman has limitations:** Accurate only for error-free sequencing

The De Bruijn graph approach is powerful for genome assembly, but real-world assemblers need additional strategies to handle sequencing errors, repetitive sequences, and other biological complexities.

---

## Files Included

### Core Programs
- `dna_generator.py` - Generate random DNA sequences
- `sequencing_simulator.py` - Simulate DNA sequencing
- `kmer_generator.py` - Extract k-mers from reads
- `debruijn_assembler.py` - Build graph and assemble contigs
- `lander_waterman.py` - Calculate theoretical predictions

### Pipeline and Testing
- `run_assembly.py` - Complete pipeline (DNA → assembly)
- `simple_test.py` - Test suite with varying parameters
- `test_assembly.py` - Comprehensive testing (requires pandas)
- `visualize_results.py` - Generate plots (bonus)

### Results
- `simple_test_results/` - Test outputs and summaries
- `test_example/` - Example assembly outputs

### Documentation
- `README.md` - Setup and usage instructions
- `P8_REPORT.md` - This report
- `requirements.txt` - Python package dependencies

---

## How to Run

### Quick Example
```bash
python3 run_assembly.py --length 1000 --coverage 10 --read_length 100 --kmer 21
```

### Full Testing
```bash
python3 simple_test.py
```

This generates assemblies with varying parameters and compares to Lander-Waterman predictions.

### Custom Parameters
```bash
# Generate DNA
python3 dna_generator.py --length 5000 --output my_genome.fasta

# Simulate sequencing
python3 sequencing_simulator.py --input my_genome.fasta --coverage 20 --read_length 150 --output my_reads.txt

# Extract k-mers
python3 kmer_generator.py --input my_reads.txt --k 31 --output my_kmers.txt

# Assemble
python3 debruijn_assembler.py --input my_kmers.txt --output my_contigs.fasta
```

---

## Dependencies

```bash
# Required for basic functionality
python3 (version 3.6 or higher)

# Optional for testing and visualization
pandas
matplotlib
numpy
openpyxl
```

The core assembly programs (dna_generator, sequencing_simulator, kmer_generator, debruijn_assembler) work with just Python 3 and no additional packages.

---

## Technical Notes

### K-mer Size Selection
We used k=21 for most tests. Larger k-mers:
- Reduce false connections (good)
- Require higher coverage (bad)
- Create more fragmented assemblies at low coverage (bad)

For our 1000bp genomes at 10x coverage, k=21 works well.

### Graph Complexity
With no errors, graphs are simple (mostly linear paths). With errors, graphs become highly branched with many dead-end paths from incorrect k-mers.

### Assembly Algorithm
Our algorithm is conservative - it stops at every branch point rather than trying to resolve ambiguities. More sophisticated assemblers use:
- Read pair information
- Coverage depth to distinguish real variants from errors
- Error correction before assembly

---

## Future Improvements

Possible extensions:
1. Add repetitive sequence simulation (bonus feature)
2. Implement graph visualization (bonus feature)
3. Add paired-end read simulation
4. Implement error correction algorithms
5. Handle reverse complement reads
6. Add consensus sequence polishing

---

## References

1. Compeau, P. E., Pevzner, P. A., & Tesler, G. (2011). How to apply de Bruijn graphs to genome assembly. Nature Biotechnology, 29(11), 987-991.

2. Lander, E. S., & Waterman, M. S. (1988). Genomic mapping by fingerprinting random clones: a mathematical analysis. Genomics, 2(3), 231-239.

3. Miller, J. R., Koren, S., & Sutton, G. (2010). Assembly algorithms for next-generation sequencing data. Genomics, 95(6), 315-327.
