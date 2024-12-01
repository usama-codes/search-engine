import pandas as pd
import spacy
import re

class Lexicon:
    """Class to build and manage lexicon mappings and save them to a file."""

    nlp = spacy.load('en_core_web_sm')

    def __init__(self, number_lemma_id = 9999, spacy_model='en_core_web_sm'):
        self.wordID = {}
        self.lemmaID = {}
        self.wordToLemmaID = {}
        self.word_counter = 0
        self.lemma_counter = 0
        self.nlp = spacy.load(spacy_model)
        self.number_lemma_id = number_lemma_id
    
    def clean_and_tokenize(self, text):
        """Cleans and tokenizes the text."""
        text = re.sub(r'http[s]?://\S+|[^a-zA-Z0-9\s]|\s+', ' ', text)  # Remove URLs, non-alphanumeric characters, and extra whitespaces
        text = re.sub(r'\s+', ' ', text)                              # Remove extra whitespaces
        doc = self.nlp(text.lower())
        tokens = [
            (token.text, token.lemma_)
            for token in doc
            if token.text.strip() != '' and not token.is_stop and not token.is_punct
        ]
        return tokens
    
    def process_tokens(self, tokens):
        """Processes tokens to create mappings."""
        for word, lemma in tokens:
            if word is None or word == '':
                continue  # Skip empty or None words

            word = word.lower()
            lemma = lemma.lower()

            # Handle special lemma ID for numbers
            if word.isdigit():
                if word not in self.wordID:
                    self.wordID[word] = self.word_counter
                    self.word_counter += 1
                lemma = str(self.number_lemma_id)
            else:
                if word not in self.wordID:
                    self.wordID[word] = self.word_counter
                    self.word_counter += 1
                if lemma not in self.lemmaID:
                    self.lemmaID[lemma] = self.lemma_counter
                    self.lemma_counter += 1
            
            # Map Word ID to Lemma ID
            self.wordToLemmaID[self.wordID[word]] = self.lemmaID.get(lemma, self.number_lemma_id)
            

    def build_lexicon(self):
        """Builds a lexicon DataFrame."""
        lexicon_data = [
            (word, word_id, self.wordToLemmaID[word_id])
            for word, word_id in self.wordID.items()
        ]
        return pd.DataFrame(lexicon_data, columns=['Word', 'Word ID', 'Lemma ID'])

    def save_lexicon(self, file_path):
        """Saves the lexicon to a CSV file."""
        lexicon_df = self.build_lexicon()
        lexicon_df.to_csv(file_path, index=False)
        return len(self.wordID)


def main():
    # Load dataset
    df = pd.read_csv('data.csv', encoding='utf-8')
    df['content'] = df['title'] + '\n' + df['text']

    # Initialize classes
    lexicon = Lexicon()

    # Process the content
    for content in df['content']:
        tokens = lexicon.clean_and_tokenize(content)
        lexicon.process_tokens(tokens)

    # Save lexicon to file
    num_unique_words = lexicon.save_lexicon('lexicon.csv')
    print("Lexicon with Word IDs and Lemma IDs saved to lexicon.csv")
    print(f"Number of unique words: {num_unique_words}")

if __name__ == "__main__":
    main()