def dfs_paths(graph, node, goal, path=None):
    if path is None:
        path = []

    path = path + [node]
    if node == goal:
        return [path]

    paths = []
    for neighbor in graph.get(node, []):
        if neighbor not in path:
            paths.extend(dfs_paths(graph, neighbor, goal, path))
    return paths


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
    paths = dfs_paths(graph, "A", "F")
    print("All paths from A to F:")
    for p in paths:
        print(" -> ".join(p))


if __name__ == "__main__":
    main()
