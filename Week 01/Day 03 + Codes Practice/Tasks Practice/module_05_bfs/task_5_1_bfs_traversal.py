from collections import deque


def bfs(graph, start):
    visited = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
    return visited


def main():
    graph = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F", "G"],
        "D": ["H"],
        "E": ["I"],
        "F": [],
        "G": ["J"],
        "H": [],
        "I": [],
        "J": [],
    }
    print("BFS traversal:", bfs(graph, "A"))


if __name__ == "__main__":
    main()
