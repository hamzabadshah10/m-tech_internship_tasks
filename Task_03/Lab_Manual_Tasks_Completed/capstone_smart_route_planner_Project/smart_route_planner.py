import heapq


def bfs(graph, start, goal):
    from collections import deque

    queue = deque([start])
    visited = {start}
    parents = {start: None}

    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            current = node
            while current is not None:
                path.append(current)
                current = parents[current]
            return path[::-1]

        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parents[neighbor] = node
                queue.append(neighbor)

    return []


def dfs(graph, start, goal):
    stack = [(start, [start])]

    while stack:
        node, path = stack.pop()
        if node == goal:
            return path

        for neighbor, _ in reversed(graph.get(node, [])):
            if neighbor not in path:
                stack.append((neighbor, path + [neighbor]))

    return []


def ucs(graph, start, goal):
    pq = [(0, start, [start])]
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)
        if node == goal:
            return path, cost
        if node in visited:
            continue
        visited.add(node)
        for neighbor, edge_cost in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + edge_cost, neighbor, path + [neighbor]))
    return [], float('inf')


def a_star(graph, start, goal, heuristic):
    pq = []
    heapq.heappush(pq, (heuristic[start], 0, start, [start]))
    visited = set()

    while pq:
        f, g, node, path = heapq.heappop(pq)
        if node == goal:
            return path, g
        if node in visited:
            continue
        visited.add(node)
        for neighbor, edge_cost in graph.get(node, []):
            if neighbor not in visited:
                g_new = g + edge_cost
                f_new = g_new + heuristic[neighbor]
                heapq.heappush(pq, (f_new, g_new, neighbor, path + [neighbor]))
    return [], float('inf')


def main():
    graph = {
        "A": [("B", 3), ("C", 5)],
        "B": [("D", 2), ("E", 4)],
        "C": [("F", 2), ("G", 6)],
        "D": [("H", 3)],
        "E": [("H", 2), ("I", 4)],
        "F": [("I", 2)],
        "G": [("J", 3)],
        "H": [("J", 2)],
        "I": [("J", 1)],
        "J": [],
    }
    heuristic = {"A": 8, "B": 5, "C": 6, "D": 4, "E": 3, "F": 4, "G": 4, "H": 2, "I": 1, "J": 0}

    start = input("Enter start node: ").strip().upper()
    goal = input("Enter goal node: ").strip().upper()

    if start not in graph or goal not in graph:
        print("Invalid node. Please enter a valid node from the graph.")
        return

    results = []
    bfs_path = bfs(graph, start, goal)
    dfs_path = dfs(graph, start, goal)
    ucs_path, ucs_cost = ucs(graph, start, goal)
    astar_path, astar_cost = a_star(graph, start, goal, heuristic)

    results.append(("BFS", bfs_path, "N/A"))
    results.append(("DFS", dfs_path, "N/A"))
    results.append(("UCS", ucs_path, ucs_cost))
    results.append(("A*", astar_path, astar_cost))

    print("\n--- Search Algorithm Comparison ---")
    print("Algorithm | Path | Cost | Nodes Explored")
    print("----------|------|------|--------------")
    for name, path, cost in results:
        print(f"{name:<10} | {'->'.join(path)} | {cost} | N/A")

    if astar_cost != float("inf"):
        print("\nBest algorithm for shortest path: A*")


if __name__ == "__main__":
    main()
