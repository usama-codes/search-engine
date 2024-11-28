import pandas as pd
import spacy
import re
from collections import Counter

# Load dataset and prepare content
df = pd.read_csv('data.csv', encoding='utf-8')
df['content'] = df['title'] + '\n' + df['text']

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

# Function to clean and tokenize content
def clean_and_tokenize_content(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespaces
    doc = nlp(text.lower())          # Lowercase and tokenize
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return set(tokens)

# Counter to store token frequencies
tokens_counter = Counter()

# Tokenize content and update the counter
for content in df['content']:
    tokens = clean_and_tokenize_content(content)  # Tokenizing the content
    tokens_counter.update(tokens)                 # Updating the counter with token frequencies

# Assign unique IDs to each token
token_to_id = {token: idx for idx, token in enumerate(tokens_counter.keys())}

# Create a DataFrame with tokens, IDs, and frequencies
lexicon_df = pd.DataFrame({
    'Token': token_to_id.keys(),
    'ID': token_to_id.values(),
    'Frequency': [tokens_counter[token] for token in token_to_id.keys()]
})

# Save the lexicon to a CSV file
lexicon_df.to_csv('lexicon_with_ids.csv', index=False)

print("Lexicon with tokens, IDs, and frequencies saved to lexicon_with_ids.csv")