
import csv
def process_data(data_file, lexicon_file, max_frequency=255):
    """
    Process the data file to create the forward index.
    Returns data formatted for two-column output.
    """
    output_data = []
    
    with open(data_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        
        for document_id, row in enumerate(reader, 1):
            if len(row) >= 3:
                title = row[0].replace(',',' ')
                url = row[2]
                tags = row[5] if len(row) > 5 else ""
                output_line = str(document_id) + '\t' + ''.join(title)+ '\t' + ''.join(url)+ '\t' + ''.join(tags)
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
        writer.writerow(['document_id', 'title', 'url', 'tags'])
        
        for line in output_data:
            # Split the line into document_id and metadata
            parts = line.split('\t')
            if len(parts) > 1:
                doc_id = parts[0]
                title = parts[1]
                url = parts[2]
                tags = parts[3]
                writer.writerow([doc_id, title, url, tags])
        
    print(f"Processed data saved to {output_file}.")


# Example usage:
data_file = 'data.csv'  # File containing document data (title, text, url, authors, timestamp, tags)
lexicon_file = 'lexicon.csv'  # File containing lexicon (word, word_id, Lemma_id)
output_file = 'newdata.csv'    # File to save the results

# Process the data and save the output
output_data = process_data(data_file, lexicon_file)
save_output(output_file, output_data)
