import requests
from requests.exceptions import RequestException
from models import Query, Link
import settings
from googlesearch import search as gsearch
from multiprocessing import Pool

def scrape_page(link):
    html = None
    try:
        response = requests.get(link, timeout=5)
        if response.status_code == 200:
            html = response.text
    except RequestException:
        pass
    return html


def search(query, num_results=settings.RESULT_COUNT):
    query_obj = Query.get_or_none(query=query)
    if query_obj:
        if len(query_obj.links) >= settings.MIN_RESULTS:
            return query_obj.links
    else:
        query_obj = Query(query=query)
        query_obj.save()
    links = list(gsearch(query, num_results))

    with Pool(settings.MAX_PROCESSES) as p:
        htmls = p.map(scrape_page, links)

    if len([h for h in htmls if h]) < settings.MIN_RESULTS:
        raise Exception("Not enough results")

    results = []
    for i, (link, html) in enumerate(zip(links, htmls)):
        if html:
            link_obj = Link(
                query=query_obj,
                html=html,
                rank=i+1,
                link=link
            )
            link_obj.save()
            results.append(link_obj)
    return results
