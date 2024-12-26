import csv
import os

# Define constants
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
    header = next(reader)  # Skip the header row
    for writer in barrel_writers:
        writer.writerow(header)

# Step 1: Read the inverted index from the CSV file and distribute it into barrels
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        word_id = int(row[0])  # The word_id from the inverted index
        barrel_index = word_id % NUM_BARRELS  # Map word_id to a barrel (modulo NUM_BARRELS)
        barrel_writers[barrel_index].writerow(row)  # Write the row to the corresponding barrel

# Close all barrel files
for f in barrel_files:
    f.close()

print(f"Barrels created and stored in '{BARRELS_DIR}' directory, organized by Word ID.")
