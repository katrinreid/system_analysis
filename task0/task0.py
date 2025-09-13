import csv
import numpy as np
from io import StringIO


def main(csv_text: str, directed: bool = False):
    f = StringIO(csv_text)
    reader = csv.reader(f)
    edges = []
    nodes = set()

    for row in reader:
        if not row:
            continue
        u, v = int(row[0]), int(row[1])
        edges.append((u, v))
        nodes.add(u)
        nodes.add(v)

    nodes = sorted(nodes)
    idx = {node: i for i, node in enumerate(nodes)}

    n = len(nodes)
    arr = np.zeros((n, n), dtype=int)

    for u, v in edges:
        i, j = idx[u], idx[v]
        arr[i][j] = 1
        if not directed:
            arr[j][i] = 1

    return arr, nodes


with open('task0.csv', 'r', encoding='utf-8') as f:
    csv_text = f.read()

matrix, nodes = main(csv_text, directed=False)
print("Матрица смежности:\n", matrix)