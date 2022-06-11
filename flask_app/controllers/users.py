from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models import user
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

# this route redirect users to the index/home page
@app.route("/")
def home():
    return render_template("index.html")
# this route handles user registration
@app.route("/register", methods = ["POST"])
def register():
    # first thing first validate inputs
    if not user.User.user_validation(request.form):
        # if any user input is invalid send the user to home page
        return redirect("/")
    else:
        #hashing passwords
        password_hash = bcrypt.generate_password_hash(request.form["password"])
        # print(password_hash)
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            #assigning the password hash into the password dictionary key    
            "password": password_hash
        }
        # saving the data
        user_id = user.User.register_user(data)
        # assigning session to the user
        session["user_id"] = user_id
    return redirect("/page4")

    
# this route handles user login
@app.route("/login", methods = ["POST"])
def login():
    data = {
        "email": request.form["email"],
    }
    found_user = user.User.verify_user(data)
    # chacking if the password match
    if not found_user:
        # flash error message if no match
        user.User.user_login_validation()
        return redirect("/")
    if not bcrypt.check_password_hash(found_user.password,request.form["password"]):
        # flash error message if no match
        user.User.user_login_validation()
        return redirect("/")
    #assigning session to the user
    session["user_id"] = found_user.id
    return redirect("/page4")

@app.route("/page4")
def page4():
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        data = {
            "id": session["user_id"]
        }
        user_to_display = user.User.get_one_user_by_id(data)
        # print(f"user is {user_to_display.first_name}")
        return render_template("page4.html",user_to_display = user.User.get_one_user_by_id(data))

# this route allows user to access a certain page
@app.route("/page")
def page():
    # check if user is logged in
    if session.get("user_id")==None:
        return redirect("/")
    else:
        return render_template("page3.html")

# this route clears the sessions
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
# this route redirects the user to the error page if the links is not found
@app.errorhandler(404)
def errors(e):
    return render_template("errorpage.html")