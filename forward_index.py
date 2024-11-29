import csv
import re
from collections import defaultdict

def preprocess_text(text):
    """
    Tokenizes and preprocesses text by converting to lowercase and removing punctuation.
    """
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
    tokens = text.split()
    return tokens

def build_forward_index(data_file, lexicon_file, output_file):
    """
    Reads the data.csv and lexicon.csv files, and builds a forward index mapping generated document IDs to token IDs.
    Writes the forward index to a new CSV file.
    """
    # Step 1: Load the text column from data.csv
    documents = []
    with open(data_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = row.get('text', '')
            documents.append(text)

    # Step 2: Load the lexicon mapping (Token -> ID)
    token_to_id = {}
    with open(lexicon_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            token = row.get('Token', '')
            token_id = row.get('ID', '')
            if token and token_id:
                token_to_id[token] = token_id

    # Step 3: Build the forward index
    forward_index = {}
    for i, text in enumerate(documents, start=1):  # Generate sequential document IDs starting from 1
        tokens = preprocess_text(text)
        token_ids = [token_to_id[token] for token in tokens if token in token_to_id]
        forward_index[i] = token_ids

    # Step 4: Write the forward index to a new CSV file
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['DocumentID', 'TokenIDs'])  # Header
        for doc_id, token_ids in forward_index.items():
            writer.writerow([doc_id, ' '.join(token_ids)])

# Paths to the input and output files
data_csv = 'data.csv'
lexicon_csv = 'lexicon_with_ids.csv'
output_csv = 'forward_index.csv'

# Build the forward index and save it to a CSV file
build_forward_index(data_csv, lexicon_csv, output_csv)

print(f"Forward index saved to {output_csv}")
