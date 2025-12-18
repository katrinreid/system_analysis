import json
from collections import defaultdict

def flatten_ranking(ranking):
    positions = {}
    for idx, block in enumerate(ranking):
        if isinstance(block, list):
            for item in block:
                positions[item] = idx
        else:
            positions[block] = idx
    return positions


def main(rank1, rank2):

    # Этап 1: ядро противоречий
    pos1 = flatten_ranking(rank1)
    pos2 = flatten_ranking(rank2)

    contradiction_core = [
        item for item in pos1
        if pos1[item] != pos2.get(item)
    ]

    # Этап 2: согласованная кластерная ранжировка
    avg_positions = {}
    for item in pos1:
        avg_positions[item] = (pos1[item] + pos2[item]) / 2

    clusters = defaultdict(list)
    for item, avg in avg_positions.items():
        clusters[avg].append(item)

    result = []
    for _, items in sorted(clusters.items()):
        items.sort()
        if len(items) == 1:
            result.append(items[0])
        else:
            result.append(items)

    return json.dumps(result, ensure_ascii=False)


if __name__ == "__main__":
    with open('rankA.json', 'r', encoding='utf-8') as file:
        rank1 = json.loads(file.read())
    with open('rankB.json', 'r', encoding='utf-8') as file:
        rank2 = json.loads(file.read())
    print(main(rank1, rank2))