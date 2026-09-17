# -*- coding: utf-8 -*-
"""Limpieza de texto (mismo criterio del notebook MP2)."""
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

_STEMMER = None
_STOPWORDS = None


def _ensure_nltk():
    global _STEMMER, _STOPWORDS
    if _STEMMER is not None:
        return
    for recurso in ("punkt", "punkt_tab", "stopwords"):
        try:
            nltk.download(recurso, quiet=True)
        except Exception:
            pass
    _STEMMER = SnowballStemmer("spanish")
    _STOPWORDS = set(stopwords.words("spanish"))


def text_preprocess(text):
    """Limpieza al estilo del tutorial del curso, en español."""
    _ensure_nltk()
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z\u00c0-\u017f\s]", " ", text)
    tokens = word_tokenize(text, language="spanish")
    tokens = [t for t in tokens if t not in _STOPWORDS and len(t) > 2]
    tokens = [_STEMMER.stem(t) for t in tokens]
    return " ".join(tokens)
