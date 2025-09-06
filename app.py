from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'events.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    type = db.Column(db.String, default='Workshop')
    date = db.Column(db.String)
    capacity = db.Column(db.Integer, default=0)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'))
    present = db.Column(db.Boolean, default=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'))
    rating = db.Column(db.Integer)  # 1-5

with app.app_context():
    db.create_all()

# Home Page
@app.route('/')
def index():
    return render_template('home.html')

# Create Event
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        type_ = request.form['type']
        date = request.form['date']
        capacity = int(request.form['capacity'])
        event = Event(title=title, type=type_, date=date, capacity=capacity)
        db.session.add(event)
        db.session.commit()
        return render_template('create_event.html', success=True)
    return render_template('create_event.html')

# Existing Events / Student Registration
@app.route('/events', methods=['GET', 'POST'])
def events():
    events_list = Event.query.all()
    message = None
    if request.method == 'POST':
        # Register student
        name = request.form['name']
        email = request.form['email']
        event_id = int(request.form['event_id'])
        student = Student.query.filter_by(email=email).first()
        if not student:
            student = Student(name=name, email=email)
            db.session.add(student)
            db.session.commit()
        # Check duplicate registration
        reg = Registration.query.filter_by(student_id=student.id, event_id=event_id).first()
        if not reg:
            reg = Registration(student_id=student.id, event_id=event_id)
            db.session.add(reg)
            db.session.commit()
            message = f"{student.name} registered successfully!"
    # Load registrations for display
    registrations = Registration.query.all()
    reg_data = []
    for r in registrations:
        student = Student.query.get(r.student_id)
        event = Event.query.get(r.event_id)
        att = Attendance.query.filter_by(registration_id=r.id).first()
        fb = Feedback.query.filter_by(registration_id=r.id).first()
        reg_data.append({
            'reg_id': r.id,
            'student_name': student.name,
            'student_email': student.email,
            'event_title': event.title,
            'attendance': att.present if att else None,
            'feedback': fb.rating if fb else None
        })
    return render_template('events.html', events=events_list, reg_data=reg_data, message=message)

# Mark attendance (admin)
@app.route('/mark_attendance/<int:reg_id>', methods=['POST'])
def mark_attendance(reg_id):
    att = Attendance.query.filter_by(registration_id=reg_id).first()
    if not att:
        att = Attendance(registration_id=reg_id, present=True)
        db.session.add(att)
    else:
        att.present = True
    db.session.commit()
    return ('', 204)

# Submit feedback (student)
@app.route('/submit_feedback/<int:reg_id>', methods=['POST'])
def submit_feedback(reg_id):
    rating = int(request.form['rating'])
    fb = Feedback.query.filter_by(registration_id=reg_id).first()
    if not fb:
        fb = Feedback(registration_id=reg_id, rating=rating)
        db.session.add(fb)
    else:
        fb.rating = rating
    db.session.commit()
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
