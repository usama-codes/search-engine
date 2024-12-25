import csv
import os
from collections import defaultdict

def build_inverted_index(forward_index_file, output_file):
    """
    Reads the forward index and builds an inverted index mapping word and lemma IDs to document IDs.
    """
    inverted_index = defaultdict(lambda: {'DocumentIDForWords': {}, 'DocumentIDForLemmas': {}})

    if not os.path.isfile(forward_index_file) or os.path.getsize(forward_index_file) == 0:
        raise FileNotFoundError(f"Input file '{forward_index_file}' does not exist or is empty.")

    # Read the forward index file
    with open(forward_index_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        for row in reader:
            if len(row) < 2:
                continue
                
            doc_id = row[0]
            # Process each word:lemma:bit_array combination
            for item in row[1:]:
                word_id, lemma_id, bit_array = item.split(':')
                # Store doc_id with its bit_array
                inverted_index[word_id]['DocumentIDForWords'][doc_id] = bit_array
                inverted_index[lemma_id]['DocumentIDForLemmas'][doc_id] = bit_array

    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID Type', 'ID', 'Document IDs and Bit Arrays'])

        for id_value, id_type_dict in inverted_index.items():
            if id_type_dict['DocumentIDForWords']:
                doc_bits = ' '.join(f"{doc}:{bits}" for doc, bits in id_type_dict['DocumentIDForWords'].items())
                writer.writerow(['WordID', id_value, doc_bits])
            if id_type_dict['DocumentIDForLemmas']:
                doc_bits = ' '.join(f"{doc}:{bits}" for doc, bits in id_type_dict['DocumentIDForLemmas'].items())
                writer.writerow(['LemmaID', id_value, doc_bits])

# File paths
forward_index_file = 'forward_index.csv'  # Changed to match forward index output
output_csv = 'inverted_index.csv'

# Build and save the inverted index
build_inverted_index(forward_index_file, output_csv)

print(f"Inverted index stored at {output_csv}")