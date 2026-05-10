import csv


def write_pairings_to_csv(pairings, filename):

    with open(filename, "w", newline="") as csvfile:

        fieldnames = [
            "student1",
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
            writer.writerow(pair)