import csv
import re
from collections import defaultdict

def preprocess_text(text):
    
    #wordizes and preprocesses text
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)  # removing non words
    words = text.split()
    return words

def build_forward_index(data_file, lexicon_file, output_file):
    """
    reading the data.csv and lexicon.csv files
    and then making a forward index that maps document on word ids and lemma ids
    """
    # loading the text from data
    documents = []
    with open(data_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = row.get('text', '')
            documents.append(text)

    # Load the lexicon mapping of word to wordID and lemmaID
    word_to_id = {}
    lemma_to_id = {}
    with open(lexicon_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            word = row.get('Word', '')
            word_id = row.get('Word ID', '')
            lemma_id = row.get('Lemma ID', '')
            #loading the list of word ids and lemma ids
            if word and word_id and lemma_id:
                word_to_id[word] = word_id
                lemma_to_id[word] = lemma_id

    # making the dict of forward index
    forward_index = {}
    for i, text in enumerate(documents, start=1):  # making documentID from 1 to n
        words = preprocess_text(text)
        word_ids = [word_to_id[word] for word in words if word in word_to_id]
        lemma_ids = [lemma_to_id[word] for word in words if word in lemma_to_id]
        forward_index[i] = {'wordIDs': word_ids, 'LemmaIDs': lemma_ids}

    # to store the forward index to new csv file 
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['DocumentID', 'wordIDs', 'LemmaIDs'])  # header of csv
        #for loop to write all the elements in forward index dict to the csv file
        for doc_id, ids in forward_index.items():
            writer.writerow([
                doc_id,
                ' '.join(ids['wordIDs']),  # Join word IDs with spaces
                ' '.join(ids['LemmaIDs'])   # Join lemma IDs with spaces
            ])

# path of input output files
data_csv = 'data.csv'
lexicon_csv = 'lexicon.csv'
output_csv = 'forward_index.csv'

# building the forward index and saving the files
build_forward_index(data_csv, lexicon_csv, output_csv)

print(f"forward index stored to path {output_csv}")
