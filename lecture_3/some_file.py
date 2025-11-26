from typing import List, Dict, Optional

students: List[Dict[str, any]] = []


def display_menu() -> None:
    """Display the main menu options."""
    print("\n--- Student Grade Analyzer ---")
    print("1. Add a new student")
    print("2. Add grades for a student")
    print("3. Generate a full report")
    print("4. Find the top student")
    print("5. Exit program")


def add_new_student() -> None:
    """Add a new student to the system."""
    name = input("Enter student name: ").strip()

    # Check if student already exists
    for student in students:
        if student["name"].lower() == name.lower():
            print(f"Student '{name}' already exists!")
            return

    # Add new student
    students.append({"name": name, "grades": []})


def add_grades_for_student() -> None:
    """Add grades for an existing student."""
    name = input("Enter student name: ").strip()

    # Find student
    student_found: Optional[Dict[str, any]] = None
    for student in students:
        if student["name"].lower() == name.lower():
            student_found = student
            break

    if not student_found:
        print(f"Student '{name}' not found!")
        return

    # Add grades
    while True:
        grade_input = input("Enter a grade (or 'done' to finish): ").strip()

        if grade_input.lower() == 'done':
            break

        try:
            grade = int(grade_input)
            if 0 <= grade <= 100:
                student_found["grades"].append(grade)
            else:
                print("Grade must be between 0 and 100!")
        except ValueError:
            print("Invalid input. Please enter a number.")


def generate_full_report() -> None:
    """Generate a report with all students and statistics."""
    if not students:
        print("No students available!")
        return

    print("\n--- Student Report ---")

    averages: List[float] = []

    for student in students:
        name = student["name"]
        grades: List[int] = student["grades"]

        try:
            average = sum(grades) / len(grades)
            averages.append(average)
            print(f"{name}'s average grade is {average:.1f}.")
        except ZeroDivisionError:
            print(f"{name}'s average grade is N/A.")

    # Calculate overall statistics
    if averages:
        print("---")
        print(f"Max Average: {max(averages):.1f}")
        print(f"Min Average: {min(averages):.1f}")
        print(f"Overall Average: {sum(averages) / len(averages):.1f}")


def find_top_student() -> None:
    """Find the student with the highest average grade."""
    if not students:
        print("No students available!")
        return

    # Filter students with grades
    students_with_grades = [s for s in students if s["grades"]]

    if not students_with_grades:
        print("No students with grades available!")
        return

    # Use max with lambda function to find top performer
    top_student = max(students_with_grades,
                      key=lambda s: sum(s["grades"]) / len(s["grades"]))

    top_average = sum(top_student["grades"]) / len(top_student["grades"])
    print(f"The student with the highest average is {top_student['name']} with a grade of {top_average:.1f}.")


def main() -> None:
    """Main program loop."""
    while True:
        try:
            display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                add_new_student()
            elif choice == '2':
                add_grades_for_student()
            elif choice == '3':
                generate_full_report()
            elif choice == '4':
                find_top_student()
            elif choice == '5':
                print("Exiting program.")
                break
            else:
                print("Invalid choice! Please enter a number between 1-5.")

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()