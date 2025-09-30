import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/find", methods=["GET", "POST"])
@login_required
def find():
    """Find activity"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        activity = request.form.get("activity")
        location = request.form.get("location")

        if not activity and not location:
            return apology("must provide at least one parameter", 400)

        user_id = session["user_id"]
        if activity and location:
            activity_db = db.execute("SELECT * FROM activity WHERE location = ? AND activity LIKE ?", location, f'%{activity}%')

        elif activity:
            activity_db = db.execute("SELECT * FROM activity WHERE activity LIKE ?", f'%{activity}%')

        elif location:
            activity_db = db.execute("SELECT * FROM activity WHERE location = ?", location)


        return render_template("index.html", database=activity_db)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        locations_db = db.execute("SELECT * FROM locations")
        return render_template("find.html", loc_db = locations_db)





@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    """Start new activity"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        activity = request.form.get("activity")
        location = request.form.get("location")
        time = request.form.get("time")
        contact = request.form.get("contact")

        # Ensure activity was submitted
        if not activity:
            return apology("must provide activity", 400)

        # Ensure location was submitted
        elif not location:
            return apology("must provide location", 400)

        # Ensure time was submitted
        elif not time:
            return apology("must provide time", 400)

        # Ensure contact was submitted
        elif not contact:
            return apology("must provide contact", 400)

        # Remember which user has logged in
        user_id = session["user_id"]

        # Insert new user info into database
        db.execute("INSERT INTO activity (activity, location, time, contact) VALUES(?, ?, ?, ?)", activity, location, time, contact)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        locations_db = db.execute("SELECT * FROM locations")
        return render_template("new.html", loc_db = locations_db)




@app.route("/")
@login_required
def index():
    """Show current activities near you"""

    user_id = session["user_id"]
    location_db = db.execute("SELECT location FROM users WHERE id = ?", user_id)
    #user_location = location_db[0]["location"]


    #activity_db = db.execute("SELECT * FROM activity WHERE location = ?", user_location)
    activity_db = db.execute("SELECT * FROM activity")
    for row in activity_db:
        activity = row["activity"]
        time = row["time"]

    return render_template("index.html", database=activity_db)


'''
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    rows = db.execute("SELECT * FROM transactions WHERE id = ?", user_id)
    return render_template("history.html", database = rows)
'''


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        sex = request.form.get("sex")
        age = int(request.form.get("age"))
        email = request.form.get("email")
        location = request.form.get("location")
        phone = request.form.get("phone")
        if phone:
                phone = int(phone)

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        #Ensure password was confirmed
        elif password != confirmation:
            return apology("password does not match", 400)

        #Ensure sex was submitted
        elif not sex:
            return apology("must provide sex", 400)

        #Ensure age was submitted
        elif not age:
            return apology("must provide age", 400)

        #Ensure age >= 18
        elif age < 18:
            return apology("age must be above 18", 400)


        # Query database for username

        elif db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology("username already taken", 400)

        # insert new user info into database
        db.execute("INSERT INTO users (username, hash, age, sex, location, email, phone) VALUES(?, ?, ?, ?, ?, ?, ?)", username, generate_password_hash(password, method='pbkdf2', salt_length=16), age, sex, location, email, phone)
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        locations_db = db.execute("SELECT * FROM locations")
        return render_template("register.html", loc_db = locations_db)



def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


#Listen for error
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
