
# Campus Event Reporting Prototype (Flask)

**Important:** The assignment's README requested must be *written personally* by you (the student). 
I have added a README template below; please edit the "My understanding" section in your own words before submission.

## What I built
- A small Flask app with SQLite storing colleges, events, students, registrations, attendance, and feedback.
- APIs to create events, register students, mark attendance, submit feedback.
- Reporting endpoints: registrations, attendance percentage, average feedback, event popularity, student participation, top 3 active students.

## Quick start (run locally)
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   python app.py
   ```
   The app will start on `http://127.0.0.1:5000/`.
3. The SQLite DB `events.db` will be created automatically on first run with sample data.

## API examples
- Create event:
  `POST /api/events` JSON body: `{"title":"New Event","type":"Workshop","date":"2025-09-20","capacity":100}`
- Register:
  `POST /api/register` JSON: `{"name":"Charlie","email":"charlie@example.com","event_id":1}`
- Mark attendance:
  `POST /api/attendance` JSON: `{"registration_id":1,"present":true}`
- Feedback:
  `POST /api/feedback` JSON: `{"registration_id":1,"rating":5}`

## Reports (GET)
- `/api/reports/registrations`
- `/api/reports/attendance/<event_id>`
- `/api/reports/avg_feedback/<event_id>`
- `/api/reports/event_popularity`
- `/api/reports/student_participation`
- `/api/reports/top_active_students`

## My understanding (PLEASE EDIT)
*(Write this part in your own words — do not paste AI-generated content)*
- Explain what the system does, assumptions you made, and any deviations from the brief.

## Notes
- The assignment requires that the README be your own writing. I generated the code and scaffolding for you — please fill the personal sections before submission.
