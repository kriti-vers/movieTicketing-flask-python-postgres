from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/movie_ticketing'
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

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([{'id': movie.id, 'title': movie.title, 'showtime': movie.showtime} for movie in movies])

@app.route('/book', methods=['POST'])
def book_ticket():
    data = request.json
    new_booking = Booking(
        movie_id=data['movie_id'],
        customer_name=data['customer_name'],
        number_of_tickets=data['number_of_tickets']
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Booking successful', 'booking_id': new_booking.id}), 201

@app.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([{'id': booking.id, 'movie_id': booking.movie_id, 'customer_name': booking.customer_name, 'number_of_tickets': booking.number_of_tickets} for booking in bookings])

if __name__ == '__main__':
    db.create_all()  # Creates the tables
    app.run(debug=True)
