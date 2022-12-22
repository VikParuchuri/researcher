from multiprocessing import Pool
import math
from urllib.parse import quote_plus

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

def scrape_playwright(link, browser):
    pass


def search_api(query, pages):
    results = []
    for i in range(0, pages):
        start = i*10+1
        url = settings.SEARCH_URL.format(
            key=settings.SEARCH_KEY,
            cx=settings.SEARCH_ID,
            query=quote_plus(query),
            start=start
        )
        response = requests.get(url)
        data = response.json()
        results += data["items"]
    links = [r["link"] for r in results]
    return links


def search(query, num_results=settings.RESULT_COUNT):
    query_obj = Query.get_or_none(query=query)
    if query_obj:
        if len(query_obj.links) >= settings.MIN_RESULTS:
            return query_obj.links
    else:
        query_obj = Query(query=query)
        query_obj.save()
    if settings.SEARCH_METHOD == "scrape":
        links = gsearch_wrapper(query, num_results, timeout=settings.RESULT_TIMEOUT)
    else:
        links = search_api(query, pages=math.ceil(num_results/10))
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
