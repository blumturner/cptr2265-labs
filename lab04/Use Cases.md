Use Cases


Use Case 1 — Add Course
Name: Add Course

Actors: Student/User

Preconditions:
The Student Grade Tracker is running.
The user is able to access the course management functions.

Main Flow:
The user selects the option to add a course.
The system asks the user to enter the course name.
The user enters the course name.
The system creates the new course.
The system displays the new course in the user's course list.

Alternate Flows:
If the user leaves the course name blank, the system shall display an error message.
If the course already exists, the system shall notify the user and not create a duplicate course.

Postconditions:
The new course is stored in the user's course list.





Use Case 2 — Enter Grade
Name: Enter Grade

Actors:Student/User

Preconditions:
The Student Grade Tracker is running.
At least one course exists.
An assignment exists for the selected course.

Main Flow:
The user selects a course.
The user selects an assignment.
The system asks the user to enter a grade.
The user enters the grade.
The system checks that the grade is valid.
The system stores the grade.
The system updates the course average.

Alternate Flows:
If the grade is outside the allowed range, the system shall display an error message.
If the selected assignment does not exist, the system shall notify the user.
If the user enters invalid information, the system shall ask the user to enter the grade again.

Postconditions:
The assignment has the new grade.
The course average is updated.




Use Case 3 — Save User Data
Name: Save User Data

Actors: Student/User

Preconditions:
The Student Grade Tracker is running.
The user has course, assignment, or grade information to save.

Main Flow:
The user selects the save option.
The system collects the user's course, assignment, and grade information.
The system saves the information to storage.
The system confirms that the data was saved successfully.

Alternate Flows:
If the data cannot be saved, the system shall display an error message.
If there is no information to save, the system shall notify the user.

Postconditions:
The user's current course, assignment, and grade information is saved.