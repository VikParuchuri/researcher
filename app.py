import time
from urllib.parse import urlparse
import os

from flask import Flask, request, render_template, stream_with_context

import settings
from filter import filter_links
from search import search
from summary import get_summary
from text import find_likely_chunks
import nltk

app = Flask(__name__)


def show_search_form():
    return render_template("index.html", placeholder="Enter search query")

def render_search_results(links=None, chunks=None, summary=None, template="results.html"):
    link_data = None
    chunk_data = None
    if links:
        link_data = []
        for link in links:
            link_data.append({
                "link": link.link,
            })
    if chunks:
        chunk_data = []
        for i, chunk in enumerate(chunks):
            chunk_data.append({
                "title": chunk.title,
                "text": chunk.text[:settings.CHUNK_DISPLAY_CHARS] + "...",
                "rank": i + 1,
                "link": chunk.link,
                "hostname": urlparse(chunk.link).hostname
            })
    return render_template(template, links=link_data, results=chunk_data, summary=summary)


def run_search(query):
    if len(query) < settings.QUERY_MIN_LENGTH:
        raise Exception("Query too short")
    start = time.time()
    results = search(query)

    search_time = time.time()
    print(f"Search runtime: {search_time - start}")

    results = filter_links(results)
    yield render_search_results(links=results, template="links.html")

    chunks = find_likely_chunks(results, query)

    processing_time = time.time()
    print(f"Local processing runtime: {processing_time - search_time}")
    yield render_search_results(chunks=chunks, template="sources.html")

    summary_text = get_summary(query, chunks)

    yield render_search_results(summary=summary_text, template="summary.html")
    print(f"API runtime: {time.time() - processing_time}")


@app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form["query"]
        return stream_with_context(run_search(query)), {"Content-Type": "text/html"}
    else:
        return show_search_form()


if __name__ == "__main__":
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    nltk.download('punkt')
    app.run(debug=True)
