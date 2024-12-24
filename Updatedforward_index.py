import csv
import re

# --- File Reading Utilities ---
def load_documents(data_file):
    """
    Reads the data file and returns a list of documents.
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
    Loads the lexicon file and returns a dictionary mapping words to word IDs (lemma IDs).
    """
    lexicon = {}
    with open(lexicon_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            word = row.get('Word', '')
            word_id = row.get('Word ID', '')
            if word and word_id:
                lexicon[word] = int(word_id)  # Store word and corresponding lemma ID (word ID)
    return lexicon

# --- Document Processing Utilities ---
def process_document(doc, lexicon):
    """
    Process a single document to generate the word IDs directly from the lexicon.
    """
    document_id, text, title, tags = doc
    words_in_title = set(title.lower().split())
    words_in_tags = set(tags.lower().split())
    
    # Tokenize the text and normalize to lowercase
    text_words = re.findall(r'\w+', text.lower())
    
    word_info = []
    
    # Process each word and get the word ID (lemma ID) from the lexicon
    for word in text_words:
        word_id = lexicon.get(word)  # Directly use the lemma ID from the lexicon
        if word_id is not None:
            # Title and tag presence (1 or 0)
            title_presence = 1 if word in words_in_title else 0
            tag_presence = 1 if word in words_in_tags else 0
            
            # Create the 10-bit array:
            # 1st bit = Title presence (1 or 0)
            # 2nd bit = Tag presence (1 or 0)
            # 8 bits for frequency (0-255, but we don't need frequency here, just presence)
            bit_array = (title_presence << 9) | (tag_presence << 8)
            
            # Append word_id, bit_array, and lemma_id (which is the same as word_id)
            word_info.append((word_id, bit_array, word_id))  # word_id as lemma_id
    
    return document_id, word_info

# --- Data Processing ---
def process_data(documents, lexicon):
    """
    Process the data to create the forward index with word ID, bit arrays, and lemma IDs.
    """
    output_data = []
    
    # Process each document
    for doc in documents:
        document_id, word_info = process_document(doc, lexicon)
        
        # Collect the output: document ID + word_id + bit_array + lemma_id
        output_line = [str(document_id)] + [f"{word_id}:{bit_array}:{lemma_id}" for word_id, bit_array, lemma_id in word_info]
        output_data.append(output_line)
    
    return output_data

# --- File Saving ---
def save_output_csv(output_file, output_data):
    """
    Save the processed output to a CSV file with columns: document_id, word_id, bit_array, lemma_id.
    """
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Document ID', 'Word ID', 'Bit Array', 'Lemma ID'])  # CSV header
        for line in output_data:
            writer.writerow(line)

# --- Main Function ---
def main(data_file, lexicon_file, output_file):
    """
    Main function to process documents and save the forward index with word ID, bit array, and lemma ID to a CSV file.
    """
    # Load documents and lexicon
    documents, document_titles, document_tags = load_documents(data_file)
    lexicon = load_lexicon(lexicon_file)
    
    # Combine documents, titles, and tags into a single list for processing
    combined_documents = list(zip(range(1, len(documents) + 1), documents, document_titles, document_tags))
    
    # Process the documents to generate word ID, bit array, and lemma ID
    total_documents = len(combined_documents)
    output_data = []
    
    for idx, doc in enumerate(combined_documents, start=1):
        document_id, word_info = process_document(doc, lexicon)
        
        # Collect the output: document ID + word_id + bit_array + lemma_id
        output_line = [str(document_id)] + [f"{word_id}:{bit_array}:{lemma_id}" for word_id, bit_array, lemma_id in word_info]
        output_data.append(output_line)
        
        # Display progress (show the current document number out of the total)
        if idx % (total_documents // 10) == 0 or idx == total_documents:
            print(f"Processing... {idx}/{total_documents} documents processed")
    
    # Save the output to a CSV file
    save_output_csv(output_file, output_data)
    print(f"Processed data saved to {output_file}")

# --- Script Execution ---
if __name__ == "__main__":
    # Paths of input/output files
    data_file = 'data.csv'  # File containing document data (text, title, tags)
    lexicon_file = 'lexicon.csv'  # File containing lexicon (word, word_id)
    output_file = 'forward.csv'    # File to save the results

    # Run the main function
    main(data_file, lexicon_file, output_file)
