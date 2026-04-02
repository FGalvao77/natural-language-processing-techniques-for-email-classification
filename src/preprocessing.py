# src/preprocessing.py
import re
import unicodedata
import spacy

from typing import List
from datetime import timedelta, datetime

def add_business_days(start_date, num_days) -> object:
    current_date = start_date
    business_days_added = 0
    while business_days_added < num_days:
        current_date += timedelta(days=1)
        # Monday=0, Sunday=6
        if current_date.weekday() < 5:  # Check if it's not a Saturday (5) or Sunday (6)
            business_days_added += 1
    return current_date

TODAY = datetime.today()
MAXIMUM_RESPONSE_TIME = 5
EXPECTED_BUSINESS_DATE = add_business_days(TODAY, MAXIMUM_RESPONSE_TIME)

nlp = spacy.load('pt_core_news_sm', disable=['parser', 'ner'])

URL_OR_EMAIL = re.compile(r'(https?://\S+|\S+@\S+\.\S+)')

def normalize_unicode(text: str) -> str:
    return unicodedata.normalize('NFKC', text)

def remove_noise(text: str) -> str:
    text = URL_OR_EMAIL.sub(' ', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'[_\-]{2,}', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text or '')
    text = normalize_unicode(text)
    text = text.lower()
    text = remove_noise(text)
    return text

def preprocess_text(text: str, remove_stopwords: bool = True, lemmatize: bool = True) -> str:
    text = clean_text(text)
    doc = nlp(text)
    tokens = []
    for tok in doc:
        if tok.is_punct or tok.is_space:
            continue
        if remove_stopwords and tok.is_stop:
            continue
        if lemmatize:
            lemma = tok.lemma_.strip()
            if lemma:
                tokens.append(lemma)
        else:
            tokens.append(tok.text)
    return ' '.join(tokens)

def batch_preprocess(texts: List[str], **kwargs) -> List[str]:
    return [preprocess_text(t, **kwargs) for t in texts]

if __name__ == '__main__':
    print(preprocess_text(f'Olá, favor enviar o contrato para fulano@example.com. Prazo {EXPECTED_BUSINESS_DATE}'))





