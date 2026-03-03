from app import db
from datetime import datetime

class Design(db.Model):
    __tablename__ = 'designs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(300), nullable=True)
    style = db.Column(db.String(100), nullable=True)
    room_type = db.Column(db.String(100), nullable=True)
    budget = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Design {self.title}>'


class FurnitureItem(db.Model):
    __tablename__ = 'furniture_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=True)
    image_path = db.Column(db.String(300), nullable=True)
    style = db.Column(db.String(100), nullable=True)
    dimensions = db.Column(db.String(150), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FurnitureItem {self.name}>'
