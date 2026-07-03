def dls(graph, node, goal, limit):
    if node == goal:
        return True
    if limit <= 0:
        return False
    for neighbor in graph.get(node, []):
        if dls(graph, neighbor, goal, limit - 1):
            return True
    return False


def ids(graph, start, goal):
    depth = 0
    iterations = 0
    while True:
        iterations += 1
        print(f"Searching at depth {depth}")
        if dls(graph, start, goal, depth):
            print(f"Goal found at depth {depth}")
            print(f"Total iterations: {iterations}")
            return
        depth += 1


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
    ids(graph, "A", "G")


if __name__ == "__main__":
    main()
