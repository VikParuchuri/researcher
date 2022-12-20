from bs4 import BeautifulSoup
from urllib.parse import urlparse
import settings


def clean_hostname(hostname):
    hostname = urlparse(hostname).hostname
    if hostname and hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname


with open("blacklist.txt") as f:
    blacklist_domains = set([clean_hostname(l) for l in f.read().split("\n")])


def tracker_urls(text):
    soup = BeautifulSoup(text)
    scripts = soup.find_all("script", {"src": True})
    srcs = [s.get("src") for s in scripts]

    links = soup.find_all("a", {"href": True})
    href = [l.get("href") for l in links]

    all_domains = set([clean_hostname(s) for s in srcs + href if s])
    trackers = all_domains.intersection(blacklist_domains)
    return trackers


def blacklisted_domain(link):
    domain = urlparse(link).hostname
    return domain in blacklist_domains


def filter_links(links):
    filtered_links = []
    for i, link in enumerate(links):
        trackers = tracker_urls(link.html)
        print(link.link)
        print(len(trackers))
        if len(trackers) > settings.MAX_TRACKER_URLS:
            continue

        if blacklisted_domain(link.link):
            continue

        filtered_links.append(link)
    return filtered_links