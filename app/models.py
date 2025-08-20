from app.init import db
from datetime import datetime
import uuid

class Site(db.Model):
    __tablename__ = 'sites'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    buildings = db.relationship('Building', backref='site', lazy=True, cascade='all, delete-orphan')

class Building(db.Model):
    __tablename__ = 'buildings'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    floors = db.Column(db.Integer, nullable=False)
    site_id = db.Column(db.String(36), db.ForeignKey('sites.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    levels = db.relationship('Level', backref='building', lazy=True, cascade='all, delete-orphan')

class Level(db.Model):
    __tablename__ = 'levels'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    level_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    map_data = db.Column(db.Text)
    building_id = db.Column(db.String(36), db.ForeignKey('buildings.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)