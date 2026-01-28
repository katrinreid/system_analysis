from pprint import pprint
from typing import List, Tuple


def main(csv_text: str, e: str) -> Tuple[
    List[List[int]],
    List[List[int]],
    List[List[int]],
    List[List[int]],
    List[List[int]],
]:
    connections = [tuple(map(int, line.split(","))) for line in csv_text.strip().splitlines()]
    nodes = sorted({v for pair in connections for v in pair})
    index = {node: idx for idx, node in enumerate(nodes)}
    n = len(nodes)

    root = index[int(e)]

    graph = [[0] * n for _ in range(n)]
    for a, b in connections:
        i, j = index[a], index[b]
        graph[i][j] = 1
        graph[j][i] = -1

    out_m = [[0] * n for _ in range(n)]
    in_m = [[0] * n for _ in range(n)]
    succ_m = [[0] * n for _ in range(n)]
    pred_m = [[0] * n for _ in range(n)]
    bro_m = [[0] * n for _ in range(n)]

    def traverse_successors(r: int, current: int, visited: set[int]):
        for nxt in range(n):
            if graph[current][nxt] == 1 and nxt not in visited:
                succ_m[r][nxt] = 1
                visited.add(nxt)
                traverse_successors(r, nxt, visited)

    def traverse_predecessors(r: int, current: int, visited: set[int]):
        for nxt in range(n):
            if graph[current][nxt] == -1 and nxt not in visited:
                pred_m[r][nxt] = 1
                visited.add(nxt)
                traverse_predecessors(r, nxt, visited)

    def find_brothers(r: int, current: int):
        for nxt in range(n):
            if graph[current][nxt] == 1 and nxt != r:
                bro_m[r][nxt] = 1

    for i in range(n):
        for j in range(n):
            relation = graph[i][j]
            if relation == 1:
                out_m[i][j] = 1
                traverse_successors(i, j, {j})
            elif relation == -1:
                in_m[i][j] = 1
                traverse_predecessors(i, j, {j})
                find_brothers(i, j)

    return out_m, in_m, succ_m, pred_m, bro_m


if __name__ == "__main__":
    with open("graph.csv", "r", encoding="utf-8") as file:
        csv_data = file.read()

    root_node = "1"

    matrices = main(csv_data, root_node)
    labels = ["out", "in", "successors", "predecessors", "brothers"]

    for title, mat in zip(labels, matrices):
        print(f"\n{title} matrix:")
        pprint(mat)
