import csv
def process_data(data_file):
    output_data = []
    with open(data_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for document_id, row in enumerate(reader, 1):
            if len(row) >= 3:
                title = row[0]
                url = row[2]
                output_line = str(document_id) + '\t' + ''.join(title)+ '\t' + ''.join(url)
                output_data.append(output_line)
            else:
                print(f"Skipping line {document_id} due to insufficient columns.")
    
    return output_data
def save_output(output_file, output_data):
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(['document_id', 'title','url'])
        
        for line in output_data:
            # Split the line into document_id and metadata
            parts = line.split('\t')
            if len(parts) > 2:
                doc_id = parts[0]
                title =parts[1]
                url = parts[2]
                # Join all word metadata with commas
                writer.writerow([doc_id,title,url])
save_output('new_data.csv',process_data('data.csv'))    