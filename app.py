from flask import Flask, request, render_template
import settings
from search import search
from text import find_likely_chunks
from filter import filter_links
import time
from summary import get_summary
from urllib.parse import urlparse

app = Flask(__name__)

def show_search_form():
    return render_template("index.html", placeholder="Enter search query")

def run_search(query):
    if len(query) < settings.QUERY_MIN_LENGTH:
        raise Exception("Query too short")
    start = time.time()
    results = search(query)
    results = filter_links(results)
    chunks = find_likely_chunks(results, query)
    print(time.time() - start)
    summary_text = get_summary(query, chunks)
    print(time.time() - start)
    template_results = []
    for i, chunk in enumerate(chunks):
        data = {
            "title": chunk.title,
            "text": chunk.text[:settings.CHUNK_DISPLAY_CHARS] + "...",
            "rank": i+1,
            "link": chunk.link,
            "hostname": urlparse(chunk.link).hostname
        }
        template_results.append(data)
    return render_template("index.html", results=template_results, placeholder="", summary=summary_text, query=query)


@app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form["query"]
        return run_search(query)
    else:
        return show_search_form()
