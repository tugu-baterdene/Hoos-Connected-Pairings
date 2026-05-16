import csv

def format_shared_times(shared_times):

    formatted = []

    for day, times in shared_times.items():

        formatted.append(
            f"{day}: {', '.join(times)}"
        )

    return " | ".join(formatted)


def write_pairings_to_csv(pairings, filename):

    with open(filename, "w", newline="") as csvfile:

        fieldnames = [
            "student1_id",
            "student1",
            "student2_id",
            "student2",
            "score",
            "shared_times"
        ]

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for pair in pairings:

            writer.writerow({
                "student1_id": pair.get("student1_id", ""),
                "student1": pair["student1"],
                "student2_id": pair.get("student2_id", ""),
                "student2": pair["student2"],
                "score": pair["score"],
                "shared_times":
                    format_shared_times(pair["shared_times"])
            })

    return filename
