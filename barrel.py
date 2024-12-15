import csv
import os

csv.field_size_limit(10**7)


TOTAL_WORDS = 521891
BARREL_SIZE = 10000
NUM_BARRELS = (TOTAL_WORDS + BARREL_SIZE - 1) // BARREL_SIZE

DATA_FILE = "inverted_index.csv"
BARRELS_DIR = "barrels"

os.makedirs(BARRELS_DIR, exist_ok=True)

# Open barrel files for writing
barrel_files = []
barrel_writers = []
for i in range(NUM_BARRELS):
    f = open(os.path.join(BARRELS_DIR, f"barrel_{i}.csv"), 'w', newline='', encoding='utf-8')
    writer = csv.writer(f)
    barrel_files.append(f)
    barrel_writers.append(writer)

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    # Write headers to each barrel file
    for writer in barrel_writers:
        writer.writerow(header)
    for row in reader:
        id_type = row[0]
        word_id = int(row[1])
        # Determine the barrel index based on word_id
        barrel_index = word_id // BARREL_SIZE
        if barrel_index >= NUM_BARRELS:
            barrel_index = NUM_BARRELS - 1  # Handle edge case
        barrel_writers[barrel_index].writerow(row)

# Close all barrel files
for f in barrel_files:
    f.close()

print(f"Barrels created and stored in '{BARRELS_DIR}' directory.")