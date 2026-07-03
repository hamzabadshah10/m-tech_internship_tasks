import heapq


def a_star(graph, start, goal, heuristic):
    open_list = []
    visited = []

    heapq.heappush(open_list, (heuristic[start], 0, start, [start]))

    while open_list:
        f, g, current, path = heapq.heappop(open_list)

        if current == goal:
            print("Goal reached")
            return path, g

        if current in visited:
            continue
        visited.append(current)

        print(f"Visiting {current} | f={f} | g={g} | h={heuristic[current]}")

        for neighbor, cost in graph[current].items():
            if neighbor not in visited:
                g_new = g + cost
                f_new = g_new + heuristic[neighbor]
                heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))

    return None, float("inf")


def main():
    graph = {
        "S": {"A": 2, "B": 5},
        "A": {"C": 4, "D": 7},
        "B": {"D": 3, "E": 6},
        "C": {"F": 5},
        "D": {"F": 2, "G": 3},
        "E": {"G": 1},
        "F": {"H": 3},
        "G": {"H": 2},
        "H": {},
    }
    heuristic = {"S": 10, "A": 8, "B": 7, "C": 6, "D": 4, "E": 3, "F": 2, "G": 1, "H": 0}

    path, cost = a_star(graph, "S", "H", heuristic)
    print(f"Path: {path}, Cost: {cost}")


if __name__ == "__main__":
    main()
