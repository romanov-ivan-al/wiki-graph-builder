import networkx as nx
from pyvis.network import Network
from playwright.sync_api import sync_playwright
import subprocess
import json


with open("wiki.json", "r") as f:
    data = json.load(f)


def traverse_dict(dictionary):
    def traverse(node):
        url = node["url"]
        children = node["children"]
        count = node["count"]
        title = node["title"]
        if count > 0:
            for child in children:
                yield (title, child["title"], count)
        for child in children:
            yield from traverse(child)

    return tuple(traverse(dictionary))


# Создание графа
G = nx.Graph()
data = traverse_dict(data)
data_sizes = {k: v for k, _, v in data}
G.add_edges_from(list(i[:2] for i in data))

# Создание объекта Network
net = Network("1000px", "1000px")

for node in G.nodes:
    net.add_node(node, label=node, size=data_sizes.setdefault(node, 1) * 10)

for source, target in G.edges:
    net.add_edge(source, target)


# Сохранение графа в HTML-файл
net.save_graph("wiki_graph.html")

subprocess.run(["open", "wiki_graph.html"])


def generate_png(url_file, name):
    with sync_playwright() as p:
        for browser_type in [p.chromium]:
            browser = browser_type.launch()
            page = browser.new_page()
            file = open(url_file, "r").read()
            page.set_content(file, wait_until="load")
            page.wait_for_timeout(3)
            page.screenshot(path=f"{name}.png", full_page=True)
            browser.close()


generate_png("wiki_graph.html", "wiki_graph")
