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



if __name__ == "__main__":
    with app.app_context():
        # Create all tables
        db.create_all()
         # Check admin exists or not
    app.run(debug=True)