# **************************************************** IMPORT *****************************************************************************
from flask import Flask ,  render_template , request ,redirect ,url_for , session 
from ticket_model import *

# ************************************************** CONFIGURATION ************************************************************************
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///my_ticket_show.sqlite3"
app.secret_key = 'b4e60b0fe2fb9b5f4799e1e5e0b8eabadf76c5ed04c9fc88f96f87f8f2a33d25'

db.init_app(app)
app.app_context().push()

# ****************************************************CONTROLLER **************************************************************************
@app.route("/" , methods=["GET" , "POST"])
def basePage():
    return render_template("base.html")

@app.route("/user_dashboard" , methods =["GET" ,"POST"])
def user_dashboard():
    venue_list = Venue.query.all()
    return render_template("user_dashboard.html", venue_list=venue_list )

@app.route("/User_Login" , methods= ["GET" , "POST"])
def User_Login():
    if request.method == "POST":
       user_username =  request.form.get("username") 
       user_userpass =  request.form.get("userpass") 
       user_obj = User.query.filter_by(user_type="user").first()
      
       if(user_obj.user_name == user_username and user_obj.user_password == user_userpass):
            session["username"] = user_username
            session["userid"] = user_obj.user_id
            return redirect(url_for("user_dashboard"))
       else:
            message = "Invalid Credentials .Please try again"
            return render_template("user_login.html" ,message = message )

    return render_template("user_login.html")    

@app.route("/register" ,methods =["GET","POST"])
def register():
    if request.method == "POST":
       first_name =  request.form.get("first_name") 
       last_name =  request.form.get("last_name") 
       mobile_number =  request.form.get("mobile_num") 
       user_type =  request.form.get("user_type") 
       user_name =  request.form.get("user_name") 
       user_password =  request.form.get("user_password")
       new_User = User( first_name = first_name, last_name=last_name ,mobile_number=mobile_number ,user_type=user_type ,user_name=user_name ,user_password=user_password)
       db.session.add(new_User)
       db.session.commit()
       return redirect(url_for("User_Login")) 
    return render_template("register.html")

@app.route("/admin_dashboard" , methods =["GET" ,"POST"])
def admin_dashboard():
    venue_list = Venue.query.all()
    return render_template("admin_dashboard.html", venue_list = venue_list )

@app.route("/Admin_Login" , methods= ["GET" , "POST"])
def Admin_Login():
    if request.method == "POST":
       admin_username =  request.form.get("admin_username") 
       admin_userpass =  request.form.get("admin_userpass") 
       admin_obj = User.query.filter_by(user_type="admin").first()
      
       if(admin_obj.user_name == admin_username and admin_obj.user_password == admin_userpass):
            session["username"] = request.form.get("admin_username") 
            session["userid"] = admin_obj.user_id
            return redirect(url_for("admin_dashboard"))
       else:
            message = "Invalid Credentials .Please try again"
            return render_template("admin_login.html" ,message = message )

    return render_template("admin_login.html")         
             
@app.route("/create_venue" , methods = ["GET" ,"POST"])
def create_venue():
    if request.method == "POST":
       venue_name =  request.form.get("venue_name") 
       venue_place_selected =  request.form.get("venue_place")
       venue_location_selected =  request.form.get("venue_location") 
       venue_capacity =  request.form.get("venue_capacity")
       newVenue = Venue(venue_name = venue_name ,venue_place = venue_place_selected ,venue_location = venue_location_selected ,venue_capacity = venue_capacity )
       db.session.add(newVenue)
       db.session.commit()
       return redirect(url_for("admin_dashboard"))

    return render_template("add_venue.html")   

@app.route("/create_show/<int:id>" , methods = ["GET","POST"])  
def create_show(id):
    venue = Venue.query.get(id)
    if request.method == "POST":
       show_name =  request.form.get("show_name") 
       show_rating_selected =  request.form.get("show_rating")
       show_tag_selected =  request.form.get("show_tag") 
       show_ticket_price =  request.form.get("show_ticket_price")
       show_timing_selected = request.form.get("show_timing")
       start_time_selected, end_time_selected = show_timing_selected.split('-')
       newShow = Show(show_name = show_name ,show_rating = show_rating_selected ,show_tag = show_tag_selected ,show_ticket_price = show_ticket_price,show_start_timing=start_time_selected , show_end_timing=end_time_selected ,show_capacity=venue.venue_capacity)
       db.session.add(newShow)
       db.session.commit()
       venue.list_of_shows.append(newShow)
       db.session.commit()
       return redirect(url_for("admin_dashboard"))
    
    return render_template("add_show.html" , venue=venue) 

@app.route("/update_show/<int:id>" , methods = ["GET" , "POST"])
def edit_show(id):
    show_obj = Show.query.get(id)
    if request.method == "POST":
       show_obj.show_name = request.form.get("show_name")
       show_obj.show_rating = request.form.get("show_rating") 
       show_obj.show_tag =  request.form.get("show_tag")
       show_obj.show_ticket_price =  request.form.get("show_ticket_price")
       show_timing_selected = request.form.get("show_timing")
       start_time_selected, end_time_selected = show_timing_selected.split('-')
       show_obj.show_start_timing=start_time_selected
       show_obj.show_end_timing=end_time_selected
       db.session.commit()
       return redirect(url_for("admin_dashboard"))
    
    return render_template("edit_show.html" , show_obj=show_obj) 

@app.route("/delete_show/<int:id>" , methods = ["GET" ,"POST"])
def delete_show(id):
    show_obj = Show.query.get(id)
    db.session.delete(show_obj)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))
 
@app.route("/update_venue/<int:id>" , methods = ["GET" , "POST"])
def edit_venue(id):
    venue_obj = Venue.query.get(id)
    if request.method == "POST":
       venue_obj.venue_name = request.form.get("venue_name")
       venue_obj.venue_place = request.form.get("venue_place") 
       venue_obj.venue_location =  request.form.get("venue_location")
       venue_obj.venue_capacity =  request.form.get("venue_capacity")
       db.session.commit()
       return redirect(url_for("admin_dashboard"))
    
    return render_template("edit_venue.html" , venue_obj=venue_obj)     

@app.route("/delete_venue/<int:id>" , methods = ["GET" ,"POST"])
def delete_venue(id):
    venue_obj = Venue.query.get(id)
    db.session.delete(venue_obj)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/booking_detail" , methods = ["GET" ,"POST"])
def booking_detail():
    user_obj =User.query.get(session.get("userid"))
    return render_template("booking_detail.html" , user_obj=user_obj)    

@app.route("/book_show/<int:id>" , methods=["GET","POST"])
def book_show(id):
    show_obj = Show.query.get(id)
    user_obj = User.query.get(session.get("userid"))
    total_price = 0
    if request.method == "POST":
       num_of_tickets_booked =  request.form.get("num_tickets") 
       if(int(num_of_tickets_booked) > show_obj.show_capacity):
            display_msg = "Unable to book. Tickets unavailable"
            return render_template("book_show.html" , display_msg = display_msg ,show_obj=show_obj)
       total_price = show_obj.show_ticket_price * int(num_of_tickets_booked)
       newShow_booked = Booking(num_of_tickets_booked = num_of_tickets_booked ,venue_name_booked = show_obj.venue_details[0].venue_name ,show_name_booked =  show_obj.show_name ,bookedshow_start_timing = show_obj.show_start_timing,bookedshow_end_timing=show_obj.show_end_timing ,total_price=total_price ,user_id_booked = session.get("userid"))
       db.session.add(newShow_booked)
       db.session.commit()
       show_obj.show_capacity -= int(num_of_tickets_booked)
       db.session.commit()
       return redirect(url_for("booking_detail"))

    return render_template("book_show.html" , show_obj=show_obj )

@app.route("/edit_profile" ,methods=["GET" , "POST"])    
def edit_profile():
    user_obj = User.query.get(session.get("userid"))
    if request.method == "POST":
        user_obj.first_name=request.form.get("first_name")
        user_obj.last_name=request.form.get("last_name")
        user_obj.mobile_number=request.form.get("mob_num")
        db.session.commit()
        return redirect(url_for("user_dashboard"))
    
    return render_template("edit_profile.html",user_obj=user_obj)

@app.route("/logout" , methods=["GET","POST"])
def logout():
    session.pop('username',None)
    session.pop('userid',None)
    return redirect('/')

@app.route("/rating" ,methods=["GET" ,"POST"])
def rating():
    return render_template("rating.html")

# ****************************************************RUN**********************************************************************************
if(__name__) == "__main__":
    app.run(debug=True)    