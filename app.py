from flask import Flask, jsonify, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)




app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/register', methods=['GET','POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user = User(username=username, email=email, password=password, role='user', full_name='', contact_number='')
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "user Register successfully", "data": data, })

if __name__ == "__main__":
    with app.app_context():
        # Create all tables
        db.create_all()
         # Check admin exists or not
    app.run(debug=True)