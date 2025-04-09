"""The currently supported stemmers.
These are called stemmers for legacy reasons, but they are actually any useful sort of simplifiers, be it lemmatizers or else.
Also, notice dummy stemmer that leaves words as they are,
so algoritms can also work without stemming."""

import spacy
import stanza
import spacy_stanza
from spacy import displacy
from tqdm import tqdm

from settings import LANG, DEVICE

from util import tokenizer

# stanza.download(LANG)
nlp = spacy_stanza.load_pipeline("xx", lang=LANG, use_gpu=DEVICE != 'CPU')


def stanza_lemmatize(word, sent):
    if not sent:
        sent = word
    doc = nlp(sent)
    for token in doc:
        if token.text == word:
            return token.lemma_


def stanza_sent_lemmatize(sent):
    doc = nlp(sent)
    return [(token.text, token.lemma_) for token in doc]


# changes here need to also be reflected in static/index.html
# en
all_stemmers = {
    "cu": {
        "dummy": lambda word, sent: word.lower(),
        "stanza": stanza_lemmatize,
    }
}

all_sent_stemmers = {
    "cu": {
        "dummy": lambda x: [(t, t) for t in tokenizer(x) if t.strip()],
        "stanza": stanza_sent_lemmatize,
    }
}

stemmers = all_stemmers[LANG]
sent_stemmers = all_sent_stemmers[LANG]

stemmer_labels = {
    "dummy": "Word Forms",
    "stanza": "Lemmatizer",
}

# default_stemmer = "stanza"
default_stemmer = "dummy"
