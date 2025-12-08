#!/usr/bin/env python3
"""
Convert text files to Excel format
"""
import pandas as pd
import os

def convert_txt_to_excel(txt_file, excel_file, sep='\t', header=0):
    """Convert a tab-separated text file to Excel"""
    try:
        # Read the text file
        df = pd.read_csv(txt_file, sep=sep, header=header)

        # Remove empty rows at the end
        df = df.dropna(how='all')

        # Write to Excel
        df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"✓ Converted {txt_file} → {excel_file}")
        return True
    except Exception as e:
        print(f"✗ Error converting {txt_file}: {e}")
        return False

def convert_text_document_to_excel(txt_file, excel_file):
    """Convert a text document (not tabular) to Excel with one column"""
    try:
        with open(txt_file, 'r') as f:
            lines = f.readlines()

        # Create a DataFrame with one column
        df = pd.DataFrame({'Content': [line.rstrip('\n') for line in lines]})

        # Write to Excel
        df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"✓ Converted {txt_file} → {excel_file}")
        return True
    except Exception as e:
        print(f"✗ Error converting {txt_file}: {e}")
        return False

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("Converting txt files to Excel format...\n")

    # Define files to convert (tabular data)
    tabular_files = [
        ('kmers_data.txt', 'kmers_data.xlsx'),
        ('graph_edges.txt', 'graph_edges.xlsx'),
        ('contigs_initial.txt', 'contigs_initial.xlsx'),
        ('contig_graph.txt', 'contig_graph.xlsx'),
        ('assembled_paths.txt', 'assembled_paths.xlsx'),
    ]

    # Convert tabular files
    success_count = 0
    for txt_file, excel_file in tabular_files:
        txt_path = os.path.join(script_dir, txt_file)
        excel_path = os.path.join(script_dir, excel_file)

        if os.path.exists(txt_path):
            if convert_txt_to_excel(txt_path, excel_path):
                success_count += 1
        else:
            print(f"✗ File not found: {txt_file}")

    # Convert HOMEWORK_ANSWERS.txt (text document)
    homework_txt = os.path.join(script_dir, 'HOMEWORK_ANSWERS.txt')
    homework_excel = os.path.join(script_dir, 'HOMEWORK_ANSWERS.xlsx')

    if os.path.exists(homework_txt):
        if convert_text_document_to_excel(homework_txt, homework_excel):
            success_count += 1
    else:
        print(f"✗ File not found: HOMEWORK_ANSWERS.txt")

    print(f"\n✓ Successfully converted {success_count}/{len(tabular_files) + 1} files")
    print("\nExcel files created:")
    for _, excel_file in tabular_files:
        print(f"  - {excel_file}")
    print(f"  - HOMEWORK_ANSWERS.xlsx")

if __name__ == "__main__":
    main()
