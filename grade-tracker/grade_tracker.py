courses = {}


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


def main():
    while True:
        print("\n===== GRADE TRACKER =====")
        print("1. Add Course")
        print("2. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_course()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()