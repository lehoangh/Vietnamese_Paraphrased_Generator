from pyvi import ViTokenizer

'''
tokenization code
'''

import spacy
spacy_vi = spacy.load('vi_core_news_lg')
stopwords = spacy_vi.Defaults.stop_words

def tokenize_vi(text):
    """
    Tokenizes Vietnamese text from a string into a list of strings (tokens)
    """
    return [tok.text for tok in spacy_vi.tokenizer(text)]