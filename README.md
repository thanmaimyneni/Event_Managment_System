
#### Campus Event Reporting Prototype

This is a Flask-based web application that helps manage events, registrations, feedback, and attendance. The system supports two types of users: Admin and Student, with different access levels.
Features
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Admin

Create and manage events
Mark student attendance
View feedback submitted by students

## Student

Register for events
Submit feedback for attended events

## Tech Stack

Backend: Flask (Python)
Database: SQLite
Frontend: HTML (Jinja2 templates), CSS (custom)
Version Control: Git & GitHub

## Installation & Running Locally

1.Navigate into the project folder:
   cd Event_Managment_System
   
2.Create a virtual environment
   python -m venv venv
   venv\Scripts\activate (for windows)
   
3.Install dependencies
   pip install -r requirements.txt

4.Initialize the database

5.Run the app
   python app.py
   
## webiste link after running app.py

http://127.0.0.1:5000

## Roles

Admin → Can create events and mark attendance
Student → Can register for events and submit feedback

## Future Improvements

User registration & authentication through UI
Export attendance and feedback reports
Email/SMS notifications for event updates
Better UI with responsive design
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Project Structure

Event_Managment_System/
│
├── app.py                 Main Flask application
├── events.db              SQLite database
├── requirements.txt       Project dependencies
├── templates/             HTML templates (Jinja2)
│   ├── index.html
│   ├── login.html
│   ├── create_event.html
│   └── ...
├── static/                CSS, JS, images
└── README.md              Documentation
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## API Endpoints

+-------------------------------------------------------------------------------------------------+
| Endpoint	                             Method	     Role	              Description               |
|-------------------------------------------------------------------------------------------------|
| /login	                                POST       All	         Login with username & password |
| /create_event	                          POST	     Admin	          Create a new event          |
| /register/<event_id>	                  GET	       Student	       Register for an event        |
| /submit_feedback/<event_id>	            POST	     Student	         Submit feedback            |
| /mark_attendance/<event_id>           	GET	       Admin	         Mark student attendance      |
| /<student_id>                                                                                   |                                                                       
---------------------------------------------------------------------------------------------------

   
