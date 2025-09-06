
# Design Document (brief)

## Data to Track
- Event creation (id, title, type, date, capacity, college_id)
- Student (id, name, email, college_id)
- Registration (id, student_id, event_id, timestamp)
- Attendance (registration_id, present)
- Feedback (registration_id, rating 1-5)

## Database Schema (tables)
- College(id, name)
- Event(id, college_id, title, type, date, capacity)
- Student(id, college_id, name, email)
- Registration(id, student_id, event_id, created_at)
- Attendance(id, registration_id, present)
- Feedback(id, registration_id, rating)

## API Design
- POST /api/events -> create event
- POST /api/register -> register student
- POST /api/attendance -> mark attendance
- POST /api/feedback -> submit feedback
- GET /api/reports/* -> reports

## Workflows
- Registration -> creates Student (if not exists) and Registration record
- Attendance -> marks Attendance.present for a registration
- Feedback -> attaches rating to a registration

## Assumptions & Edge Cases
- Duplicate registrations prevented by checking existing registration
- Feedback optional; average computed only if present
- IDs are global integers; in multi-college setups you might prefix or use UUIDs
