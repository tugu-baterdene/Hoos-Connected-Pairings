from pairing_logic import generate_pairings
from pairing_logic.csv_loader import load_students_from_csv
from pairing_logic.csv_writer import write_pairings_to_csv

students = load_students_from_csv("example_data/students1.csv")

pairings = generate_pairings(students)

print("\nFinal Pairings:\n")

for pair in pairings:
    print(
        f"{pair['student1']} ↔ {pair['student2']} "
        f"(Score: {pair['score']})"
    )

    print("Shared Availability:")
    for day, times in pair["shared_times"].items():
        print(f"  {day}: {', '.join(times)}")

    print()
    
write_pairings_to_csv(pairings, "output/pairings_output.csv")

print("\nPairings have been written to output/pairings_output.csv")