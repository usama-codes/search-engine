import csv
import re


# --- Preprocessing Utilities ---
def preprocess_text(text):
    """
    Tokenizes and preprocesses text.
    """
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
    return text.split()

# --- File Reading Utilities ---
def load_documents(data_file):
    """
    Reads the data file and returns two lists: documents and document titles.
    """
    documents = []
    document_titles = []
    document_tags = []
    with open(data_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            documents.append(row.get('text', ''))
            document_tags.append(row.get('tags', ''))
            document_titles.append(row.get('title', ''))
    return documents, document_titles, document_tags

def load_lexicon(lexicon_file):
    """
    Loads the lexicon file and returns dictionaries for word-to-ID and lemma-to-ID mappings.
    """
    word_to_id = {}
    lemma_to_id = {}
    with open(lexicon_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            word = row.get('Word', '')
            word_id = row.get('Word ID', '')
            lemma_id = row.get('Lemma ID', '')
            if word and word_id and lemma_id:
                word_to_id[word] = word_id
                lemma_to_id[word] = lemma_id
    return word_to_id, lemma_to_id

# --- Index Building Utilities ---
def build_forward_index(documents, document_titles, document_tags, word_to_id, lemma_to_id):
    """
    Builds the forward index mapping document IDs to word IDs, lemma IDs, and title word IDs.
    """
    forward_index = {}

    # Build word and lemma IDs for documents
    for doc_id, text in enumerate(documents, start=1):  # Start document IDs from 1
        words = preprocess_text(text)
        word_ids = [word_to_id[word] for word in words if word in word_to_id]
        lemma_ids = [lemma_to_id[word] for word in words if word in lemma_to_id]
        forward_index[doc_id] = {'Word IDs': word_ids, 'Lemma IDs': lemma_ids}

    # Add title word IDs
    for doc_id, title in enumerate(document_titles, start=1):
        title_words = preprocess_text(title)
        title_ids = [word_to_id[word] for word in title_words if word in word_to_id]
        if doc_id in forward_index:
            forward_index[doc_id]['Title Word IDs'] = title_ids

    for doc_id, tags in enumerate(document_tags, start=1):
        tag_words = preprocess_text(tags)
        tag_ids = [word_to_id[word] for word in tag_words if word in word_to_id]
        if doc_id in forward_index:
            forward_index[doc_id]['Tag Word IDs'] = tag_ids

    return forward_index


# --- File Writing Utilities ---
def save_forward_index(forward_index, output_file):
    """
    Saves the forward index to a CSV file.
    """
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Document ID', 'Word IDs', 'Lemma IDs', 'Title Word IDs', 'Tag Word IDs'])
        for doc_id, ids in forward_index.items():
            writer.writerow([
                doc_id,
                ' '.join(ids['Word IDs']),
                ' '.join(ids['Lemma IDs']),
                ' '.join(ids.get('Title Word IDs', [])),
                ' '.join(ids.get('Tag Word IDs', []))            
                ])


# --- Main Function ---
def main(data_file, lexicon_file, output_file):
    """
    Main function to build and save the forward index.
    """
    # Load data and lexicon
    documents, document_titles, document_tags = load_documents(data_file)
    word_to_id, lemma_to_id = load_lexicon(lexicon_file)

    # Build forward index
    forward_index = build_forward_index(documents, document_titles, document_tags, word_to_id, lemma_to_id)

    # Save forward index to file
    save_forward_index(forward_index, output_file)
    print(f"Forward index stored at {output_file}")


# --- Script Execution ---
if __name__ == "__main__":
    # Paths of input/output files
    data_csv = 'data.csv'
    lexicon_csv = 'lexicon.csv'
    output_csv = 'forward_index.csv'

    # Run the main function
    main(data_csv, lexicon_csv, output_csv)
