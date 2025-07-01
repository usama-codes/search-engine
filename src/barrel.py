import csv
from pathlib import Path

# Constants
num_barrels = 50
chunk_size = 11200
csv.field_size_limit(10**7)

# Set base directory relative to script location
BASE_DIR = Path(__file__).resolve().parent
engine_data_dir = BASE_DIR.parent / "engine_data"
barrels_dir = engine_data_dir / "barrels"
csv_file_path = engine_data_dir / "inverted_index.csv"

# Create barrel directory if it doesn't exist
barrels_dir.mkdir(parents=True, exist_ok=True)

# Initialize empty barrels
barrels = {i: [] for i in range(num_barrels)}

# Read CSV
with csv_file_path.open('r', newline='') as f:
    reader = csv.reader(f)
    next(f)  # Skip header
    for row in reader:
        word_id = int(row[0])
        doc_info = row[1]
        barrel_index = word_id % num_barrels
        barrels[barrel_index].append((word_id, doc_info))

# Write each barrel to a file, chunking if needed
for barrel_index, data in barrels.items():
    chunk_id = 0
    row_count = 0
    barrel_filename = barrels_dir / f"barrel_{barrel_index}_chunk{chunk_id}.csv"
    f = barrel_filename.open('w', newline='')
    f.write("Word ID, Doc ID : Bit Array\n")

    for word_id, doc_info in data:
        f.write(f"{word_id},{doc_info}\n")
        row_count += 1

        if row_count >= chunk_size:
            f.close()
            chunk_id += 1
            row_count = 0
            barrel_filename = barrels_dir / f"barrel_{barrel_index}_chunk{chunk_id}.csv"
            f = barrel_filename.open('w', newline='')
            f.write("Word ID, Doc ID : Bit Array\n")

    f.close()

print("Barrels have been created and written to files.")
