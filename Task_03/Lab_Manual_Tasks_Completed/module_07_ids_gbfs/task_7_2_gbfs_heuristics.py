def greedy_bfs(graph, start, goal, heuristic):
    open_list = [start]
    visited = []
    path = []

    while open_list:
        current = min(open_list, key=lambda node: heuristic[node])
        open_list.remove(current)
        path.append(current)

        if current == goal:
            return path

        visited.append(current)
        for neighbor in graph[current]:
            if neighbor not in visited and neighbor not in open_list:
                open_list.append(neighbor)
    return path


def main():
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": [],
        "E": ["G"],
        "F": [],
        "G": [],
    }

    heuristic_sets = [
        {"A": 7, "B": 6, "C": 2, "D": 1, "E": 1, "F": 3, "G": 0},
        {"A": 4, "B": 3, "C": 5, "D": 2, "E": 1, "F": 4, "G": 0},
    ]

    for index, heuristic in enumerate(heuristic_sets, start=1):
        path = greedy_bfs(graph, "A", "G", heuristic)
        print(f"Heuristic set {index}: {path}")


if __name__ == "__main__":
    main()
