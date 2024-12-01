import csv
import os
from collections import defaultdict

def build_inverted_index(forward_index_file, output_file):
    """
    Reads the forward index and builds an inverted index mapping word and lemma IDs to document IDs.
    """
    inverted_index = defaultdict(lambda: {'DocumentIDForWords': set(), 'DocumentIDForLemmas': set()})

    if not os.path.isfile(forward_index_file) or os.path.getsize(forward_index_file) == 0:
        raise FileNotFoundError(f"Input file '{forward_index_file}' does not exist or is empty.")

    # Read the forward index file
    with open(forward_index_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            doc_id = row['Document ID']
            word_ids = row['Word IDs'].split()
            lemma_ids = row['Lemma IDs'].split()

            for word_id in word_ids:
                inverted_index[word_id]['DocumentIDForWords'].add(doc_id)
            for lemma_id in lemma_ids:
                inverted_index[lemma_id]['DocumentIDForLemmas'].add(doc_id)

    if os.path.exists(output_file):
        overwrite = input(f"File '{output_file}' already exists. Overwrite? (y/n): ").strip().lower()
    if overwrite != 'y':
        print("Operation cancelled.")
        return
    
    elif not os.path.exists(output_file):
        open(output_file, 'w').close()

    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID Type', 'ID', 'Document IDs'])

        for id_value, id_type_dict in inverted_index.items():
            if id_type_dict['DocumentIDForWords']:
                writer.writerow(['WordID', id_value, ' '.join(sorted(id_type_dict['DocumentIDForWords']))])
            if id_type_dict['DocumentIDForLemmas']:
                writer.writerow(['LemmaID', id_value, ' '.join(sorted(id_type_dict['DocumentIDForLemmas']))])

# File paths
forward_index_file = 'forward_index.csv'
output_csv = 'inverted_index.csv'

# Build and save the inverted index
build_inverted_index(forward_index_file, output_csv)

print(f"Inverted index stored at {output_csv}")
