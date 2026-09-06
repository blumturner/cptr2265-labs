System Design

Major Components:
User Interface Module - Provides the screens and controls that the user interacts with. 
The user can create courses, add assignments, enter grades, and view course averages.

Course Management Module - Handles creating, editing, and deleting courses. 
It also maintains the list of courses available to the user.

Assignment Management Module - Handles adding, editing, and deleting assignments within a selected course.
It stores the assignment name and grade information.

Grade Calculation Module - Calculates assignment percentages and course averages
 using the grades stored in the system.

Data Storage Module - Stores and retrieves courses, assignments, and grade information so that data remains 
available after the application is closed.

Data Flow can be shown like this
User Interface -> Management Modules -> Grade Calculation/Data Storage -> User Interface 
