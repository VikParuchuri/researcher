from multiprocessing import Pool

import requests
from googlesearch import search as gsearch
from requests.exceptions import RequestException
import stopit

import settings
from models import Query, Link

@stopit.threading_timeoutable(default='not finished')
def gsearch_wrapper(query, num_results):
    return list(gsearch(query, num_results))


def scrape_page(link):
    html = None
    try:
        response = requests.get(link, timeout=settings.RESULT_TIMEOUT)
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
    links = gsearch_wrapper(query, num_results, timeout=settings.RESULT_TIMEOUT)
    if links == 'not finished':
        raise Exception("Problem getting results from search.")
    with Pool(settings.MAX_PROCESSES) as p:
        htmls = p.map(scrape_page, links)

    if len([h for h in htmls if h]) < settings.MIN_RESULTS:
        raise Exception("Not enough results from search.")

    results = []
    for i, (link, html) in enumerate(zip(links, htmls)):
        if html:
            link_obj = Link(
                query=query_obj,
                html=html,
                rank=i + 1,
                link=link
            )
            link_obj.save()
            results.append(link_obj)
    return results
