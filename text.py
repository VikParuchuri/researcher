import math
from itertools import repeat, chain
from typing import NamedTuple

from bs4 import BeautifulSoup
from newspaper import fulltext
from newspaper.cleaners import DocumentCleaner
from newspaper.configuration import Configuration
from newspaper.extractors import ContentExtractor
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer, util

import settings

model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')


class Chunk(NamedTuple):
    text: str
    similarity: float
    link: str
    title: str


def strip_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    for e in soup.find_all():
        if e.name in ['script', 'head', 'style', 'aside', 'footer', 'header', 'nav', 'img', 'svg', 'button', 'form']:
            e.extract()
    return str(soup)


def get_text(text):
    text = strip_html(text)
    try:
        text = fulltext(text, language=settings.LANGUAGE)
    except (AttributeError, TypeError, UnicodeDecodeError):
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
    if chunk_len > settings.CHUNK_MIN_LENGTH:
        chunks.append(chunk)
    return chunks


def find_likely_chunk(link, query_doc):
    if not link.html:
        return None
    title = get_title(link.html)
    text = get_text(link.html)

    if not title or not text:
        return None

    chunks = []
    chunked = split_chunks(text)

    if len(chunked) == 0:
        return None

    chunk_docs = model.encode(chunked)
    similarities = util.cos_sim(query_doc, chunk_docs)[0].tolist()
    for (chunk, similarity) in zip(chunked, similarities):
        chunks.append(Chunk(chunk, similarity, link.link, title))
    sorted_chunks = sorted(chunks, key=lambda x: x.similarity, reverse=True)
    return sorted_chunks[:max(1, math.floor(settings.CHUNK_LIMIT / 2))]


def filter_list(links):
    flat_links = []
    filtered_links = []
    for link in links:
        if link.link not in flat_links:
            filtered_links.append(link)
            flat_links.append(link.link)
    return filtered_links


def find_likely_chunks(links, query):
    links = filter_list(links)
    query_doc = model.encode(query)
    chunks = map(find_likely_chunk, links, repeat(query_doc))
    chunks = [c for c in chunks if c]
    chunks = list(chain.from_iterable(chunks))
    chunks = [c for c in chunks if c]
    sorted_chunks = sorted(chunks, key=lambda x: x.similarity, reverse=True)
    return sorted_chunks[:settings.CHUNK_LIMIT]
