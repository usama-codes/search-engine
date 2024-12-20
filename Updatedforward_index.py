import csv
import re
from collections import Counter

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
    Loads the lexicon file and returns a dictionary mapping words to word IDs.
    """
    lexicon = {}
    with open(lexicon_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            word = row.get('Word', '')
            word_id = row.get('Word ID', '')
            if word and word_id:
                lexicon[word] = int(word_id)  # Store word and corresponding ID
    return lexicon

# --- Document Processing Utilities ---
def process_document(doc, lexicon, max_frequency=255):
    """
    Process a single document to generate the word IDs and their bit arrays.
    """
    document_id, text, title, tags = doc
    words_in_title = set(title.lower().split())
    words_in_tags = set(tags.lower().split())
    
    # Tokenize the text and normalize to lowercase
    text_words = re.findall(r'\w+', text.lower())
    
    word_info = []
    word_frequency = {}
    
    # Count the frequency of each word in the document
    for word in text_words:
        if word in lexicon:
            word_frequency[word] = word_frequency.get(word, 0) + 1

    # Process each word's information
    for word, freq in word_frequency.items():
        word_id = lexicon.get(word)
        if word_id is not None:
            # Title and tag presence (1 or 0)
            title_presence = 1 if word in words_in_title else 0
            tag_presence = 1 if word in words_in_tags else 0
            
            # Limit frequency to the max frequency of 255
            frequency = min(freq, max_frequency)
            
            # Create the 10-bit array:
            # 1st bit = Title presence (1 or 0)
            # 2nd bit = Tag presence (1 or 0)
            # 8 bits for frequency (0-255)
            frequency_bits = frequency  # Frequency encoded as an 8-bit number
            bit_array = (title_presence << 9) | (tag_presence << 8) | frequency_bits
            word_info.append((word_id, bit_array))
    
    return document_id, word_info

# --- Data Processing ---
def process_data(documents, lexicon, max_frequency=255):
    """
    Process the data to create the forward index with bit arrays.
    """
    output_data = []
    
    # Process each document
    for doc in documents:
        document_id, word_info = process_document(doc, lexicon, max_frequency)
        
        # Collect the output: document ID + word ID + bit array
        output_line = [str(document_id)] + [f"{word_id}:{bit_array}" for word_id, bit_array in word_info]
        output_data.append(output_line)
    
    return output_data

# --- File Saving ---
def save_output_csv(output_file, output_data):
    """
    Save the processed output to a CSV file with columns: document_id, word_id:bit_array pairs.
    """
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Document ID', 'Word ID:Bit Array'])  # CSV header
        for line in output_data:
            writer.writerow(line)

# --- Main Function ---
def main(data_file, lexicon_file, output_file):
    """
    Main function to process documents and save the forward index with bit encoding to a CSV file.
    """
    # Load documents and lexicon
    documents, document_titles, document_tags = load_documents(data_file)
    lexicon = load_lexicon(lexicon_file)
    
    # Combine documents, titles, and tags into a single list for processing
    combined_documents = list(zip(range(1, len(documents) + 1), documents, document_titles, document_tags))
    
    # Process the documents to generate word IDs and bit arrays
    output_data = process_data(combined_documents, lexicon)
    
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
