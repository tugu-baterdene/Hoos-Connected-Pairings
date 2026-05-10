from itertools import combinations
import networkx as nx

# Algorithm for pairing students based on:
#  - Availability overlap (3 points per overlapping time slot)
#  - Experience difference (4 points if one has facilitated before and the other hasn't)
#  - Confidence difference (2 points per confidence level difference)
# Pairs with no availability overlap are considered impossible and given a very low score to ensure they are not paired together.

def overlap_score(s1, s2):
    score = 0
    for day in s1["availability"]:
        if day in s2["availability"]:
            overlap = set(s1["availability"][day]) & set(s2["availability"][day])
            score += len(overlap)
    return score


def experience_score(s1, s2):
    if s1["facilitated_before"] != s2["facilitated_before"]:
        return 5
    return 0


def confidence_score(s1, s2):
    return abs(s1["confidence"] - s2["confidence"])


def compatibility(s1, s2):
    overlap = overlap_score(s1, s2)

    if overlap == 0:
        return -999  # impossible pair

    return (
        overlap * 3
        + experience_score(s1, s2) * 4
        + confidence_score(s1, s2) * 2
    )

def shared_availability(s1, s2):

    shared = {}

    for day in s1["availability"]:

        if day in s2["availability"]:

            overlap = (
                set(s1["availability"][day])
                & set(s2["availability"][day])
            )

            if overlap:
                shared[day] = list(overlap)

    return shared

def generate_pairings(students):
    G = nx.Graph()

    # Add weighted edges
    for s1, s2 in combinations(students, 2):

        score = compatibility(s1, s2)

        print(f"Compatibility between {s1['name']} and {s2['name']}: {score}")

        if score > 0:

            G.add_edge(
                s1["name"],
                s2["name"],
                weight=score
            )

    

    # Compute optimal matching
    matching = nx.max_weight_matching(
        G,
        maxcardinality=True
    )

    final_pairs = []

    for n1, n2 in matching:

        score = G[n1][n2]["weight"]

        s1 = next(s for s in students if s["name"] == n1)
        s2 = next(s for s in students if s["name"] == n2)

        final_pairs.append({
            "student1": n1,
            "student2": n2,
            "score": score,
            "shared_times": shared_availability(s1, s2)
        })

    return final_pairs

