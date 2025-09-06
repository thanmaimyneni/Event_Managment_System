from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'events.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret')  # Needed for sessions
db = SQLAlchemy(app)

# ===============================
# MODELS
# ===============================
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

# ===============================
# ROLE-BASED ACCESS CONTROL
# ===============================
def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get('role') in roles:
                return f(*args, **kwargs)
            return abort(403)
        return wrapper
    return decorator

# ===============================
# AUTH ROUTES
# ===============================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mode = request.form.get('mode')

        if mode == 'admin':
            pwd = request.form.get('password', '')
            admin_pwd = os.environ.get('ADMIN_PASSWORD', 'admin123')
            if pwd == admin_pwd:
                session['role'] = 'admin'
                flash('Logged in as Admin', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid admin password', 'danger')

        elif mode == 'student':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            if name and email:
                session['role'] = 'student'
                session['student_name'] = name
                session['student_email'] = email
                flash('Logged in as Student', 'success')
                return redirect(url_for('events'))
            else:
                flash('Provide both name and email', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('index'))

# ===============================
# MAIN ROUTES
# ===============================
@app.route('/')
def index():
    return render_template('home.html')

@require_role('admin')
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

@app.route('/events', methods=['GET', 'POST'])
def events():
    events_list = Event.query.all()
    message = None
    if request.method == 'POST':
        # Require student role
        if session.get('role') != 'student':
            return abort(403)

        name = session.get('student_name')
        email = session.get('student_email')
        event_id = int(request.form['event_id'])

        student = Student.query.filter_by(email=email).first()
        if not student:
            student = Student(name=name, email=email)
            db.session.add(student)
            db.session.commit()

        # Prevent duplicate registration
        reg = Registration.query.filter_by(student_id=student.id, event_id=event_id).first()
        if not reg:
            reg = Registration(student_id=student.id, event_id=event_id)
            db.session.add(reg)
            db.session.commit()
            message = f"{student.name} registered successfully!"

    # Load registrations
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

@require_role('admin')
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

@require_role('student')
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

# ===============================
# RUN
# ===============================
if __name__ == '__main__':
    app.run(debug=True)
