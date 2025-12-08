#!/usr/bin/env python3
"""
Identify the famous quote from the assembled contigs
"""
import pandas as pd

# Read contigs
contigs_df = pd.read_excel('contigs.xlsx')

print("IDENTIFYING THE FAMOUS QUOTE")
print("=" * 70)
print()

# Show all contigs
print("All assembled contigs:")
print()
for _, contig in contigs_df.iterrows():
    print(f"Contig {contig['contig_id']:2d} (length {contig['length']:2d}): {contig['sequence']}")

print()
print("=" * 70)
print()

# Based on the contigs, manually piece together the quote
quote_lines = [
    "all that is gold does not glitter",
    "not all those who wander are lost",
    "the old that is strong does not wither",
    "deep roots are not reached by the frost",
    "from the ashes a fire shall be woken",
    "a light from the shadows shall spring renewed",
    "shall be blade that was broken",
    "the crownless again shall be"
]

# The actual quote (adding spaces back)
full_quote = """All that is gold does not glitter,
Not all those who wander are lost;
The old that is strong does not wither,
Deep roots are not reached by the frost.

From the ashes a fire shall be woken,
A light from the shadows shall spring;
Renewed shall be blade that was broken,
The crownless again shall be king."""

print("IDENTIFIED QUOTE:")
print()
print(full_quote)
print()
print("=" * 70)
print()
print("This is the famous poem about Aragorn from J.R.R. Tolkien's")
print("'The Lord of the Rings: The Fellowship of the Ring'")
print()
print("Often referred to as 'The Riddle of Strider' or 'All That Is Gold'")
print("=" * 70)

# Save the results
with open('quote_identified.txt', 'w') as f:
    f.write("FAMOUS QUOTE IDENTIFIED\n")
    f.write("=" * 70 + "\n\n")
    f.write(full_quote + "\n\n")
    f.write("=" * 70 + "\n")
    f.write("Source: J.R.R. Tolkien, 'The Lord of the Rings'\n")
    f.write("        The Fellowship of the Ring, Book I, Chapter 10\n")
    f.write("        'Strider'\n\n")
    f.write("This poem describes Aragorn, the rightful king of Gondor,\n")
    f.write("who appears as a humble ranger but is destined for greatness.\n")

print("\nSaved: quote_identified.txt")
