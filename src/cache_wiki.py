import requests
import json
import logging
import argparse

from bs4 import BeautifulSoup

pars = argparse.ArgumentParser()
pars.add_argument("-p", "--text", type=str)
pars.add_argument("-d", "--count", type=int)
args = pars.parse_args()

name_file_json = "wiki.json"
search_teg_a = "wikipedia.org"
url_start = "https://www.wikipedia.org/wiki/" + args.text
url_next = "https://www.wikipedia.org"

limit_count_links_max = 100

if args.count is not None:
    limit_count_links_max = args.count


url_set = set()


def get_links(url):
    try:
        global limit_count_links_max

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = {"url": url, "children": [], "count": 0, "title": soup.title.text}
        soup = BeautifulSoup(response.text, "html.parser")
        linkss = soup.select("#bodyContent a")

        for link in linkss:
            href = link.get("href")
            if href is None:
                continue
            if "http" not in href:
                href = url_next + href
            if search_teg_a in href and check_url(href) and check_link(href):
                url_set.add(href)
                #  print(len(url_set))
                temp = get_links(href)
                if temp is None:
                    continue
                if temp is not None:

                    links["children"].append(temp)
                    links["count"] += 1

        return links
    except Exception as e:

        return None


def check_url(href):
    try:
        if len(url_set) < limit_count_links_max and href not in url_set:
            return True
        else:
            return False
    except Exception as e:
        return False


def check_link(url):
    try:
        response = requests.head(url)
        if response.status_code == 301 and all(
            True if i not in url else False
            for i in ("jpeg", "#", "php?", "jpg", "svg", "png")
        ):
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False


logging.basicConfig(
    filename="log_file.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
all_links = get_links(url_start)


with open(name_file_json, "w", encoding="utf-8") as file:
    json.dump(all_links, file, indent=4)
