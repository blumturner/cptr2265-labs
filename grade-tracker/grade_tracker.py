import json

DATA_FILE = "grades.json"


def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(courses, file, indent=4)

    print("Data saved.")


courses = load_data()


def add_course():
    course_name = input("Enter course name: ").strip()

    if not course_name:
        print("Course name cannot be empty.")
        return

    if course_name in courses:
        print("Course already exists.")
        return

    courses[course_name] = {
        "assignments": {}
    }

    print(f"Course '{course_name}' added.")


def remove_course():
    course_name = input("Enter course name to remove: ").strip()

    if course_name not in courses:
        print("Course not found.")
        return

    del courses[course_name]
    print(f"Course '{course_name}' removed.")


def add_assignment():
    course_name = input("Enter course name: ").strip()

    if course_name not in courses:
        print("Course not found.")
        return

    assignment_name = input("Enter assignment name: ").strip()

    if not assignment_name:
        print("Assignment name cannot be empty.")
        return

    if assignment_name in courses[course_name]["assignments"]:
        print("Assignment already exists.")
        return

    courses[course_name]["assignments"][assignment_name] = None

    print(f"Assignment '{assignment_name}' added.")


def edit_assignment():
    course_name = input("Enter course name: ").strip()

    if course_name not in courses:
        print("Course not found.")
        return

    old_name = input("Enter assignment name to edit: ").strip()

    if old_name not in courses[course_name]["assignments"]:
        print("Assignment not found.")
        return

    new_name = input("Enter new assignment name: ").strip()

    if not new_name:
        print("Assignment name cannot be empty.")
        return

    if new_name in courses[course_name]["assignments"]:
        print("An assignment with that name already exists.")
        return

    grade = courses[course_name]["assignments"].pop(old_name)
    courses[course_name]["assignments"][new_name] = grade

    print(f"Assignment renamed to '{new_name}'.")


def enter_grade():
    course_name = input("Enter course name: ").strip()

    if course_name not in courses:
        print("Course not found.")
        return

    assignment_name = input("Enter assignment name: ").strip()

    if assignment_name not in courses[course_name]["assignments"]:
        print("Assignment not found.")
        return

    try:
        grade = float(input("Enter grade (0-100): "))

        if grade < 0 or grade > 100:
            print("Grade must be between 0 and 100.")
            return

        courses[course_name]["assignments"][assignment_name] = grade

        print(f"Grade of {grade} entered for '{assignment_name}'.")

    except ValueError:
        print("Please enter a valid number.")


def view_courses():
    if not courses:
        print("No courses found.")
        return

    for course_name, course_data in courses.items():
        print(f"\nCourse: {course_name}")

        assignments = course_data["assignments"]

        if not assignments:
            print("  No assignments.")
            continue

        for assignment_name, grade in assignments.items():
            if grade is None:
                print(f"  {assignment_name}: Not graded")
            else:
                print(f"  {assignment_name}: {grade}")


def main():
    while True:
        print("\n===== GRADE TRACKER =====")
        print("1. Add Course")
        print("2. Remove Course")
        print("3. Add Assignment")
        print("4. Edit Assignment")
        print("5. Enter Grade")
        print("6. View Courses")
        print("7. Save and Exit")
        print("8. Exit Without Saving")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_course()
        elif choice == "2":
            remove_course()
        elif choice == "3":
            add_assignment()
        elif choice == "4":
            edit_assignment()
        elif choice == "5":
            enter_grade()
        elif choice == "6":
            view_courses()
        elif choice == "7":
            save_data()
            print("Goodbye!")
            break
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()