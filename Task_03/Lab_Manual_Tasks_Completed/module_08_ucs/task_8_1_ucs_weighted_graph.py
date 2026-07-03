import heapq


def ucs(graph, start, goal):
    pq = [(0, start, [])]
    visited = []

    while pq:
        cost, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.append(node)
        path = path + [node]

        if node == goal:
            return cost, path

        for neighbor, edge_cost in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + edge_cost, neighbor, path))

    return float("inf"), []


def main():
    graph = {
        "A": [("B", 1), ("C", 4)],
        "B": [("D", 2), ("E", 5)],
        "C": [("F", 3)],
        "D": [("G", 1)],
        "E": [("G", 2)],
        "F": [("G", 5)],
        "G": [],
    }

    cost, path = ucs(graph, "A", "G")
    print(f"Path: {path}, Cost: {cost}")


if __name__ == "__main__":
    main()
