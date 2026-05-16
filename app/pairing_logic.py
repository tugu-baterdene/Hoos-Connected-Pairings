from itertools import combinations
import networkx as nx
from app.config import WEIGHTS

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


def compatibility(s1, s2, weights):
    overlap = overlap_score(s1, s2)

    if overlap == 0:
        return -999  # impossible pair

    return (
        overlap * weights["overlap"]
        + experience_score(s1, s2) * weights["experience"]
        + confidence_score(s1, s2) * weights["confidence"]
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


def student_key(student):

    return student.get("student_id", student["name"])


def generate_pairings(students, weights=None):

    if weights is None:
        weights = WEIGHTS

    G = nx.Graph()

    students_by_id = {
        student_key(student): student
        for student in students
    }

    G.add_nodes_from(students_by_id)

    # Add weighted edges
    for s1, s2 in combinations(students, 2):

        score = compatibility(s1, s2, weights)

        if score > 0:

            G.add_edge(
                student_key(s1),
                student_key(s2),
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

        s1 = students_by_id[n1]
        s2 = students_by_id[n2]

        details = detailed_breakdown(
            s1,
            s2,
            weights
        )

        final_pairs.append({
            "student1_id": n1,
            "student2_id": n2,
            "student1": s1["name"],
            "student2": s2["name"],
            "score": score,
            "shared_times": details["shared_times"],
            "overlap_points": details["overlap_points"],
            "experience_points": details["experience_points"],
            "confidence_points": details["confidence_points"],
            "experience_balanced": details["experience_balanced"],
            "confidence_gap": details["confidence_gap"]
        })

    return final_pairs

def detailed_breakdown(s1, s2, weights):

    overlap = overlap_score(s1, s2)

    experience = experience_score(s1, s2)

    confidence = confidence_score(s1, s2)

    return {

        "overlap_points":
            overlap * weights["overlap"],

        "experience_points":
            experience * weights["experience"],

        "confidence_points":
            confidence * weights["confidence"],

        "shared_times":
            shared_availability(s1, s2),

        "experience_balanced":
            s1["facilitated_before"]
            !=
            s2["facilitated_before"],

        "confidence_gap":
            abs(
                s1["confidence"]
                -
                s2["confidence"]
            )
    }
