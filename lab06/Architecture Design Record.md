Architecture Design Record

I decided to use a Layered Architecture for the Student Grade Tracker. The system will have three main layers: the Presentation Layer, Business Logic Layer, and Data Access Layer. The Presentation Layer will handle the user interface, the Business Logic Layer will handle courses, assignments, grades, and calculations, and the Data Access Layer will handle saving and loading data.

I chose this architecture because the Student Grade Tracker is a small system and does not need a complicated design. Separating the system into layers will keep the different responsibilities organized and make the program easier to understand and maintain.

I considered using MVC, but I decided that it would add some structure that is not necessary for this small project. I also considered Microservices, but having multiple separate services would make the project more complicated than it needs to be. Event Driven Architecture was another option, but the grade tracker does not need different parts of the system to communicate through events.

The main advantage of using a Layered Architecture is that each part of the system has a specific responsibility. This makes the system easier to change and maintain. A disadvantage is that information has to move through multiple layers, which can add some extra processing. For this project, that small trade-off is worth it because the system is simple and does not need the complexity of other architectures.



NFR 1 — Usability
The system shall be easy for a new user to use without needing additional instructions. The Presentation Layer supports this requirement by keeping user interaction separate from the rest of the application. This makes it easier to organize the interface and change how users enter and view information without changing the grade calculation or data storage logic.

NFR 2 — Performance
The system shall update grades and calculations within a couple of seconds. The Layered Architecture supports this requirement by keeping the system simple and avoiding unnecessary network communication between separate services. Since the Student Grade Tracker is a small application, using one application with organized layers should provide enough performance without the overhead of microservices.

NFR 3 — Reliability
The system shall correctly save user data so that information is not lost when the application is closed. The Data Access Layer is responsible for saving and loading the student's data, giving the system one dedicated part for handling storage. Separating data storage from the other layers makes it easier to test and maintain the code responsible for saving and retrieving information.
