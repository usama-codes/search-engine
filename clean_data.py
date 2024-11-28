import pandas as pd
import spacy
import re
from collections import Counter


df = pd.read_csv('data.csv', encoding='utf-8')
df['content'] = df['title'] + '\n' + df['text']


nlp = spacy.load('en_core_web_sm')  # Load the spaCy model

def clean_and_tokenize_content(text):
    text = re.sub(r'\s+', ' ', text)
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return set(tokens)


tokens_counter = Counter()  # Counter to store the token frequencies

for content in df['content']:
    tokens = clean_and_tokenize_content(content)    # Tokenizing the content
    tokens_counter.update(tokens)                   # Updating the counter with the token frequencies

lexicon_df = pd.DataFrame(tokens_counter.items(), columns=['Token', 'Frequency'])

lexicon_df.to_csv('lexicon.csv', index=False)

print("Lexicon with token frequencies saved to lexicon.csv")