from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost/movie_ticketing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    showtime = db.Column(db.DateTime, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)

def test_db_connection():
    try:
        # Use app context to test database connection
        with app.app_context():
            db.session.execute(text('SELECT 1'))
            print("Database connection is successful.")
    except OperationalError as e:
        print(f"Database connection failed: {e}")

if __name__ == '__main__':
    with app.app_context():  # Create application context here
        db.create_all()  # Creates the tables
        test_db_connection()  # Test the database connection
    app.run(host='0.0.0.0', port=5000, debug=True) #By default, Flask runs on localhost, which means it's only accessible from the local machine. To make it accessible externally.

