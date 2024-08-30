import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-v", action="store_true")
parser.add_argument("--from", dest="start", type=str)
parser.add_argument("--to", dest="finish", type=str)
parser.add_argument("--non-directed", action="store_true")
args = parser.parse_args()


start = args.start
finish = args.finish

count_map = dict()


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


with open("wiki.json", "r") as f:
    data = json.load(f)
    res_graf = tuple((str(i[0]), str(i[1])) for i in traverse_dict(data))


def edges_to_graph(point, edges_tuple, sring_edge, count=1, visited=None):
    if visited is None:
        visited = set()
    for i in edges_tuple:
        if i[1] == finish and i[0] == point:
            count_map[count] = sring_edge + " -> " + i[1]
        if i[0] == point and count < len(edges_tuple) and i[1] not in visited:
            visited.add(i[1])
            edges_to_graph(
                i[1], edges_tuple, sring_edge + " -> " + i[1], count + 1, visited
            )


def edges_to_graph_two(point, edges_tuple, sring_edge, count=1, visited=None):
    if visited is None:
        visited = set()
    for i in edges_tuple:
        if i[1] == finish and i[0] == point:
            count_map[count] = sring_edge + " -> " + i[1]
            break
        elif i[0] == finish and i[1] == point:
            count_map[count] = sring_edge + " -> " + i[0]
            break

        if i[0] == point and count < len(edges_tuple) and i[1] not in visited:
            visited.add(i[1])
            edges_to_graph_two(
                i[1], edges_tuple, sring_edge + " -> " + i[1], count + 1, visited
            )
        if i[1] == point and count < len(edges_tuple) and i[0] not in visited:
            visited.add(i[0])
            edges_to_graph_two(
                i[0], edges_tuple, sring_edge + " -> " + i[0], count + 1, visited
            )


if args.non_directed:
    edges_to_graph_two(start, res_graf, start)
else:
    edges_to_graph(start, res_graf, start)


if len(count_map) != 0:
    result_min = min(count_map)
    print(result_min)
    if args.v:
        print(count_map[result_min])
else:
    print("path not found")
