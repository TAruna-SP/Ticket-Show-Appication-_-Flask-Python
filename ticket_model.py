from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id =  db.Column(db.Integer() ,primary_key = True)
    user_name = db.Column(db.String(30) ,nullable =False)
    first_name = db.Column(db.String(30) ,nullable =False)
    last_name = db.Column(db.String(30) ,nullable = True)
    mobile_number = db.Column(db.String(30) ,nullable =False)
    user_password = db.Column(db.String(30) ,nullable =False)
    user_type = db.Column(db.String(10) , nullable = False)
    shows_booked = db.relationship("Booking", backref="user_details")

class Booking(db.Model):
    booking_id = db.Column(db.Integer() ,primary_key = True)
    venue_name_booked = db.Column(db.String(30) ,nullable =False)
    show_name_booked = db.Column(db.String(30) ,nullable =False)
    bookedshow_start_timing  = db.Column(db.String(20), nullable = False)
    bookedshow_end_timing = db.Column(db.String(20), nullable = False) 
    total_price =  db.Column(db.Integer())
    num_of_tickets_booked = db.Column(db.Integer())
    user_id_booked = db.Column(db.Integer(), db.ForeignKey("user.user_id" ))
  
class Venue(db.Model):
    venue_id =  db.Column(db.Integer() ,primary_key = True)
    venue_name = db.Column(db.String(30) ,nullable =False)
    venue_place = db.Column(db.String(30) ,nullable =False)
    venue_location = db.Column(db.String(30) ,nullable =False)
    venue_capacity =  db.Column(db.Integer())
    list_of_shows = db.relationship("Show", backref="venue_details" , secondary = "venue_show_relation")

class Show(db.Model):
    show_id =  db.Column(db.Integer() ,primary_key = True)
    show_name = db.Column(db.String(30) ,nullable =False)
    show_rating =  db.Column(db.Integer())
    show_tag = db.Column(db.String(30) ,nullable =False)
    show_start_timing = db.Column(db.String(20), nullable = False)
    show_end_timing = db.Column(db.String(20), nullable = False)
    show_ticket_price =  db.Column(db.Integer())
    show_capacity = db.Column(db.Integer())

class Venue_show_relation(db.Model):
    venueID = db.Column(db.Integer(), db.ForeignKey("venue.venue_id" ), primary_key = True)
    showID = db.Column(db.Integer(), db.ForeignKey("show.show_id" ), primary_key = True)



