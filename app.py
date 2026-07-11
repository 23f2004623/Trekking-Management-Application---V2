from flask import Flask, jsonify, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended  import ( 
    JWTManager, create_access_token, jwt_required, get_jwt_identity)

from functools import wraps
import json
from sqlalchemy import text



app = Flask(__name__)

# allow requests from vue app
CORS(app)


# sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = '@1234'  # Change this to a random secret key
jwt = JWTManager(app)



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
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade="all, delete-orphan")
    assigned_treks = db.relationship('Trek', backref='assigned_staff', lazy=True)


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
    status = db.Column(db.String(20), default='Open')  # Pending, Open, Closed, Completed
    start_date = db.Column(db.String(20), nullable=False)  # YYYY-MM-DD
    end_date = db.Column(db.String(20), nullable=False)    # YYYY-MM-DD
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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



@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Trekking API"}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        
        return jsonify({"message": "Email already exists"}), 400
    
    if user.status == 'Blacklisted':
        return jsonify({"message": "User is blacklisted and cannot register"}), 403
    

    user = User(username=username, email=email, password=password(password), role='user', full_name='', contact_number='', status='active')
    db.session.add(user)
    db.session.commit()
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
        password=password(password),
        role='staff',
        full_name=full_name,
        contact_number=contact_number,
        status='active'
    )
    db.session.add(staff)
    db.session.commit()
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
    status = data.get('status', 'Open')  # Default to 'Open' if not provided
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    description = data.get('description')
    image_url = data.get('image_url')

    trek = trekking_table(
        name=name,
        location=location,
        difficulty=difficulty,
        duration_days=duration_days,
        available_slots=available_slots,
        total_slots=total_slots,
        assigned_staff_id=assigned_staff_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
        description=description,
        image_url=image_url
    )
    db.session.add(trek)
    db.session.commit()
    return jsonify({"message": "Trek created successfully", "data": data}), 201

@app.route('/admin/delete_trek', methods=['POST'])
def delete_trek():
    data = request.get_json()
    trek_id = data.get('trek_id')

    trek = trekking_table.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    db.session.delete(trek)
    db.session.commit()
    return jsonify({"message": "Trek deleted successfully"}), 200

@app.route('/admin/create_booking', methods=['POST'])
def create_booking():
    data = request.get_json()
    user_id = data.get('user_id')
    trek_id = data.get('trek_id')

    # Check if the user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Check if the trek exists
    trek = trekking_table.query.get(trek_id)
    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    # Check if there are available slots
    if trek.available_slots <= 0:
        return jsonify({"message": "No available slots for this trek"}), 400

    # Create the booking
    booking = booking_table(user_id=user_id, trek_id=trek_id)
    db.session.add(booking)

    # Decrease the available slots for the trek
    trek.available_slots -= 1

    db.session.commit()
    return jsonify({"message": "Booking created successfully", "data": data}), 201

@app.route('/admin/blacklist_staff', methods=['POST'])
def blacklist_staff():
    data = request.get_json()
    staff_id = data.get('staff_id')

    staff = User.query.get(staff_id)
    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    staff.is_blacklisted = True
    db.session.commit()
    return jsonify({"message": "Staff blacklisted successfully"}), 200


if __name__ == "__main__":
    with app.app_context():
        # Create all tables
        db.create_all()
         # Check admin exists or not
    app.run(debug=True)