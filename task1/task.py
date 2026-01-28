from pprint import pprint


def main(csv_text):
    connections = [tuple(map(int, line.split(","))) for line in csv_text.strip().splitlines()]
    nodes = sorted({v for pair in connections for v in pair})
    index = {node: idx for idx, node in enumerate(nodes)}
    n = len(nodes)

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

    def traverse_successors(root: int, current: int, visited: set[int]):
        for nxt in range(n):
            if graph[current][nxt] == 1 and nxt not in visited:
                succ_m[root][nxt] = 1
                visited.add(nxt)
                traverse_successors(root, nxt, visited)

    def traverse_predecessors(root: int, current: int, visited: set[int]):
        for nxt in range(n):
            if graph[current][nxt] == -1 and nxt not in visited:
                pred_m[root][nxt] = 1
                visited.add(nxt)
                traverse_predecessors(root, nxt, visited)

    def find_brothers(root: int, current: int):
        for nxt in range(n):
            if graph[current][nxt] == 1 and nxt != root:
                bro_m[root][nxt] = 1

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

    return [out_m, in_m, succ_m, pred_m, bro_m]


if __name__ == "__main__":
    with open("task1.csv", "r", encoding="utf-8") as file:
        csv_data = file.read()

    matrices = main(csv_data)
    labels = ["out", "in", "successors", "predecessors", "brothers"]
    
    for title, mat in zip(labels, matrices):
        print(f"\n{title} matrix:")
        pprint(mat)
