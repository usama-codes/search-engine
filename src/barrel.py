import csv
import os

# Constants
num_barrels = 50  # Number of barrels
chunk_size = 11200  # Number of rows per barrel
csv.field_size_limit(10**7)

# Create barrel directories if they don't exist
if not os.path.exists('D:/NUST/SEMESTER_3/DSA/End_Project/test/engine_data/barrels'):
    os.mkdir('D:/NUST/SEMESTER_3/DSA/End_Project/test/engine_data/barrels')

# Initialize empty barrels as lists
barrels = {i: [] for i in range(num_barrels)}

# Read the inverted index from a CSV file
csv_filename = 'D:/NUST/SEMESTER_3/DSA/End_Project/test/engine_data/inverted_index.csv'  # Change this to your actual CSV file path
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
    barrel_filename = f'D:/NUST/SEMESTER_3/DSA/End_Project/test/engine_data/barrels/barrel_{barrel_index}.csv'
    
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
                barrel_filename = f'D:/NUST/SEMESTER_3/DSA/End_Project/test/engine_data/barrels/barrel_{barrel_index}chunk{count//chunk_size}.csv'
                f = open(barrel_filename, 'w')
                f.write(f'{word_id},{doc_info}\n')
        
        # Close the final file
        f.close()

print("Barrels have been created and written to files.")