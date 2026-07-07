import heapq


def a_star(graph, start, goal, heuristic):
    open_list = []
    visited = []
    heapq.heappush(open_list, (heuristic[start], 0, start, [start]))

    while open_list:
        f, g, current, path = heapq.heappop(open_list)
        if current == goal:
            return path, g
        if current in visited:
            continue
        visited.append(current)

        for neighbor, cost in graph[current].items():
            if neighbor not in visited:
                g_new = g + cost
                f_new = g_new + heuristic[neighbor]
                heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))

    return None, float("inf")


def main():
    graph = {
        "A": {"B": 4, "C": 7},
        "B": {"D": 3, "E": 5},
        "C": {"F": 2, "G": 6},
        "D": {"H": 4},
        "E": {"H": 2, "I": 3},
        "F": {"I": 5},
        "G": {"J": 4},
        "H": {"J": 2},
        "I": {"J": 1},
        "J": {},
    }
    heuristic = {"A": 8, "B": 5, "C": 6, "D": 4, "E": 3, "F": 5, "G": 4, "H": 2, "I": 1, "J": 0}

    path, cost = a_star(graph, "A", "J", heuristic)
    print(f"Optimal route: {path}")
    print(f"Total cost: {cost}")


if __name__ == "__main__":
    main()
