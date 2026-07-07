from collections import deque


def path_exists(graph, start, goal):
    queue = deque([start])
    visited = set()

    while queue:
        node = queue.popleft()
        if node == goal:
            return True
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                queue.append(neighbor)
    return False


def main():
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
        "D": [],
        "E": ["F"],
        "F": [],
    }
    print(path_exists(graph, "A", "F"))


if __name__ == "__main__":
    main()
