import csv

csv.field_size_limit(1000000000)  # Increase the field size limit for large CSV files
# Step 1: Read the forward index from the CSV file
forward_index = []

# Read the forward_index.csv file
with open('forward_index.csv', 'r') as file:
    reader = csv.reader(file)
    next(file)  # Skip the header row
    for row in reader:
        # Convert each row into a tuple (doc_id, word_metadata)
        doc_id = int(row[0])  # The document ID
        word_metadata = row[1]  # The word metadata string
        forward_index.append((doc_id, word_metadata))

# Step 2: Initialize an empty inverted index
inverted_index = {}

# Step 3: Process each document in the forward index
for doc_id, word_metadata in forward_index:
    # Split word_metadata into individual word_id:lemma_id:bitarray entries
    entries = word_metadata.split()

    # Step 4: Process each word metadata
    for entry in entries:
        word_id, lemma_id, bitarray = entry.split(':')
        
        word_id = int(lemma_id)  # Convert word_id to an integer

        # Step 5: Add doc_id and bitarray to the inverted index for the current word_id
        if word_id not in inverted_index:
            inverted_index[word_id] = []

        inverted_index[word_id].append(f"{doc_id}:{bitarray}")

# Step 6: Write the inverted index to a CSV file
with open('inverted_index.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['word_id', 'doc_info'])
    for word_id, doc_bitarray_pairs in inverted_index.items():
        # Join doc_id:bitarray pairs with a space
        writer.writerow([word_id, ' '.join(doc_bitarray_pairs)])

print("Inverted index created successfully!")
