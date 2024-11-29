from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Factory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    
    machines = db.relationship('Machine', backref='factory', lazy=True)
    workers = db.relationship('Worker', backref='factory', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location
        }

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    factory_id = db.Column(db.Integer, db.ForeignKey('factory.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'factory_id': self.factory_id
        }

class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    factory_id = db.Column(db.Integer, db.ForeignKey('factory.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'factory_id': self.factory_id
        }