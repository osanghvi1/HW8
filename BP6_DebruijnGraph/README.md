# BP6 - De Bruijn Graph Assembly

## What This Project Does

This project reconstructs a famous quote from fragmented pieces (k-mers) using a De Bruijn graph - a common method used in DNA sequence assembly.

## The Problem

I was given:
- 207 different 5-letter pieces (k-mers) from a famous quote
- Each piece had a count showing how many times it appeared
- All spaces and punctuation were removed from the original
- The pieces came from 30-letter "reads" sampled about 7 times each
- No errors in the data

My task:
- Rebuild the original quote
- Create a De Bruijn graph from the pieces
- Assemble contigs (longer sequences)
- Calculate quality statistics (N50)

## How I Solved It

### Step 1: Collected the Data

Started with 207 unique 5-mers from the problem:
- Total pieces: 207 unique 5-mers
- Total observations: 1,456 times
- Average coverage: 7.03x (each piece appears ~7 times)

### Step 2: Built the De Bruijn Graph

The graph shows how pieces connect:
- **Nodes**: 4-letter sequences (200 total)
- **Edges**: 5-letter k-mers (207 total)
- Each 5-mer connects its first 4 letters to its last 4 letters

**Simple example:**
- K-mer: "afire"
- Creates connection: "afir" → "fire"

**My graph had:**
- 1 starting point, 1 ending point
- 8 branch points (where paths split)
- 6 merge points (where paths join)

### Step 3: Found Contigs

I walked through the graph finding continuous paths:
- Started at tips or branch points
- Followed the path until hitting another branch
- Saved each continuous sequence

**Result:** 17 contigs from 5 to 49 letters long

### Step 4: Calculated Statistics

- **Number of contigs**: 17
- **Total length**: 275 letters
- **N50**: 21 letters
  - This means half the assembly is in pieces ≥ 21 letters
- **Longest piece**: 49 letters
- **Shortest piece**: 5 letters

### Step 5: Identified the Quote

Looking at the contigs, I recognized the quote:

**"All That Is Gold Does Not Glitter"**

_The Riddle of Strider from J.R.R. Tolkien's "The Lord of the Rings"_

Full text:
```
All that is gold does not glitter,
Not all those who wander are lost;
The old that is strong does not wither,
Deep roots are not reached by the frost.

From the ashes a fire shall be woken,
A light from the shadows shall spring;
Renewed shall be blade that was broken,
The crownless again shall be king.
```

This poem appears in "The Fellowship of the Ring" (Book I, Chapter 10: "Strider") and describes Aragorn, the ranger who is the rightful king of Gondor.

## Results

### The Quote I Found

The five longest pieces gave it away:

1. `snotwitherdeeprootsarenotreachedbythefrostfromthe` (49 letters)
2. `snotglitternotallthosewhowanderarelosttheoldthat` (48 letters)
3. `hallspringrenewedshal` (21 letters)
4. `okenthecrownlessagain` (21 letters)
5. `atisstrongdoesnot` (17 letters)

These clearly come from "All That Is Gold Does Not Glitter" - the famous Tolkien poem about Aragorn.

### Assembly Quality

| What I Measured | Result |
|----------------|---------|
| Total contigs | 17 |
| Total length | 275 letters |
| N50 | 21 letters |
| Longest piece | 49 letters |
| Shortest piece | 5 letters |

## Files Included

### Main Deliverables (what gets graded)
- **debruijn_graph_complete.xlsx** - The complete graph showing all nodes and connections
- **contigs.xlsx** - All 17 assembled contigs with details
- **BP6_ANSWERS.txt** - Written answers to all questions
- **BP6_ANSWERS.xlsx** - Excel version of answers with summary
- **README.md** - This file explaining everything

### Supporting Files
- `kmer_edges.xlsx` - All the k-mer connections
- `graph_nodes.xlsx` - Information about each node
- `contigs_sequences.txt` - Easy-to-read contig list
- `quote_identified.txt` - The identified quote

### Python Scripts (how I built everything)
- `build_debruijn_graph.py` - Builds the graph
- `find_contigs.py` - Finds continuous paths
- `create_complete_graph.py` - Makes the final Excel file
- `identify_quote.py` - Identifies the quote

## Why Did I Get 17 Pieces Instead of 1?

The quote is continuous, but I got 17 separate contigs because:

1. **Repeated words** - Words like "shall" and "that" appear multiple times, creating forks in the path where I couldn't tell which way to go

2. **Conservative approach** - I stopped at each fork rather than guessing, to avoid mistakes

3. **This mirrors real DNA assembly** - Repeated sequences in genomes cause the same problem

### What Does N50 = 21 Mean?

- Half my assembly is in pieces of 21 letters or longer
- Shows moderate quality (perfect would be N50 = 275)
- The two big pieces (49 and 48 letters) contain most of the quote

### Connection to Biology

This is exactly how DNA sequencing works:
- Short DNA reads → my 30-letter fragments
- K-mers → 5-letter overlaps
- Contigs → assembled pieces
- Repeated DNA → repeated words causing breaks

In real sequencing, we'd solve this with:
- Longer reads that span repeats
- Higher coverage (more copies of each piece)
- Paired-end reads that show which pieces connect

## Key Terms Explained

**De Bruijn Graph** - A way to show how pieces connect. Each k-mer is an edge, each (k-1)-mer is a node. Walking through the graph rebuilds the sequence.

**N50** - The length where half your assembly is in pieces that big or bigger. Higher = better quality.

**Coverage** - How many times each piece appears on average (mine was 7x). More coverage = easier to assemble correctly.

**Contig** - A continuous assembled sequence. I got 17 of them.

## Summary

I successfully reconstructed Tolkien's "All That Is Gold Does Not Glitter" poem from 207 small pieces using De Bruijn graph assembly. The final assembly had 17 contigs with an N50 of 21 letters.

This shows both the power of graph-based assembly (I got the quote!) and its limitations (broken into 17 pieces due to repeated words). The same challenges exist in real DNA sequencing where repeated sequences make assembly difficult.
