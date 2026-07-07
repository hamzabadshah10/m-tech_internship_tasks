def dls(graph, node, goal, limit, depth=0, visited=None):
    if visited is None:
        visited = set()

    if node == goal:
        return True
    if depth >= limit:
        return False

    visited.add(node)
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            if dls(graph, neighbor, goal, limit, depth + 1, visited):
                return True
    return False


def main():
    graph = {
        "A": ["B", "C", "D"],
        "B": ["E", "F"],
        "C": [],
        "D": ["G"],
        "E": [],
        "F": [],
        "G": [],
    }

    for limit in [2, 4]:
        reachable = dls(graph, "A", "F", limit)
        print(f"Limit {limit}: reachable = {reachable}")


if __name__ == "__main__":
    main()
