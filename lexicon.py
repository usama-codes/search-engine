import pandas as pd
import re
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import cProfile

class Lexicon:
    """Class to build and manage lexicon mappings and save them to a file."""
    nltk.download('averaged_perceptron_tagger', quiet=True)

    def __init__(self):
        self.wordID = {}
        self.lemmaID = {}
        self.wordToLemmaID = {}
        self.word_counter = 0
        self.lemma_counter = 0
        
        # Initialize NLTK resources
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def get_wordnet_pos(self, tag):
        """Map POS tag to the format recognized by WordNetLemmatizer."""
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN 
    
    def clean_and_tokenize(self, text):
        """Cleans and tokenizes the text."""
        # Clean text using regex
        text = re.sub(r'http[s]?://\S+|[^a-zA-Z0-9\s]+|\s+', ' ', text).strip()
        
        # Tokenize using NLTK
        tokens = word_tokenize(text.lower())
        
        pos_tags = nltk.pos_tag(tokens)

        # Lemmatize and filter stop words and punctuation
        tokens = [
            (word, self.lemmatizer.lemmatize(word, self.get_wordnet_pos(pos)))
            for word, pos in pos_tags
            if word not in self.stop_words and word.isalpha()
        ]
        return tokens
    
    def process_tokens(self, tokens):
        """Processes tokens to create mappings."""
        for word, lemma in tokens:
            if word is None or word == '':
                continue  # Skip empty or None words

            word = word.lower()
            lemma = lemma.lower()

            if word not in self.wordID:
                self.wordID[word] = self.word_counter
                self.word_counter += 1
            if lemma not in self.lemmaID:
                self.lemmaID[lemma] = self.lemma_counter
                self.lemma_counter += 1
            
            # Map Word ID to Lemma ID
            self.wordToLemmaID[self.wordID[word]] = self.lemmaID.get(lemma)
    
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
    df['content'] = df['content'].fillna('').astype(str)
    
    # Initialize classes
    lexicon = Lexicon()

    # Process the content
    total_articles = len(df)
    for idx, content in enumerate(df['content']):
        tokens = lexicon.clean_and_tokenize(content)
        lexicon.process_tokens(tokens)

        # Print progress every 500 articles
        if (idx + 1) % 500 == 0:
            print(f"Processed {idx + 1}/{total_articles} articles.")

    # Save lexicon to file
    num_unique_words = lexicon.save_lexicon('lexicon.csv')
    print("Lexicon with Word IDs and Lemma IDs saved to lexicon.csv")
    print(f"Number of unique words: {num_unique_words}")

def profile_main():
    main()

if __name__ == "__main__":
    main()