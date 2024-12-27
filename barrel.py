import csv
import os

csv.field_size_limit(100000000)

num_barrels = 50  # Number of barrels
chunk_size = 2333  # Number of rows per barrel

if not os.path.exists('barrels'):
    os.mkdir('barrels')

barrels = {i: [] for i in range(num_barrels)}

csv_filename = 'inverted_index.csv'  # Change this to your actual CSV file path
with open(csv_filename, mode='r') as f:
    reader = csv.reader(f)
    next(f)
    next(f)
    for row in reader:
        word_id = int(row[0])  # Assuming the first column is word_id
        doc_info = row[1]  # Assuming the second column is doc_info
        barrel_index = word_id % num_barrels  # Calculate barrel based on word_id % 50
        barrels[barrel_index].append((word_id, doc_info))

for barrel_index, data in barrels.items():
    barrel_filename = f'barrels/barrel_{barrel_index}.csv'
    
    with open(barrel_filename, 'w') as f:
        count = 0

        f.write("Word ID, Doc ID : Bit Array\n")

        for word_id, doc_info in data:
            f.write(f'{word_id},{doc_info}\n')
            count += 1
            if count >= chunk_size:
                f.close()
                count = 0
                barrel_filename = f'barrels/barrel_{barrel_index}_chunk_{count//chunk_size}.csv'
                f = open(barrel_filename, 'w')
                f.write(f'{word_id},{doc_info}\n')
        
        f.close()

print("Barrels have been created and written to files.")
print("Barrels have been created and written to files.")
