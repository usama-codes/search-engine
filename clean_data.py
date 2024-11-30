import pandas as pd
import spacy
import re

# Loading and reading the dataset
df = pd.read_csv('data.csv', encoding='utf-8')
df['content'] = df['title'] + '\n' + df['text']

# Loading spacy model for text processing
nlp = spacy.load('en_core_web_sm')

# Function to clean and tokenize the content
def clean_and_tokenize_content(text):
    text = re.sub(r'http[s]?://\S+|[^a-zA-Z0-9\s]|\s+', ' ', text)  # Remove URLs, non-alphanumeric characters and extra whitespaces
    text = re.sub(r'\s+', ' ', text)                              # Remove extra whitespaces
    doc = nlp(text.lower())          
    tokens = [(token.text, token.lemma_) for token in doc if token.text.strip() != '' and not token.is_stop and not token.is_punct] 
    return tokens

word_to_id = {} # Word to ID mapping
lemma_to_id = {}    # Lemma to ID mapping
word_id_to_lemma_id = {}    # Word ID to Lemma ID mapping

word_counter = 0
lemma_counter = 0

# Special Lemma ID for numbers
number_lemma_id = 9999

for content in df['content']:
    tokens = clean_and_tokenize_content(content)
    for word, lemma in tokens:
        # Assign a special lemma ID for numbers
        if word.isdigit():
            if word not in word_to_id:
                word_to_id[word] = word_counter
                word_counter += 1
            lemma = str(number_lemma_id)

        else:
            if word not in word_to_id:
                word_to_id[word] = word_counter
                word_counter += 1
            
            if lemma not in lemma_to_id:
                lemma_to_id[lemma] = lemma_counter
                lemma_counter += 1

        # Assign the lemma ID to the word ID
        word_id_to_lemma_id[word_to_id[word]] = lemma_to_id.get(lemma, number_lemma_id)

lexicon_data = []
# Create a lexicon with Word IDs and Lemma IDs
for word, word_id in word_to_id.items():
    lemma_id = word_id_to_lemma_id[word_id]
    lexicon_data.append((word, word_id, lemma_id))

lexicon_df = pd.DataFrame(lexicon_data, columns=['Word', 'Word ID', 'Lemma ID'])

lexicon_df.to_csv('lexicon.csv', index=False)

print("Lexicon with Word IDs and Lemma IDs saved to lexicon.csv")
print("Number of unique words:", len(word_to_id))