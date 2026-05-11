import csv

# Parses the availability string from the CSV into a dictionary format.

def parse_availability(avail_string):

    availability = {}

    days = avail_string.split(";")

    for day_entry in days:

        day, times = day_entry.split(":")

        availability[day] = times.split("|")

    return availability


def load_students_from_csv(filename):

    students = []

    with open(filename, newline="") as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            students.append({
                "name": row["name"],
                "facilitated_before":
                    row["facilitated_before"] == "True",

                "confidence": int(row["confidence"]),

                "availability":
                    parse_availability(row["availability"])
            })

    return students