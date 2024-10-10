from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from datetime import datetime
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost/movie_ticketing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    showtime = db.Column(db.DateTime, nullable=False)

# Define the Booking model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)

# Test the database connection
def test_db_connection():
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
            print("Database connection is successful.")
    except OperationalError as e:
        print(f"Database connection failed: {e}")

@app.route('/')
def home():
    return render_template('index.html')

# Route to get all movies
@app.route('/movies', methods=['GET'])
def get_movies():
    with app.app_context():
        movies = Movie.query.all()
        return jsonify([{'id': movie.id, 'title': movie.title, 'showtime': movie.showtime.isoformat()} for movie in movies])

# Route to book a ticket
@app.route('/book',methods=['POST'])
def book_ticket():
    data = request.get_json()  # Use get_json to parse the incoming JSON
    print(f"Received data: {data}") 
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    new_booking = Booking(
        movie_id=data['movie_id'],
        customer_name=data['customer_name'],
        number_of_tickets=data['number_of_tickets']
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Booking successful', 'booking_id': new_booking.id}), 201

# Route to get all bookings
@app.route('/bookings', methods=['GET'])
def get_bookings():
    with app.app_context():
        bookings = Booking.query.all()
        return jsonify([{'id': booking.id, 'movie_id': booking.movie_id, 'customer_name': booking.customer_name, 'number_of_tickets': booking.number_of_tickets} for booking in bookings])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the tables
        test_db_connection()  # Test the database connection
    app.run(host='0.0.0.0', port=5000, debug=True)  # Make the app accessible externally

