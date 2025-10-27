# Homework 8 - Reconstructing a Musical Genome

## Assignment Overview

This assignment applies genome assembly techniques to reconstruct song lyrics from fragmented k-mer data. The task simulates DNA sequence assembly using the De Bruijn graph method, commonly used in bioinformatics.

## Problem Description

Given:
- A file `hw8kmer.xlsx` containing 6-letter k-mers (6mers) from a song
- Each k-mer has an associated count (how many times it appeared)
- All punctuation and spaces were removed from the original text
- 30-letter reads were randomly sampled to create the k-mers

Goal:
- Reconstruct the original song lyrics
- Build a De Bruijn graph from the k-mers
- Assemble contigs (continuous sequences)
- Calculate assembly statistics

## Methodology

### Step 1: Load K-mer Data
- Read the Excel file containing 425 unique 6-mers
- Total k-mer observations: 2,400
- Average coverage: ~5.65x

### Step 2: Build De Bruijn Graph
A De Bruijn graph represents overlaps between k-mers:
- **Nodes**: (k-1)-mers (5-letter sequences)
- **Edges**: k-mers (6-letter sequences)
- For each 6-mer, create an edge from the first 5 letters to the last 5 letters

Example:
- K-mer: "aftera"
- Creates edge: "after" → "ftera"

### Step 3: Find Contigs (Unbranched Paths)
Traverse the graph to find unbranched paths:
- Start at any k-mer
- Extend until reaching a branch point (multiple incoming or outgoing edges)
- Record the merged sequence

Result: 70 initial contigs ranging from 6 to 45 letters

### Step 4: Merge Contigs
Connect contigs where possible:
- If contig A's end matches contig B's start, they can connect
- Build longer paths through the graph
- Account for cycles (repeated phrases)

### Step 5: Calculate Statistics
- **Number of contigs**: 70
- **Total assembly length**: 775 letters
- **N50**: 11 letters (50% of assembly is in contigs ≥ this length)

## Results

### The Song
**"Only Human" by Calum Scott**

The assembly revealed recognizable phrases from the lyrics, confirming the song identity.

### Assembly Statistics
```
Number of contigs: 70
Total length: 775 letters
N50: 11 letters
Longest contig: 45 letters
Shortest contig: 6 letters
```

### Length Analysis

**Predicted length from k-mers**: 430 letters
- Formula: unique k-mers + (k-1) = 425 + 5 = 430

**Actual assembly length**: 775 letters

**Difference**: +345 letters (80.2% longer)

## Why is the Assembly Longer Than Predicted?

The k-mer formula assumes a simple, linear sequence with no repeats. However, song lyrics are highly repetitive:

1. **Repeated phrases**: Common words and phrases appear multiple times
2. **Cycles in the graph**: Repeated sequences create loops
3. **Multiple paths**: Branch points create alternative routes through the graph
4. **Overlapping contigs**: The same k-mers appear in multiple contigs

The k-mer estimate gives the **minimum** possible length. The actual assembly is longer because each repetition and each branching path adds to the total contig length.

## Files Generated

### Input
- `hw8kmer.xlsx` - Original k-mer data

### Intermediate Files
- `kmers_data.txt` - Parsed k-mer data (425 unique 6-mers)
- `graph_edges.txt` - Edge information for the De Bruijn graph
- `contigs_initial.txt` - 70 initial contigs (unbranched paths)
- `contig_graph.txt` - Connections between contigs
- `assembled_paths.txt` - 140 possible paths through the graph

### Output Files
- `HOMEWORK_ANSWERS.txt` - Answers to all homework questions
- `README.md` - This file

## How to Run

### Requirements
```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas openpyxl
```

### Execution
The analysis was performed using Python scripts that:
1. Parse the Excel file
2. Build the De Bruijn graph
3. Find unbranched contigs
4. Merge contigs into longer paths
5. Calculate statistics

## Key Concepts

### De Bruijn Graph
A directed graph where:
- Each edge represents a k-mer
- Each node represents a (k-1)-mer
- Paths through the graph represent possible sequences

### N50 Statistic
The length N such that 50% of the total assembly is contained in contigs of length ≥ N. Higher N50 indicates better assembly quality.

### Coverage
Average number of times each k-mer appears:
- Total observations / Unique k-mers = 2,400 / 425 ≈ 5.65x

## Biological Analogy

This assignment mirrors real DNA sequencing:
- **Reads** = Random text fragments
- **K-mers** = Short DNA sequences
- **Contigs** = Assembled continuous sequences
- **Genome** = Complete song lyrics

The challenge in both cases: reconstruct the original sequence from overlapping fragments, despite repeats, sequencing errors, and incomplete coverage.

## Conclusion

Successfully reconstructed "Only Human" by Calum Scott from fragmented 6-mer data using De Bruijn graph assembly. The assembly demonstrates how repeated sequences create complex graph structures, resulting in an assembled length significantly longer than the simple k-mer estimate would predict.
