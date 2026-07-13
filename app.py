from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token, JWTManager, jwt_required, get_jwt_identity,
)

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from functools import wraps
import json
from flask_caching import Cache
from sqlalchemy import text
from datetime import datetime, date, timedelta   # add timedelta
from flask_mail import Mail, Message
from celery import Celery
from celery.schedules import crontab
from celery.result import AsyncResult

app = Flask(__name__)

from sqlalchemy import func

# allow requests from vue app

CORS(app)
import os
basedir = os.path.abspath(os.path.dirname(__file__))
import csv
import uuid
from flask import Flask, request, jsonify, send_from_directory, send_file
EXPORT_DIR = os.path.join(basedir, "instance", "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)


# sqlite database

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(basedir, "instance", "trekking.db")
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = '@1234'  # Change this to a random secret key
jwt = JWTManager(app)

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_REDIS_DB"] = 0
app.config["CACHE_DEFAULT_TIMEOUT"] = 60 
app.config["CACHE_KEY_PREFIX"] = "tma_cache_"

cache = Cache(app)


# Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "06aditya10sharma@gmail.com"      # change this
app.config["MAIL_PASSWORD"] = "dcgb zzno lmay mzur" #password
app.config["MAIL_DEFAULT_SENDER"] = "06aditya10sharma@gmail.com"

# Email address where monthly admin report will be sent
app.config["ADMIN_REPORT_EMAIL"] = "06aditya10sharma@gmail.com"

mail = Mail(app)
# After any create/update/delete we clear the whole cache so users never

# Flask-Mail (for reminders, reports, export notifications)


def clear_cache():
    # Clear old cached API data after create, update or delete operations.
    try:
        cache.clear()
    except Exception as error:
        print("Cache clear error:", error)


def make_user_cache_key():
    # User id is included because some API responses are different for each user.
    user_id = get_jwt_identity()
    query_data = request.query_string.decode("utf-8")
    return str(user_id) + ":" + request.path + ":" + query_data


def cache_only_success(response):
    # Some routes return response and status code as a tuple
    if isinstance(response, tuple):
        status_code = response[1]

        if status_code == 200:
            return True
        else:
            return False

    
    if response.status_code == 200:
        return True
    else:
        return False == 200
    

from datetime import timedelta

# Celery + Redis (background jobs + daily schedule)
def make_celery(flask_app):
    celery_app = Celery(
        flask_app.import_name,
        broker="redis://localhost:6379/1",
        backend="redis://localhost:6379/1",
    )
    celery_app.conf.update(
        timezone="Asia/Kolkata",
        enable_utc=True,
        beat_schedule={
            "daily-trek-reminder": {
                "task": "send_trek_reminders",
                
                "schedule": crontab(hour=8, minute=0)
            },
            "monthly-admin-report": {
                "task": "send_monthly_admin_report",
                # Run on the first day of every month at 9:00 AM
                "schedule": crontab(day_of_month=1, hour=9, minute=0)
            },
        },
    )

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


celery = make_celery(app)


# creat table user (id int primary key, name varchar(100), email varchar(100), password varchar(100), created_at datetime)
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, staff, user
    full_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='active')  # active, blacklisted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Specific to staff role (added columns programmatically, nullable for admin/users)
    experience = db.Column(db.String(100), nullable=True)
    specialization = db.Column(db.String(200), nullable=True)

    # Relationships
    bookings = db.relationship('booking_table', backref='user', lazy=True, cascade="all, delete-orphan")
    assigned_treks = db.relationship('trekking_table', backref='assigned_staff', lazy=True)


class trekking_table(db.Model):
    __tablename__ = 'treks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Easy, Moderate, Hard
    duration_days = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(20), default='Upcoming')  # Upcoming, Pending, Approved, Open, Closed, Ongoing, Completed
    start_date = db.Column(db.String(20), nullable=False)  # YYYY-MM-DD
    end_date = db.Column(db.String(20), nullable=False)    # YYYY-MM-DD
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('booking_table', backref='trek', lazy=True, cascade="all, delete-orphan")

class booking_table(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Booked')  # Booked, Cancelled, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class feedback_table(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


export_tasks = {}


# Celery background jobs

@celery.task(name="send_trek_reminders")
def send_trek_reminders():
    # This task checks treks starting tomorrow and sends reminder emails.
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    upcoming_treks = trekking_table.query.filter_by(start_date=tomorrow).all()

    sent_count = 0

    for trek in upcoming_treks:
        bookings = booking_table.query.filter_by(
            trek_id=trek.id,
            status='Booked'
        ).all()

        for booking in bookings:
            user = User.query.get(booking.user_id)

            if user and user.email:
                try:
                    message = Message(
                        subject='Trek Reminder - ' + trek.name,
                        recipients=[user.email]
                    )

                    message.body = (
                        'Hello ' + user.full_name + ',\
\
'
                        'This is a reminder that your trek "' + trek.name +
                        '" starts tomorrow.\
'
                        'Location: ' + trek.location + '\
'
                        'Start Date: ' + trek.start_date + '\
'
                        'End Date: ' + trek.end_date + '\
\
'
                        'Please be prepared and reach on time.\
\
'
                        'Trek Journey Team'
                    )

                    mail.send(message)
                    sent_count = sent_count + 1
                except Exception as error:
                    print('Reminder email error:', error)

    return {
        'message': 'Daily reminder task completed',
        'emails_sent': sent_count
    }


@celery.task(name="send_monthly_admin_report")
def send_monthly_admin_report():
    # Report is created for the previous calendar month.
    today = date.today()
    first_day_this_month = today.replace(day=1)
    last_day_previous_month = first_day_this_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)

    start_date = first_day_previous_month.isoformat()
    end_date = last_day_previous_month.isoformat()

    completed_treks = trekking_table.query.filter(
        trekking_table.status == 'Completed',
        trekking_table.end_date >= start_date,
        trekking_table.end_date <= end_date
    ).all()

    completed_trek_ids = [trek.id for trek in completed_treks]

    number_of_participants = 0
    popular_treks = []

    for trek in completed_treks:
        participant_count = booking_table.query.filter_by(
            trek_id=trek.id,
            status='Completed'
        ).count()

        number_of_participants = number_of_participants + participant_count

        popular_treks.append({
            'name': trek.name,
            'participants': participant_count
        })

    popular_treks.sort(
        key=lambda item: item['participants'],
        reverse=True
    )

    popular_rows = ''

    if len(popular_treks) == 0:
        popular_rows = '<tr><td colspan="2">No completed treks in this month</td></tr>'
    else:
        for item in popular_treks[:5]:
            popular_rows = popular_rows + (
                '<tr>'
                '<td style="padding:8px;border:1px solid #ddd;">' +
                item['name'] +
                '</td>'
                '<td style="padding:8px;border:1px solid #ddd;">' +
                str(item['participants']) +
                '</td>'
                '</tr>'
            )

    report_html = (
        '<div style="font-family:Arial,sans-serif;">'
        '<h2>Monthly Trekking Activity Report</h2>'
        '<p><b>Report Period:</b> ' + start_date + ' to ' + end_date + '</p>'
        '<p><b>Number of treks conducted:</b> ' + str(len(completed_treks)) + '</p>'
        '<p><b>Number of participants:</b> ' + str(number_of_participants) + '</p>'
        '<h3>Popular Treks</h3>'
        '<table style="border-collapse:collapse;width:100%;max-width:600px;">'
        '<tr>'
        '<th style="padding:8px;border:1px solid #ddd;text-align:left;">Trek Name</th>'
        '<th style="padding:8px;border:1px solid #ddd;text-align:left;">Participants</th>'
        '</tr>' + popular_rows +
        '</table>'
        '</div>'
    )

    admin_email = app.config.get('ADMIN_REPORT_EMAIL')

    if admin_email:
        try:
            message = Message(
                subject='Monthly Trekking Activity Report',
                recipients=[admin_email]
            )
            message.html = report_html
            mail.send(message)
        except Exception as error:
            print('Monthly report email error:', error)
            return {
                'message': 'Report created but email failed',
                'error': str(error)
            }

    return {
        'message': 'Monthly report sent successfully',
        'treks_conducted': len(completed_treks),
        'participants': number_of_participants,
        'popular_treks': popular_treks[:5]
    }


@celery.task(name="create_trekking_history_csv")
def create_trekking_history_csv(user_id):
    # This task creates the CSV file in the background.
    user = User.query.get(user_id)

    if not user:
        raise ValueError('User not found')

    bookings = booking_table.query.filter_by(user_id=user_id).order_by(
        booking_table.created_at.desc()
    ).all()

    file_name = 'trek_history_' + str(user_id) + '_' + str(uuid.uuid4()) + '.csv'
    file_path = os.path.join(EXPORT_DIR, file_name)

    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            'Trek Name',
            'Location',
            'Start Date',
            'End Date',
            'Difficulty',
            'Booking Date',
            'Status'
        ])

        for booking in bookings:
            trek = trekking_table.query.get(booking.trek_id)

            writer.writerow([
                trek.name if trek else '',
                trek.location if trek else '',
                trek.start_date if trek else '',
                trek.end_date if trek else '',
                trek.difficulty if trek else '',
                booking.booking_date.strftime('%Y-%m-%d'),
                booking.status
            ])

    # Email notification after the CSV is ready.
    if user.email:
        try:
            message = Message(
                subject='Your Trekking History Export is Ready',
                recipients=[user.email]
            )
            message.body = (
                'Hello ' + user.full_name + ',\
\
'
                'Your trekking history CSV export has been completed. '
                'You can download it from the Trek Journey application.\
\
'
                'Trek Journey Team'
            )
            mail.send(message)
        except Exception as error:
            print('CSV notification email error:', error)

    return {
        'user_id': user_id,
        'file_name': file_name,
        'download_url': '/api/user/export-download/' + file_name
    }


@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Trekking API"}), 200


@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name') or data.get('fullName') or ''
    contact_number = data.get('contact_number') or ''

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role='user',
        full_name=full_name,
        contact_number=contact_number,
        status='active'
    )
    db.session.add(user)
    db.session.commit()
    clear_cache()
    return jsonify({"message": "User registered successfully"}), 201


@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User account does not exist"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    if user.status == 'blacklisted':
        return jsonify({"message": "This account is blacklisted. Log in denied."}), 403

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name,
            "contact_number": user.contact_number,
            "status": user.status
        }
    }), 200


@app.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, make_cache_key=make_user_cache_key, response_filter=cache_only_success)
def admin_dashboard():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    recent_bookings = booking_table.query.order_by(booking_table.created_at.desc()).limit(5).all()
    booking_list = []

    for booking in recent_bookings:
        trek = trekking_table.query.get(booking.trek_id)
        booking_user = User.query.get(booking.user_id)
        booking_list.append({
            "id": booking.id,
            "user_name": booking_user.full_name if booking_user else '',
            "user_email": booking_user.email if booking_user else '',
            "trek_name": trek.name if trek else '',
            "trek_location": trek.location if trek else '',
            "trek_start_date": trek.start_date if trek else '',
            "trek_status": trek.status if trek else '',
            "booking_date": booking.booking_date.strftime('%Y-%m-%d'),
            "status": booking.status
        })

    return jsonify({
        "stats": {
            "total_treks": trekking_table.query.count(),
            "total_users": User.query.filter_by(role='user').count(),
            "total_staff": User.query.filter_by(role='staff').count(),
            "total_bookings": booking_table.query.filter_by(status='Booked').count()
        },
        "recent_bookings": booking_list
    }), 200


@app.route('/api/admin/bookings', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, make_cache_key=make_user_cache_key, response_filter=cache_only_success)
def admin_bookings():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    bookings = booking_table.query.order_by(booking_table.created_at.desc()).all()
    booking_list = []

    for booking in bookings:
        trek = trekking_table.query.get(booking.trek_id)
        booking_user = User.query.get(booking.user_id)
        booking_list.append({
            "id": booking.id,
            "user_name": booking_user.full_name if booking_user else '',
            "user_email": booking_user.email if booking_user else '',
            "trek_name": trek.name if trek else '',
            "trek_location": trek.location if trek else '',
            "trek_start_date": trek.start_date if trek else '',
            "trek_status": trek.status if trek else '',
            "booking_date": booking.booking_date.strftime('%Y-%m-%d'),
            "status": booking.status
        })

    return jsonify(booking_list), 200


@app.route('/api/admin/treks', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def admin_get_treks():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    treks = trekking_table.query.order_by(trekking_table.created_at.desc()).all()
    trek_list = []

    for trek in treks:
        staff = User.query.get(trek.assigned_staff_id) if trek.assigned_staff_id else None
        trek_list.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration_days": trek.duration_days,
            "available_slots": trek.available_slots,
            "total_slots": trek.total_slots,
            "assigned_staff_id": trek.assigned_staff_id,
            "assigned_staff_name": staff.full_name if staff else None,
            "status": trek.status,
            "start_date": trek.start_date,
            "end_date": trek.end_date,
            "description": trek.description,
            "image_url": trek.image_url
        })

    return jsonify(trek_list), 200


@app.route('/api/admin/treks', methods=['POST'])
@jwt_required()
def admin_create_trek():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    data = request.get_json()
    name = data.get('name')
    location = data.get('location')
    difficulty = data.get('difficulty')
    duration_days = data.get('duration_days')
    total_slots = data.get('total_slots')
    assigned_staff_id = data.get('assigned_staff_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    description = data.get('description')
    image_url = data.get('image_url')

    if not total_slots or int(total_slots) <= 0:
        return jsonify({"message": "Trek must have at least 1 slot"}), 400

    if start_date <= date.today().isoformat():
        return jsonify({"message": "Trek start date must be after today"}), 400

    duplicate = trekking_table.query.filter_by(
        name=name,
        location=location,
        start_date=start_date
    ).first()

    if duplicate:
        return jsonify({"message": "Duplicate trek already exists with same name, location and start date"}), 400

    if assigned_staff_id:
        existing_treks = trekking_table.query.filter_by(
            assigned_staff_id=assigned_staff_id
        ).all()

        for existing in existing_treks:
            if start_date <= existing.end_date and end_date >= existing.start_date:
                return jsonify({"message": "Staff already assigned to an overlapping trek"}), 400

    trek = trekking_table(
        name=name,
        location=location,
        difficulty=difficulty,
        duration_days=duration_days,
        available_slots=total_slots,
        total_slots=total_slots,
        assigned_staff_id=assigned_staff_id,
        status='Upcoming',
        start_date=start_date,
        end_date=end_date,
        description=description,
        image_url=image_url
    )
    db.session.add(trek)
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Trek created successfully", "data": data}), 201


@app.route('/api/admin/treks/<int:trek_id>', methods=['PUT'])
@jwt_required()
def admin_update_trek(trek_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    trek = trekking_table.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    data = request.get_json()
    name = data.get('name')
    location = data.get('location')
    difficulty = data.get('difficulty')
    duration_days = data.get('duration_days')
    total_slots = data.get('total_slots')
    assigned_staff_id = data.get('assigned_staff_id')
    status = data.get('status')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    description = data.get('description')
    image_url = data.get('image_url')

    if not total_slots or int(total_slots) <= 0:
        return jsonify({"message": "Trek must have at least 1 slot"}), 400

    if start_date <= date.today().isoformat():
        return jsonify({"message": "Trek start date must be after today"}), 400

    duplicate = trekking_table.query.filter(
        trekking_table.name == name,
        trekking_table.location == location,
        trekking_table.start_date == start_date,
        trekking_table.id != trek_id
    ).first()

    if duplicate:
        return jsonify({"message": "Duplicate trek already exists with same name, location and start date"}), 400

    booked_count = booking_table.query.filter_by(trek_id=trek_id, status='Booked').count()

    if int(total_slots) < booked_count:
        return jsonify({"message": "Cannot reduce total slots below current bookings"}), 400

    if assigned_staff_id:
        existing_treks = trekking_table.query.filter(
            trekking_table.assigned_staff_id == assigned_staff_id,
            trekking_table.id != trek_id
        ).all()

        for existing in existing_treks:
            if start_date <= existing.end_date and end_date >= existing.start_date:
                return jsonify({"message": "Staff already assigned to an overlapping trek"}), 400

    trek.name = name
    trek.location = location
    trek.difficulty = difficulty
    trek.duration_days = duration_days
    trek.total_slots = total_slots
    trek.available_slots = int(total_slots) - booked_count
    trek.assigned_staff_id = assigned_staff_id
    trek.status = status
    trek.start_date = start_date
    trek.end_date = end_date
    trek.description = description
    trek.image_url = image_url

    if status == 'Completed':
        active_bookings = booking_table.query.filter_by(trek_id=trek_id, status='Booked').all()
        for active_booking in active_bookings:
            active_booking.status = 'Completed'

    db.session.commit()
    clear_cache()
    return jsonify({"message": "Trek updated successfully"}), 200


@app.route('/api/admin/treks/<int:trek_id>/assign_staff', methods=['PUT'])
@jwt_required()
def assign_staff(trek_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    trek = trekking_table.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    data = request.get_json()
    assigned_staff_id = data.get('assigned_staff_id')

    if assigned_staff_id:
        staff = User.query.get(assigned_staff_id)
        if not staff or staff.role != 'staff':
            return jsonify({"message": "Invalid staff member"}), 400

        existing_treks = trekking_table.query.filter(
            trekking_table.assigned_staff_id == assigned_staff_id,
            trekking_table.id != trek_id
        ).all()

        for existing in existing_treks:
            if trek.start_date <= existing.end_date and trek.end_date >= existing.start_date:
                return jsonify({"message": "Staff already assigned to an overlapping trek"}), 400

    trek.assigned_staff_id = assigned_staff_id
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Staff assigned successfully"}), 200


@app.route('/api/admin/treks/<int:trek_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_trek(trek_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    trek = trekking_table.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    booking_table.query.filter_by(trek_id=trek_id).delete()
    db.session.delete(trek)
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Trek deleted successfully"}), 200


@app.route('/api/admin/staff', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def admin_get_staff():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    staff_list = User.query.filter_by(role='staff').all()
    result = []

    for staff in staff_list:
        result.append({
            "id": staff.id,
            "full_name": staff.full_name,
            "email": staff.email,
            "contact_number": staff.contact_number,
            "experience": staff.experience,
            "specialization": staff.specialization,
            "status": staff.status
        })

    return jsonify(result), 200


@app.route('/api/admin/staff', methods=['POST'])
@jwt_required()
def admin_create_staff():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    contact_number = data.get('contact_number')
    experience = data.get('experience')
    specialization = data.get('specialization')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    username = email.split('@')[0]

    if User.query.filter_by(username=username).first():
        username = username + str(User.query.count() + 1)

    staff = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role='staff',
        full_name=full_name,
        contact_number=contact_number,
        experience=experience,
        specialization=specialization,
        status='active'
    )
    db.session.add(staff)
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Staff created successfully"}), 201


@app.route('/api/admin/staff/<int:staff_id>/status', methods=['PUT'])
@jwt_required()
def admin_staff_status(staff_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    staff = User.query.get(staff_id)
    if not staff or staff.role != 'staff':
        return jsonify({"message": "Staff not found"}), 404

    data = request.get_json()
    staff.status = data.get('status')
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Staff status updated successfully"}), 200


@app.route('/api/admin/staff/<int:staff_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_staff(staff_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    staff = User.query.get(staff_id)
    if not staff or staff.role != 'staff':
        return jsonify({"message": "Staff not found"}), 404

    db.session.delete(staff)
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Staff deleted successfully"}), 200


@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def admin_get_users():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    users = User.query.filter_by(role='user').all()
    result = []

    for u in users:
        result.append({
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "contact_number": u.contact_number,
            "status": u.status
        })

    return jsonify(result), 200


@app.route('/api/admin/users/<int:user_id>/status', methods=['PUT'])
@jwt_required()
def admin_user_status(user_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    target_user = User.query.get(user_id)
    if not target_user or target_user.role != 'user':
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    target_user.status = data.get('status')
    db.session.commit()
    clear_cache()
    return jsonify({"message": "User status updated successfully"}), 200


@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def admin_delete_user(user_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    target_user = User.query.get(user_id)
    if not target_user or target_user.role != 'user':
        return jsonify({"message": "User not found"}), 404

    db.session.delete(target_user)
    db.session.commit()
    clear_cache()
    return jsonify({"message": "User deleted successfully"}), 200


@app.route('/api/admin/search', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, make_cache_key=make_user_cache_key, response_filter=cache_only_success)
def admin_search():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    search_type = request.args.get('type')
    query = request.args.get('q', '').strip().lower()

    if search_type == 'staff':
        staff_list = User.query.filter_by(role='staff').all()
        result = []

        for staff in staff_list:
            if query in staff.full_name.lower() or query in staff.email.lower() or query in (staff.specialization or '').lower():
                result.append({
                    "id": staff.id,
                    "full_name": staff.full_name,
                    "email": staff.email,
                    "contact_number": staff.contact_number,
                    "experience": staff.experience,
                    "specialization": staff.specialization,
                    "status": staff.status
                })

        return jsonify(result), 200

    if search_type == 'user':
        users = User.query.filter_by(role='user').all()
        result = []

        for u in users:
            if query in u.full_name.lower() or query in u.email.lower():
                result.append({
                    "id": u.id,
                    "full_name": u.full_name,
                    "email": u.email,
                    "contact_number": u.contact_number,
                    "status": u.status
                })

        return jsonify(result), 200

    return jsonify({"message": "Invalid search type"}), 400


@app.route('/api/staff/dashboard', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, make_cache_key=make_user_cache_key, response_filter=cache_only_success)
def staff_dashboard():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'staff':
        return jsonify({"message": "Unauthorized access"}), 403

    assigned_treks = trekking_table.query.filter_by(assigned_staff_id=user.id).all()
    trek_list = []
    total_participants = 0
    ongoing_count = 0

    for trek in assigned_treks:
        booked_count = booking_table.query.filter_by(trek_id=trek.id, status='Booked').count()
        total_participants = total_participants + booked_count

        if trek.status == 'Ongoing':
            ongoing_count = ongoing_count + 1

        trek_list.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "start_date": trek.start_date,
            "end_date": trek.end_date,
            "available_slots": trek.available_slots,
            "total_slots": trek.total_slots,
            "status": trek.status
        })

    return jsonify({
        "stats": {
            "assigned_treks_count": len(assigned_treks),
            "total_participants": total_participants,
            "ongoing_treks_count": ongoing_count
        },
        "assigned_treks": trek_list
    }), 200


@app.route('/api/staff/treks/<int:trek_id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, make_cache_key=make_user_cache_key, response_filter=cache_only_success)
def staff_get_trek(trek_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'staff':
        return jsonify({"message": "Unauthorized access"}), 403

    trek = trekking_table.query.get(trek_id)
    if not trek or trek.assigned_staff_id != user.id:
        return jsonify({"message": "Trek not found or not assigned to you"}), 404

    return jsonify({
        "id": trek.id,
        "name": trek.name,
        "location": trek.location,
        "difficulty": trek.difficulty,
        "duration_days": trek.duration_days,
        "available_slots": trek.available_slots,
        "total_slots": trek.total_slots,
        "status": trek.status,
        "start_date": trek.start_date,
        "end_date": trek.end_date,
        "description": trek.description
    }), 200


@app.route('/api/staff/treks/<int:trek_id>/participants', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, make_cache_key=make_user_cache_key, response_filter=cache_only_success)
def staff_get_participants(trek_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'staff':
        return jsonify({"message": "Unauthorized access"}), 403

    trek = trekking_table.query.get(trek_id)
    if not trek or trek.assigned_staff_id != user.id:
        return jsonify({"message": "Trek not found or not assigned to you"}), 404

    bookings = booking_table.query.filter_by(trek_id=trek_id, status='Booked').all()
    result = []

    for booking in bookings:
        booking_user = User.query.get(booking.user_id)
        result.append({
            "id": booking_user.id if booking_user else booking.user_id,
            "full_name": booking_user.full_name if booking_user else '',
            "email": booking_user.email if booking_user else '',
            "contact_number": booking_user.contact_number if booking_user else '',
            "booking_date": booking.booking_date.strftime('%Y-%m-%d')
        })

    return jsonify(result), 200


@app.route('/api/staff/treks/<int:trek_id>', methods=['PUT'])
@jwt_required()
def staff_update_trek(trek_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'staff':
        return jsonify({"message": "Unauthorized access"}), 403

    trek = trekking_table.query.get(trek_id)
    if not trek or trek.assigned_staff_id != user.id:
        return jsonify({"message": "Trek not found or not assigned to you"}), 404

    data = request.get_json()
    available_slots = data.get('available_slots')
    status = data.get('status')

    booked_count = booking_table.query.filter_by(trek_id=trek_id, status='Booked').count()

    if int(available_slots) < booked_count:
        return jsonify({"message": "Cannot reduce available slots below current bookings"}), 400

    if int(available_slots) > trek.total_slots:
        return jsonify({"message": "Available slots cannot exceed total slots"}), 400

    trek.available_slots = available_slots

    if status == 'Completed' or status == 'Ongoing':
        trek.status = status
    elif status == 'Open' or status == 'Closed':
        trek.status = status
    else:
        trek.status = 'Pending'

    if trek.status == 'Completed':
        active_bookings = booking_table.query.filter_by(trek_id=trek_id, status='Booked').all()
        for active_booking in active_bookings:
            active_booking.status = 'Completed'

    db.session.commit()
    clear_cache()
    return jsonify({"message": "Trek updated successfully"}), 200


@app.route('/api/staff/treks/<int:trek_id>/complete', methods=['PUT'])
@jwt_required()
def staff_complete_trek(trek_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'staff':
        return jsonify({"message": "Unauthorized access"}), 403

    trek = trekking_table.query.get(trek_id)
    if not trek or trek.assigned_staff_id != user.id:
        return jsonify({"message": "Trek not found or not assigned to you"}), 404

    trek.status = 'Completed'

    active_bookings = booking_table.query.filter_by(trek_id=trek_id, status='Booked').all()
    for active_booking in active_bookings:
        active_booking.status = 'Completed'

    db.session.commit()
    clear_cache()
    return jsonify({"message": "Trek marked as completed"}), 200


@app.route('/api/user/treks', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def user_get_treks():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'user':
        return jsonify({"message": "Unauthorized access"}), 403

    treks = trekking_table.query.all()
    user_bookings = booking_table.query.filter_by(user_id=user.id, status='Booked').all()
    booked_trek_ids = [b.trek_id for b in user_bookings]
    trek_list = []

    for trek in treks:
        staff = User.query.get(trek.assigned_staff_id) if trek.assigned_staff_id else None
        trek_list.append({
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration_days": trek.duration_days,
            "available_slots": trek.available_slots,
            "total_slots": trek.total_slots,
            "status": trek.status,
            "start_date": trek.start_date,
            "end_date": trek.end_date,
            "description": trek.description,
            "image_url": trek.image_url,
            "assigned_staff_name": staff.full_name if staff else None,
            "is_booked": trek.id in booked_trek_ids,
            "can_book": trek.status == 'Open' and trek.available_slots > 0 and trek.id not in booked_trek_ids
        })

    return jsonify(trek_list), 200


@app.route('/api/user/bookings', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60, make_cache_key=make_user_cache_key, response_filter=cache_only_success)
def user_get_bookings():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'user':
        return jsonify({"message": "Unauthorized access"}), 403

    bookings = booking_table.query.filter_by(user_id=user.id).order_by(booking_table.created_at.desc()).all()
    result = []

    for booking in bookings:
        trek = trekking_table.query.get(booking.trek_id)
        result.append({
            "id": booking.id,
            "trek_id": booking.trek_id,
            "trek_name": trek.name if trek else '',
            "trek_location": trek.location if trek else '',
            "trek_start_date": trek.start_date if trek else '',
            "trek_end_date": trek.end_date if trek else '',
            "trek_difficulty": trek.difficulty if trek else '',
            "trek_status": trek.status if trek else '',
            "booking_date": booking.booking_date.strftime('%Y-%m-%d'),
            "status": booking.status
        })

    return jsonify(result), 200


@app.route('/api/user/bookings', methods=['POST'])
@jwt_required()
def user_create_booking():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'user':
        return jsonify({"message": "Unauthorized access"}), 403

    if user.status == 'blacklisted':
        return jsonify({"message": "Blacklisted users cannot make bookings"}), 403

    data = request.get_json()
    trek_id = data.get('trek_id')

    trek = trekking_table.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    if trek.status != 'Open':
        return jsonify({"message": "Booking is allowed only when trek status is Open"}), 400

    if trek.available_slots <= 0:
        return jsonify({"message": "No available slots for this trek"}), 400

    existing_booking = booking_table.query.filter_by(
        user_id=user.id,
        trek_id=trek_id,
        status='Booked'
    ).first()

    if existing_booking:
        return jsonify({"message": "You have already booked this trek"}), 400

    db.session.refresh(trek)

    if trek.available_slots <= 0:
        return jsonify({"message": "No available slots for this trek"}), 400

    booking = booking_table(user_id=user.id, trek_id=trek_id)
    db.session.add(booking)
    trek.available_slots = trek.available_slots - 1
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Booking created successfully"}), 201


@app.route('/api/user/bookings/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def user_cancel_booking(booking_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'user':
        return jsonify({"message": "Unauthorized access"}), 403

    booking = booking_table.query.get(booking_id)
    if not booking or booking.user_id != user.id:
        return jsonify({"message": "Booking not found"}), 404

    if booking.status != 'Booked':
        return jsonify({"message": "Only active bookings can be cancelled"}), 400

    trek = trekking_table.query.get(booking.trek_id)
    booking.status = 'Cancelled'

    if trek:
        trek.available_slots = trek.available_slots + 1

    db.session.commit()
    clear_cache()
    return jsonify({"message": "Booking cancelled successfully"}), 200


@app.route('/api/user/history', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def user_history():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'user':
        return jsonify({"message": "Unauthorized access"}), 403

    bookings = booking_table.query.filter(
        booking_table.user_id == user.id,
        booking_table.status.in_(['Completed', 'Cancelled'])
    ).order_by(booking_table.created_at.desc()).all()

    result = []

    for booking in bookings:
        trek = trekking_table.query.get(booking.trek_id)
        result.append({
            "id": booking.id,
            "trek_name": trek.name if trek else '',
            "trek_location": trek.location if trek else '',
            "trek_start_date": trek.start_date if trek else '',
            "trek_end_date": trek.end_date if trek else '',
            "trek_status": trek.status if trek else '',
            "booking_date": booking.booking_date.strftime('%Y-%m-%d'),
            "status": booking.status
        })

    return jsonify(result), 200


@app.route('/api/admin/history', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def admin_history():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    bookings = booking_table.query.filter(
        booking_table.status.in_(['Completed', 'Cancelled'])
    ).order_by(booking_table.created_at.desc()).all()

    result = []

    for booking in bookings:
        trek = trekking_table.query.get(booking.trek_id)
        booking_user = User.query.get(booking.user_id)
        result.append({
            "id": booking.id,
            "user_name": booking_user.full_name if booking_user else '',
            "user_email": booking_user.email if booking_user else '',
            "trek_name": trek.name if trek else '',
            "trek_location": trek.location if trek else '',
            "trek_start_date": trek.start_date if trek else '',
            "trek_end_date": trek.end_date if trek else '',
            "trek_status": trek.status if trek else '',
            "booking_date": booking.booking_date.strftime('%Y-%m-%d'),
            "status": booking.status
        })

    return jsonify(result), 200


@app.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def user_update_profile():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'user':
        return jsonify({"message": "Unauthorized access"}), 403

    data = request.get_json()

    if data.get('full_name'):
        user.full_name = data.get('full_name')
    if data.get('contact_number'):
        user.contact_number = data.get('contact_number')

    db.session.commit()
    clear_cache()
    return jsonify({
        "message": "Profile updated successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name,
            "contact_number": user.contact_number,
            "status": user.status
        }
    }), 200


@app.route('/api/user/export-history', methods=['GET'])
@jwt_required()
def user_export_history():
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'user':
        return jsonify({"message": "Unauthorized access"}), 403

    # Start the CSV job in Celery instead of creating it inside the API request.
    task = create_trekking_history_csv.delay(user.id)

    # Store task owner in Redis for one hour.
    cache.set('export_owner_' + task.id, user.id, timeout=3600)

    return jsonify({
        "message": "CSV export started",
        "task_id": task.id
    }), 202


@app.route('/api/user/export-status/<task_id>', methods=['GET'])
@jwt_required()
def user_export_status(task_id):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'user':
        return jsonify({"message": "Unauthorized access"}), 403

    owner_id = cache.get('export_owner_' + task_id)

    if owner_id is None or int(owner_id) != user.id:
        return jsonify({"message": "Export task not found"}), 404

    task = AsyncResult(task_id, app=celery)

    if task.state == 'PENDING' or task.state == 'STARTED':
        return jsonify({
            "status": "pending"
        }), 200

    if task.state == 'SUCCESS':
        result = task.result

        return jsonify({
            "status": "ready",
            "result": {
                "download_url": result.get('download_url')
            }
        }), 200

    if task.state == 'FAILURE':
        return jsonify({
            "status": "failed",
            "message": str(task.result)
        }), 200

    return jsonify({
        "status": task.state.lower()
    }), 200


@app.route('/api/user/export-download/<file_name>', methods=['GET'])
@jwt_required()
def user_export_download(file_name):
    user = User.query.get(int(get_jwt_identity()))
    if not user or user.role != 'user':
        return jsonify({"message": "Unauthorized access"}), 403

    # A user can only download a file created for their own user id.
    expected_start = 'trek_history_' + str(user.id) + '_'

    if not file_name.startswith(expected_start):
        return jsonify({"message": "You cannot download this file"}), 403

    file_path = os.path.join(EXPORT_DIR, file_name)

    if not os.path.exists(file_path):
        return jsonify({"message": "CSV file not found"}), 404

    return send_from_directory(
        EXPORT_DIR,
        file_name,
        as_attachment=True
    )


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(username=username, email=email, password=generate_password_hash(password), role='user', full_name='', contact_number='', status='active')
    db.session.add(user)
    db.session.commit()
    clear_cache()
    return jsonify({"message": "user Register successfully", "data": data, })

@app.route('/Login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User account does not exist"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    if user.status == 'blacklisted':
        return jsonify({"message": "This account is blacklisted. Log in denied."}), 403

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"message": "Login successful", "access_token": access_token}), 200

@app.route('/admin/create_staff', methods=['POST'])
def create_staff():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    contact_number = data.get('contact_number')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    staff = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role='staff',
        full_name=full_name,
        contact_number=contact_number,
        status='active'
    )
    db.session.add(staff)
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Staff created successfully", "data": data}), 201

@app.route('/admin/delete_staff', methods=['POST'])
def delete_staff():
    data = request.get_json()
    staff_id = data.get('staff_id')

    staff = User.query.get(staff_id)
    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    db.session.delete(staff)
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Staff deleted successfully"}), 200


@app.route('/admin/create_trek', methods=['POST'])
def create_trek():
    data = request.get_json()
    name = data.get('name')
    location = data.get('location')
    difficulty = data.get('difficulty')
    duration_days = data.get('duration_days')
    available_slots = data.get('available_slots')
    total_slots = data.get('total_slots')
    assigned_staff_id = data.get('assigned_staff_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    description = data.get('description')
    image_url = data.get('image_url')

    if not total_slots or int(total_slots) <= 0:
        return jsonify({"message": "Trek must have at least 1 slot"}), 400

    if start_date <= date.today().isoformat():
        return jsonify({"message": "Trek start date must be after today"}), 400

    duplicate = trekking_table.query.filter_by(
        name=name,
        location=location,
        start_date=start_date
    ).first()

    if duplicate:
        return jsonify({"message": "Duplicate trek already exists"}), 400

    if assigned_staff_id:
        existing_treks = trekking_table.query.filter_by(
            assigned_staff_id=assigned_staff_id
        ).all()

        for existing in existing_treks:
            if start_date <= existing.end_date and end_date >= existing.start_date:
                return jsonify({"message": "Staff already assigned to an overlapping trek"}), 400

    trek = trekking_table(
        name=name,
        location=location,
        difficulty=difficulty,
        duration_days=duration_days,
        available_slots=available_slots,
        total_slots=total_slots,
        assigned_staff_id=assigned_staff_id,
        status='Upcoming',
        start_date=start_date,
        end_date=end_date,
        description=description,
        image_url=image_url
    )
    db.session.add(trek)
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Trek created successfully", "data": data}), 201

@app.route('/admin/delete_trek', methods=['POST'])
def delete_trek():
    data = request.get_json()
    trek_id = data.get('trek_id')

    trek = trekking_table.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    booking_table.query.filter_by(trek_id=trek_id).delete()
    db.session.delete(trek)
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Trek deleted successfully"}), 200

@app.route('/admin/create_booking', methods=['POST'])
def create_booking():
    data = request.get_json()
    user_id = data.get('user_id')
    trek_id = data.get('trek_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    trek = trekking_table.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    if trek.status != 'Open':
        return jsonify({"message": "Booking is allowed only when trek status is Open"}), 400

    if trek.available_slots <= 0:
        return jsonify({"message": "No available slots for this trek"}), 400

    existing_booking = booking_table.query.filter_by(
        user_id=user_id,
        trek_id=trek_id,
        status='Booked'
    ).first()

    if existing_booking:
        return jsonify({"message": "User has already booked this trek"}), 400

    db.session.refresh(trek)

    if trek.available_slots <= 0:
        return jsonify({"message": "No available slots for this trek"}), 400

    booking = booking_table(user_id=user_id, trek_id=trek_id)
    db.session.add(booking)
    trek.available_slots -= 1
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Booking created successfully", "data": data}), 201

@app.route('/admin/blacklist_staff', methods=['POST'])
def blacklist_staff():
    data = request.get_json()
    staff_id = data.get('staff_id')

    staff = User.query.get(staff_id)
    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    staff.status = 'blacklisted'
    db.session.commit()
    clear_cache()
    return jsonify({"message": "Staff blacklisted successfully"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(role='admin').first():
            admin = User(
                username='admin',
                email='admin@tma.com',
                password=generate_password_hash('admin123'),
                role='admin',
                full_name='Admin',
                contact_number='8630042780',
                status='active'
            )
            db.session.add(admin)
            db.session.commit()
            clear_cache()

    app.run(debug=True)
