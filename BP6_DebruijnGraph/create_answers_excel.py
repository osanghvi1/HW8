#!/usr/bin/env python3
"""
Create an Excel version of the answers
"""
import pandas as pd

# Create a summary sheet
summary_data = {
    'Question': [
        'What is the famous quote?',
        'Number of contigs',
        'Total assembly length',
        'N50',
        'Longest contig',
        'Shortest contig',
        'Total unique 5-mers',
        'Total k-mer observations',
        'Average coverage',
        'Graph nodes (4-mers)',
        'Graph edges (5-mers)',
        'Start tips',
        'End tips',
        'Branch points (out)',
        'Merge points (in)'
    ],
    'Answer': [
        'All That Is Gold Does Not Glitter (Tolkien, LOTR)',
        17,
        275,
        21,
        49,
        5,
        207,
        1456,
        '7.03x',
        200,
        207,
        1,
        1,
        8,
        6
    ]
}

summary_df = pd.DataFrame(summary_data)

# Create the quote text
quote_text = """All that is gold does not glitter,
Not all those who wander are lost;
The old that is strong does not wither,
Deep roots are not reached by the frost.

From the ashes a fire shall be woken,
A light from the shadows shall spring;
Renewed shall be blade that was broken,
The crownless again shall be king."""

quote_data = {
    'The Famous Quote': [line for line in quote_text.split('\n')],
}

quote_df = pd.DataFrame(quote_data)

# Load contigs for reference
contigs_df = pd.read_excel('contigs.xlsx')

# Save to Excel with multiple sheets
with pd.ExcelWriter('BP6_ANSWERS.xlsx', engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    quote_df.to_excel(writer, sheet_name='The Quote', index=False)
    contigs_df.to_excel(writer, sheet_name='Contigs', index=False)

print("Created BP6_ANSWERS.xlsx with 3 sheets:")
print("  1. Summary - Key statistics and answers")
print("  2. The Quote - The famous quote identified")
print("  3. Contigs - All assembled contigs")
