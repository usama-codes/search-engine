import csv
import os

# Constants
num_barrels = 50  # Number of barrels
chunk_size = 2333  # Number of rows per barrel

# Create barrel directories if they don't exist
if not os.path.exists('barrels'):
    os.mkdir('barrels')

# Initialize empty barrels as lists
barrels = {i: [] for i in range(num_barrels)}

# Read the inverted index from a CSV file
csv_filename = 'inverted_index.csv'  # Change this to your actual CSV file path
with open(csv_filename, mode='r') as f:
    reader = csv.reader(f)
    next(f)
    for row in reader:
        word_id = int(row[0])  # Assuming the first column is word_id
        doc_info = row[1]  # Assuming the second column is doc_info
        barrel_index = word_id % num_barrels  # Calculate barrel based on word_id % 50
        barrels[barrel_index].append((word_id, doc_info))

# Now, let's write each barrel to a separate file, ensuring we don't exceed chunk_size
for barrel_index, data in barrels.items():
    # Determine file name for each barrel
    barrel_filename = f'barrels/barrel_{barrel_index}.csv'
    
    with open(barrel_filename, 'w') as f:
        count = 0

        f.write("Word ID, Doc ID : Bit Array\n")

        for word_id, doc_info in data:
            f.write(f'{word_id},{doc_info}\n')
            count += 1
            # If the number of rows exceeds the chunk size, create a new file
            if count >= chunk_size:
                f.close()
                count = 0
                # Open a new barrel file for the next chunk
                barrel_filename = f'barrels/barrel_{barrel_index}_chunk_{count//chunk_size}.csv'
                f = open(barrel_filename, 'w')
                f.write(f'{word_id},{doc_info}\n')
        
        # Close the final file
        f.close()

print("Barrels have been created and written to files.")
