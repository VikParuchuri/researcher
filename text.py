from newspaper import fulltext
from newspaper.configuration import Configuration
from newspaper.extractors import ContentExtractor
from newspaper.cleaners import DocumentCleaner
import settings
import spacy
from typing import NamedTuple
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_md")


class Chunk(NamedTuple):
    text: str
    similarity: float
    link: str
    title: str


def strip_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    for e in soup.find_all():
        if e.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            e.extract()
        elif e.name not in ['ol', 'ul', 'li', 'pre', 'code', 'p']:
            e.unwrap()
    return str(soup)

def get_text(text):
    text = strip_html(text)
    try:
        text = fulltext(text, language=settings.LANGUAGE)
    except (AttributeError, TypeError):
        text = None
    return text


def get_title(text):
    title = None
    try:
        config = Configuration()
        config.language = settings.LANGUAGE

        extractor = ContentExtractor(config)
        document_cleaner = DocumentCleaner(config)
        doc = config.get_parser().fromstring(text)
        doc = document_cleaner.clean(doc)
        title = extractor.get_title(doc)
    except (AttributeError, TypeError):
        pass
    return title


def split_words(text):
    return text.split()


def split_sentences(text):
    return sent_tokenize(text)


def split_chunks(text):
    sents = [i for i in split_sentences(text)]
    chunks = []
    chunk = ""
    chunk_len = 0
    for sent in sents:
        sent_len = len(split_words(sent))
        if sent_len + chunk_len < settings.CHUNK_MAX_LENGTH:
            chunk += " " + sent
            chunk_len += sent_len
        else:
            chunks.append(chunk)
            chunk = sent
            chunk_len = sent_len
    chunks.append(chunk)
    return chunks


def similarity_score(doc1, doc2):
    return doc1.similarity(doc2)


def similar_chunks(text, title, link, query_doc):
    chunks = []
    chunked = split_chunks(text)
    for chunk in chunked:
        chunk_doc = nlp(chunk)
        chunks.append(Chunk(chunk, similarity_score(query_doc, chunk_doc), link, title))
    return chunks


def find_likely_chunks(links, query):
    chunks = []
    query_doc = nlp(query)
    for i, link in enumerate(links):
        if not link.html:
            continue
        title = get_title(link.html)
        text = get_text(link.html)

        if title and text:
            chunks += similar_chunks(text, title, link.link, query_doc)
    sorted_chunks = sorted(chunks, key=lambda x: x.similarity, reverse=True)
    return sorted_chunks[:settings.RESULT_COUNT]