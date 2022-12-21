from flask import Flask, request, render_template
import settings
from search import search
from text import find_likely_chunks
from filter import filter_links
import time
from summary import generate_prompt, get_summary

app = Flask(__name__)

def show_search_form():
    return render_template("index.html", placeholder="Enter search query")

def run_search(query):
    if len(query) < settings.QUERY_MIN_LENGTH:
        raise Exception("Query too short")
    start = time.time()
    results = search(query)
    print(time.time() - start)
    results = filter_links(results)
    print(time.time() - start)
    chunks = find_likely_chunks(results, query)
    summary_text = get_summary(query, chunks)
    print(time.time() - start)
    template_results = []
    for i, chunk in enumerate(chunks):
        data = {
            "title": chunk.title,
            "text": chunk.text[:settings.CHUNK_DISPLAY_CHARS] + "...",
            "rank": i+1,
            "link": chunk.link
        }
        template_results.append(data)
    return render_template("index.html", results=template_results, placeholder=query, summary=summary_text)


@app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form["query"]
        return run_search(query)
    else:
        return show_search_form()
