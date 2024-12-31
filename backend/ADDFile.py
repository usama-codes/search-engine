import csv
import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class ADDFile:
    csv.field_size_limit(10**7)
    def __init__(self, lexicon_file, barrel_directory, doc_id_file, num_barrels=50):
        self.lexicon_file = lexicon_file
        self.barrel_directory = barrel_directory
        self.doc_id_file = doc_id_file
        self.num_barrels = num_barrels
        self.lexicon = self._load_lexicon()
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

        # Ensure barrel directory exists
        if not os.path.exists(self.barrel_directory):
            os.makedirs(self.barrel_directory)
#loading the lexicon from the lexicon file
    def _load_lexicon(self):
        lexicon = {}
        with open(self.lexicon_file, 'r', encoding='utf-8') as f:
            next(f)  # Skip header row
            for line in f:
                word, word_id, lemma_id = line.strip().split(',')
                lexicon[word] = (int(word_id), int(lemma_id))
        return lexicon
#getting the document it from text file and incrementing it
    def _get_next_doc_id(self):
        """
        Read and increment the document ID from the doc_id file.
        """
        if not os.path.exists(self.doc_id_file):
            with open(self.doc_id_file, 'w') as f:
                f.write('1')  # Initialize with the first doc_id

        with open(self.doc_id_file, 'r+') as f:
            current_id = int(f.read().strip())
            new_id = current_id + 1
            f.seek(0)
            f.write(str(new_id))
            f.truncate()
        return new_id
    #cleaning the text of the new document and tokenizing it

    def _clean_and_tokenize(self, text):
        """
        Tokenizes and lemmatizes the input text while removing stopwords.
        """
        text = re.sub(r'http[s]?://\S+|[^a-zA-Z0-9\s]+|\s+', ' ', text).strip()
        tokens = word_tokenize(text.lower())

        tokens = [
            (word, self.lemmatizer.lemmatize(word))
            for word in tokens
            if word not in self.stop_words and word.isalpha()
        ]
        return tokens
#updating the barrel with the new document by the word id 
    def _update_barrel(self, word_id, doc_bitarray_entry):
        """
        Update the specific barrel for the given word ID.
        """
        barrel_index = word_id % self.num_barrels
        barrel_file = os.path.join(self.barrel_directory, f'barrel_{barrel_index}.csv')

        updated = False
        barrel_data = []

        if os.path.exists(barrel_file):
            with open(barrel_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                for row in reader:
                    current_word_id = int(row[0])
                    doc_info = row[1]
                    if current_word_id == word_id:
                        doc_info += f" {doc_bitarray_entry}"
                        updated = True
                    barrel_data.append((current_word_id, doc_info))

        if not updated:
            barrel_data.append((word_id, doc_bitarray_entry))

        with open(barrel_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['word_id', 'doc_info'])
            writer.writerows(barrel_data)
#updating the inverted index with the new document
    def update_index(self, new_file):
        """
        Update the inverted index using the data from the new file.
        """
        doc_id = self._get_next_doc_id()

        with open(new_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                title = row[0]
                url = row[2]
                text = row[1]
                tags = row[5] if len(row) > 5 else ""
                with open('D:/NUST/SEMESTER_3/DSA/End_Project/test/engine_data/newdata.csv', 'a', encoding='utf-8', newline='') as h:
                    writer = csv.writer(h)
                    writer.writerow([doc_id, title, url, tags])

                tokens = self._clean_and_tokenize(title + ' ' + text + ' ' + tags)
                words_in_title = set(title.lower().split())
                words_in_tags = set(tags.lower().split())

                word_frequency = {}
                for word, lemma in tokens:
                    if word in self.lexicon:
                        word_id, lemma_id = self.lexicon[word]
                        title_presence = 1 if word in words_in_title else 0
                        tag_presence = 1 if word in words_in_tags else 0
                        bitarray = (title_presence << 9) | (tag_presence << 8) | min(word_frequency.get(word, 0), 255)

                        if word in word_frequency:
                            word_frequency[word] += 1
                        else:
                            word_frequency[word] = 1

                        doc_bitarray_entry = f"{doc_id}:{bitarray}"
                        self._update_barrel(lemma_id, doc_bitarray_entry)

        print(f"Inverted index updated successfully for document ID {doc_id}.")


# temporary example usage of the ADDFile class
if __name__ == "__main__":
    lexicon_file = 'lexicon.csv'
    barrel_directory = 'barrels'
    doc_id_file = 'doc_id.txt'
    new_file = 'download/download1.csv'

    index_manager = ADDFile(lexicon_file, barrel_directory, doc_id_file)
    index_manager.update_index(new_file)
