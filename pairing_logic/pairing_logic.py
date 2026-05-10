from itertools import combinations

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


def generate_pairings(students):
    all_pairs = []

    for s1, s2 in combinations(students, 2):
        score = compatibility(s1, s2)
        all_pairs.append((score, s1["name"], s2["name"]))

    all_pairs.sort(reverse=True)

    used = set()
    final_pairs = []

    for score, n1, n2 in all_pairs:
        if n1 not in used and n2 not in used and score > 0:
            final_pairs.append({
                "student1": n1,
                "student2": n2,
                "score": score
            })
            
            used.add(n1)
            used.add(n2)

    return final_pairs