from pairing_logic import generate_pairings


students = [
    {
        "name": "Alice",
        "availability": {
            "Mon": ["6PM", "7PM"],
            "Wed": ["5PM"]
        },
        "facilitated_before": True,
        "confidence": 5
    },

    {
        "name": "Bob",
        "availability": {
            "Mon": ["7PM"],
            "Wed": ["5PM"]
        },
        "facilitated_before": False,
        "confidence": 2
    },

    {
        "name": "Charlie",
        "availability": {
            "Mon": ["6PM"],
            "Tue": ["4PM"]
        },
        "facilitated_before": False,
        "confidence": 1
    },

    {
        "name": "Diana",
        "availability": {
            "Mon": ["6PM", "7PM"],
            "Wed": ["5PM"]
        },
        "facilitated_before": True,
        "confidence": 4
    }
]


pairings = generate_pairings(students)

print("\nFinal Pairings:\n")

for pair in pairings:
    print(
        f"{pair['student1']} ↔ {pair['student2']} "
        f"(Score: {pair['score']})"
    )