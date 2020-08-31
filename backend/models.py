from datetime import datetime
from flask_login import UserMixin
from backend.app import db

#schema for User table
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    # attributes
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50),nullable=False)
    phoneNumber = db.Column(db.String(10),nullable=False,unique=True)
    # Relationships
    tkt = db.relationship('Ticket', backref=db.backref('tickets', lazy=True))

#schema for Ticket table
class Ticket(db.Model):
    __tablename__ = 'ticket'
    # attributes
    tid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    cust_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    time_of_movie=db.Column(db.DateTime,db.ForeignKey('movieShow.timing'),nullable=False)
    hasexpired = db.Column(db.Boolean,default=0)

#schema for MovieShow table    
class MovieShow(db.Model):
    __tablename__ = 'movieShow'
    # attributes
    timing = db.Column(db.DateTime,primary_key=True, unique=True, nullable=False)
    number_of_tickets = db.Column(db.Integer,default=20)
    # Relationships
    time = db.relationship('Ticket',cascade="save-update",backref=db.backref('time', lazy=True))
