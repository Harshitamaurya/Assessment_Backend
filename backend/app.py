from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
#adding database path
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///C:/Users/HP-PC/Desktop/ZOMENTUM/backend/ticketbooking.db'
db = SQLAlchemy(app)

from backend import functions
