import csv
import os
from collections import defaultdict

def build_inverted_index(forward_index_file, output_file):
    """
    Reads the forward index and builds an inverted index mapping word and lemma IDs to document IDs.
    """
    inverted_index = defaultdict(lambda: {'wordIDs': set(), 'LemmaIDs': set()})

    # Read the forward index file
    with open(forward_index_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            doc_id = row['DocumentID']
            word_ids = row['wordIDs'].split()
            lemma_ids = row['LemmaIDs'].split()

            for word_id in word_ids:
                inverted_index[word_id]['wordIDs'].add(doc_id)
            for lemma_id in lemma_ids:
                inverted_index[lemma_id]['LemmaIDs'].add(doc_id)

    # Ensure file creation if it doesn't exist
    if not os.path.exists(output_file):
        open(output_file, 'w').close()  # Creates an empty file

    # Save the inverted index to the output file
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID Type', 'ID', 'DocumentIDs'])

        for id_value, id_type_dict in inverted_index.items():
            if id_type_dict['wordIDs']:
                writer.writerow(['WordID', id_value, ' '.join(sorted(id_type_dict['wordIDs']))])
            if id_type_dict['LemmaIDs']:
                writer.writerow(['LemmaID', id_value, ' '.join(sorted(id_type_dict['LemmaIDs']))])

# File paths
forward_index_file = 'forward_index.csv'
output_csv = 'inverted_index.csv'

# Build and save the inverted index
build_inverted_index(forward_index_file, output_csv)

print(f"Inverted index stored at {output_csv}")
