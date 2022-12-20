from flask import Flask, request
from search import search
from text import find_likely_chunks
from filter import filter_links

app = Flask(__name__)

styles = """
<style>
    .site {
        font-size: .8rem;
        color: green;
    }
    
    .snippet {
        font-size: .9rem;
        color: gray;
        margin-bottom: 30px;
    }
</style>
"""

search_template = styles + """
     <form action="/" method="post">
      <input type="text" name="query">
      <input type="submit" value="Search">
    </form> 
    """

result_template = """
<p class="site">{rank}: {link}</p>
<a href="{link}">{title}</a>
<p class="snippet">{snippet}</p>
"""


def show_search_form():
    return search_template


def run_search(query):
    results = search(query)
    results = filter_links(results)
    rendered = search_template
    chunks = find_likely_chunks(results, query)
    for i, chunk in enumerate(chunks):
        data = {
            "title": chunk.title,
            "snippet": chunk.text,
            "rank": i+1,
            "link": chunk.link
        }
        rendered += result_template.format(**data)
    return rendered


@app.route("/", methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form["query"]
        return run_search(query)
    else:
        return show_search_form()
