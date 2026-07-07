from typing import Dict, Tuple

# A dictionary-based graph representing a city with 10 nodes.
# Keys are node names, values are dictionaries of {neighbor: edge_weight}
CITY_GRAPH: Dict[str, Dict[str, float]] = {
    "A": {"B": 4.0, "C": 2.0},
    "B": {"A": 4.0, "D": 5.0, "E": 12.0},
    "C": {"A": 2.0, "F": 10.0, "G": 4.0},
    "D": {"B": 5.0, "H": 7.0},
    "E": {"B": 12.0, "I": 2.0},
    "F": {"C": 10.0, "I": 6.0},
    "G": {"C": 4.0, "H": 3.0},
    "H": {"D": 7.0, "G": 3.0, "J": 5.0},
    "I": {"E": 2.0, "F": 6.0, "J": 4.0},
    "J": {"H": 5.0, "I": 4.0}
}

# Heuristic dictionary (Estimated distance to Goal 'J')
# In a real-world scenario, this might be straight-line distance.
HEURISTICS: Dict[str, float] = {
    "A": 10.0,
    "B": 8.0,
    "C": 9.0,
    "D": 6.0,
    "E": 4.0,
    "F": 5.0,
    "G": 6.0,
    "H": 3.0,
    "I": 2.0,
    "J": 0.0
}
