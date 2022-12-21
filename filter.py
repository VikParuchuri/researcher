from bs4 import BeautifulSoup
from urllib.parse import urlparse
import settings
from multiprocessing import Pool

def clean_hostname(hostname):
    hostname = urlparse(hostname).hostname
    if hostname and hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname


with open("blacklist.txt") as f:
    blacklist_domains = set([clean_hostname(l) for l in f.read().split("\n")])


def tracker_urls(text):
    soup = BeautifulSoup(text, parser="html.parser")
    scripts = soup.find_all("script", {"src": True})
    srcs = [s.get("src") for s in scripts]

    links = soup.find_all("a", {"href": True})
    href = [l.get("href") for l in links]

    all_domains = set([clean_hostname(s) for s in srcs + href if s])
    trackers = all_domains.intersection(blacklist_domains)
    return trackers


def total_scripts(text):
    soup = BeautifulSoup(text, parser="html.parser")
    scripts = soup.find_all("script")
    return len(scripts)


def blacklisted_domain(link):
    domain = urlparse(link).hostname
    return domain in blacklist_domains


def filter_link(link):
    trackers = tracker_urls(link.html)
    script_count = total_scripts(link.html)
    if len(trackers) > settings.MAX_TRACKER_URLS:
        return None

    if blacklisted_domain(link.link):
        return None

    if script_count > settings.MAX_SCRIPTS:
        return None

    return link


def filter_links(links):
    links = map(filter_link, links)

    return [l for l in links if l]