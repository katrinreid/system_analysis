from math import log2, log, e
from collections import deque


def analyze_graph(data: str, root_node: str) -> tuple[float, float]:
    edge_list = [tuple(map(int, line.split(","))) for line in data.strip().splitlines()]

    vertices = sorted({v for edge in edge_list for v in edge})
    total_nodes = len(vertices)
    root = int(root_node)

    graph = {v: set() for v in vertices}
    for a, b in edge_list:
        graph[a].add(b)

    rel1 = set(edge_list)
    rel2 = {(b, a) for a, b in edge_list}

    rel3 = set()
    for a in vertices:
        for mid in graph[a]:
            for b in graph.get(mid, []):
                if b != a:
                    rel3.add((a, b))
    rel3 -= rel1
    rel4 = {(b, a) for a, b in rel3}

    levels = {root: 0}
    queue = deque([root])
    while queue:
        current = queue.popleft()
        for neighbor in graph.get(current, []):
            if neighbor not in levels:
                levels[neighbor] = levels[current] + 1
                queue.append(neighbor)

    rel5 = {(a, b) for a in vertices for b in vertices if a != b and levels.get(a) == levels.get(b)}

    relations = [rel1, rel2, rel3, rel4, rel5]

    L_values = {v: [] for v in vertices}
    for v in vertices:
        for rel in relations:
            count = sum(1 for (a, b) in rel if a == v)
            L_values[v].append(count)

    H = 0.0
    for v in vertices:
        for lij in L_values[v]:
            if lij > 0:
                p = lij / (total_nodes - 1)
                H -= p * log2(p)

    H = round(H, 1)

    coef = 1 / (e * log(2))
    relation_types = 5
    H_ref = coef * total_nodes * relation_types
    H_norm = round(H / H_ref, 2)

    return H, H_norm


if __name__ == "__main__":
    with open("task2.csv", encoding="utf-8") as f:
        content = f.read()
    print(analyze_graph(content, "1"))