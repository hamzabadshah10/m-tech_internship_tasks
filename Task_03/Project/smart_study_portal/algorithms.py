import heapq
from typing import Dict, List, Tuple
from collections import deque

def bfs(graph: Dict[str, Dict[str, float]], start: str, goal: str) -> Tuple[List[str], float, int]:
    """Breadth-First Search Algorithm."""
    if start not in graph or goal not in graph:
        return ([], 0.0, 0)

    queue = deque([(start, [start], 0.0)])
    visited = set()
    nodes_explored = 0

    while queue:
        node, path, cost = queue.popleft()

        if node in visited:
            continue
            
        visited.add(node)
        nodes_explored += 1

        if node == goal:
            return (path, cost, nodes_explored)

        for neighbor, edge_weight in graph.get(node, {}).items():
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor], cost + edge_weight))

    return ([], 0.0, nodes_explored)


def ucs(graph: Dict[str, Dict[str, float]], start: str, goal: str) -> Tuple[List[str], float, int]:
    """Uniform Cost Search Algorithm."""
    if start not in graph or goal not in graph:
        return ([], 0.0, 0)

    pq = [(0.0, start, [start])]
    visited = set()
    nodes_explored = 0

    while pq:
        cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue
            
        visited.add(node)
        nodes_explored += 1

        if node == goal:
            return (path, cost, nodes_explored)

        for neighbor, edge_weight in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(pq, (cost + edge_weight, neighbor, path + [neighbor]))

    return ([], 0.0, nodes_explored)


def a_star(graph: Dict[str, Dict[str, float]], start: str, goal: str, heuristics: Dict[str, float]) -> Tuple[List[str], float, int]:
    """A* Search Algorithm (f(n) = g(n) + h(n))."""
    if start not in graph or goal not in graph:
        return ([], 0.0, 0)

    # Priority Queue stores tuples of: (f_cost, g_cost, node, path)
    pq = [(heuristics.get(start, 0.0), 0.0, start, [start])]
    visited = set()
    nodes_explored = 0

    while pq:
        f_cost, g_cost, node, path = heapq.heappop(pq)

        if node in visited:
            continue
            
        visited.add(node)
        nodes_explored += 1

        if node == goal:
            return (path, g_cost, nodes_explored)

        for neighbor, edge_weight in graph.get(node, {}).items():
            if neighbor not in visited:
                new_g_cost = g_cost + edge_weight
                new_f_cost = new_g_cost + heuristics.get(neighbor, 0.0)
                heapq.heappush(pq, (new_f_cost, new_g_cost, neighbor, path + [neighbor]))

    return ([], 0.0, nodes_explored)
