import csv
import re

# Parses the availability string from the CSV into a dictionary format.

DAY_COLUMNS = {
    "monday": "Monday",
    "mon": "Mon",
    "tuesday": "Tuesday",
    "tue": "Tue",
    "wednesday": "Wednesday",
    "wed": "Wed",
    "thursday": "Thursday",
    "thu": "Thu",
    "friday": "Friday",
    "fri": "Fri",
    "saturday": "Saturday",
    "sat": "Sat",
    "sunday": "Sunday",
    "sun": "Sun",
}

STUDENT_ID_COLUMNS = [
    "student_id",
    "studentid",
    "id",
    "uva_id",
    "computing_id",
    "net_id",
    "email",
]


def normalize_key(key):

    return key.strip().lower().replace(" ", "_")


def parse_time_values(value):

    return [
        time.strip()
        for time in re.split(r"[|;,]", value)
        if time.strip()
    ]


def parse_availability(avail_string):

    availability = {}

    if not avail_string:
        return availability

    days = avail_string.split(";")

    for day_entry in days:

        if not day_entry.strip():
            continue

        if ":" not in day_entry:
            raise ValueError(
                "Availability entries must look like 'Monday:6PM|7PM'"
            )

        day, times = day_entry.split(":", 1)

        parsed_times = parse_time_values(times)

        if parsed_times:
            availability[day.strip()] = parsed_times

    return availability


def parse_day_columns(row):

    availability = {}

    for column, day_name in DAY_COLUMNS.items():

        times = parse_time_values(row.get(column, ""))

        if times:
            availability[day_name] = times

    return availability


def get_required_value(row, key, row_number):

    value = row.get(key, "")

    if value == "":
        raise ValueError(
            f"Row {row_number} is missing required column '{key}'."
        )

    return value


def parse_bool(value):

    return value.strip().lower() in {"true", "yes", "y", "1"}


def get_student_id(row, name, row_number):

    for key in STUDENT_ID_COLUMNS:

        if row.get(key):
            return row[key]

    fallback_name = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    return f"row-{row_number - 1}-{fallback_name}"


def load_students_from_csv(filename):

    students = []

    with open(filename, newline="", encoding="utf-8-sig") as csvfile:

        reader = csv.DictReader(csvfile)

        for row_number, row in enumerate(reader, start=2):

            normalized_row = {
                normalize_key(key): (value or "").strip()
                for key, value in row.items()
                if key is not None
            }

            if normalized_row.get("availability"):
                availability = parse_availability(
                    normalized_row["availability"]
                )
            else:
                availability = parse_day_columns(normalized_row)

            if not availability:
                raise ValueError(
                    f"Row {row_number} is missing availability data. "
                    "Use either an 'availability' column or day columns "
                    "like 'Monday', 'Tuesday', and 'Wednesday'."
                )

            confidence = get_required_value(
                normalized_row,
                "confidence",
                row_number
            )

            name = get_required_value(
                normalized_row,
                "name",
                row_number
            )

            students.append({
                "student_id": get_student_id(
                    normalized_row,
                    name,
                    row_number
                ),
                "name": name,
                "facilitated_before":
                    parse_bool(
                        get_required_value(
                            normalized_row,
                            "facilitated_before",
                            row_number
                        )
                    ),

                "confidence": int(confidence),

                "availability":
                    availability
            })

    return students
