import re
import csv

def load_lexicon(lexicon_file):
    """
    Load the lexicon file which maps words to word IDs and lexicon IDs.
    """
    lexicon = {}
    with open(lexicon_file, 'r', encoding='utf-8') as f:
        next(f)  # Skip the header if there is one
        for line in f:
            Word, Word_ID, Lemma_id = line.strip().split(',')
            lexicon[Word] = (int(Word_ID), int(Lemma_id))  # Store word_id and Lemma_id as a tuple
    return lexicon

def process_document(doc, lexicon, max_frequency=255):
    """
    Process a single document to generate the word IDs, lexicon IDs, and their bit arrays.
    """
    # Unpack the 6 values in the document (title, text, url, authors, timestamp, tags)
    title, text, tags = doc
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
        word_id, Lemma_id = lexicon.get(word, (None, None))
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
            word_info.append((word_id, Lemma_id, bit_array))
    
    return word_info

def process_data(data_file, lexicon_file, max_frequency=255):
    """
    Process the data file to create the forward index.
    Returns data formatted for two-column output.
    """
    lexicon = load_lexicon(lexicon_file)
    output_data = []
    
    with open(data_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        
        for document_id, row in enumerate(reader, 1):
            if len(row) >= 3:
                title = row[0]
                text = row[1]
                tags = row[5] if len(row) > 5 else ""
                
                reduced_doc = [title, text, tags]
                word_info = process_document(reduced_doc, lexicon, max_frequency)
                
                metadata = [f"{word_id}:{Lemma_id}:{bit_array}" for word_id, Lemma_id, bit_array in word_info]
                output_line = str(document_id) + '\t' + ' '.join(metadata)
                output_data.append(output_line)
            else:
                print(f"Skipping line {document_id} due to insufficient columns.")
    
    return output_data



def save_output(output_file, output_data):
    """
    Save the processed output to a file with 2 columns:
    1. document_id
    2. word_metadata (comma-separated list of word_id:Lemma_id:bit_array)
    """
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['document_id', 'word_metadata'])
        
        for line in output_data:
            # Split the line into document_id and metadata
            parts = line.split('\t')
            if len(parts) > 1:
                doc_id = parts[0]
                # Join all word metadata with commas
                word_metadata = ','.join(parts[1:])
                writer.writerow([doc_id, word_metadata])
        
    print(f"Processed data saved to {output_file}.")


# Example usage:
data_file = 'data.csv'  # File containing document data (title, text, url, authors, timestamp, tags)
lexicon_file = 'lexicon.csv'  # File containing lexicon (word, word_id, Lemma_id)
output_file = 'forward_index.csv'    # File to save the results

# Process the data and save the output
output_data = process_data(data_file, lexicon_file)
save_output(output_file, output_data)