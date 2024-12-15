import csv
import os

csv.field_size_limit(10**7)

# Define constants
BARREL_SIZE = 11000  # Number of entries per barrel
NUM_BARRELS = 50  # Total number of barrels
DATA_FILE = "inverted_index.csv"  # Input file containing the inverted index
BARRELS_DIR = "barrels"  # Directory to store barrel files

# Create the barrels directory if it doesn't exist
os.makedirs(BARRELS_DIR, exist_ok=True)

# Initialize barrel files and writers
barrel_files = [open(f"{BARRELS_DIR}/barrel_{i}.csv", 'w', newline='', encoding='utf-8') for i in range(NUM_BARRELS)]
barrel_writers = [csv.writer(f) for f in barrel_files]

# Write headers to each barrel file
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for writer in barrel_writers:
        writer.writerow(header)

# Distribute rows to barrels based on Word ID
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        word_id = int(row[1])  # based on wordID and lemma ID
        barrel_index = word_id % NUM_BARRELS  # Map Word ID/LemmaID to a barrel
        barrel_writers[barrel_index].writerow(row)

# Close all barrel files
for f in barrel_files:
    f.close()

print(f"Barrels created and stored in '{BARRELS_DIR}' directory, organized by Word ID.")
