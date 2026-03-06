from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# ──────────────────────────────────────────────
# User Model
# ──────────────────────────────────────────────
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    designs = db.relationship('Design', backref='user', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and store the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# ──────────────────────────────────────────────
# Design Model
# ──────────────────────────────────────────────
class Design(db.Model):
    __tablename__ = 'designs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_path = db.Column(db.String(300), nullable=True)
    selected_style = db.Column(db.String(100), nullable=True)
    ai_output = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Design {self.id}>'


# ──────────────────────────────────────────────
# Furniture Model
# ──────────────────────────────────────────────
class Furniture(db.Model):
    __tablename__ = 'furniture'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=True)
    image_url = db.Column(db.String(300), nullable=True)

    # Relationship
    bookings = db.relationship('Booking', backref='furniture', lazy=True)

    def __repr__(self):
        return f'<Furniture {self.name}>'


# ──────────────────────────────────────────────
# Booking Model
# ──────────────────────────────────────────────
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    furniture_id = db.Column(db.Integer, db.ForeignKey('furniture.id'), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Booking {self.id}>'
