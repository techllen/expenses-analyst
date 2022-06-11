from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
class User:
    # initializing database name variable
    database_name = "private_wall_db"

    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    # this method creates user entry in the database
    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)" 
        # retrieving the id of created user for session
        user_id = connectToMySQL(User.database_name).query_db(query,data)
        return user_id
    # this method verifies users from our database
    @classmethod
    def verify_user(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        user = connectToMySQL(User.database_name).query_db(query,data)
        # print(user)
        # checking if we found any user
        if len(user) == 0:
            return False
        else:
            return cls(user[0])
    # this method get all users from our database
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users ORDER BY first_name ASC"
        users = connectToMySQL(User.database_name).query_db(query)
        users_to_display = []
        # checking if we found any user
        if len(users) == 0:
            return None
        else:
        # turning user results to objects
            for user in users:
                this_user = cls(user)
                # print(this_user)
                users_to_display.append(this_user)
            # returning list of user objects
            return users_to_display
    # this method get one user from the database
    @classmethod
    def get_one_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        user = connectToMySQL(User.database_name).query_db(query,data)
        # print(user)
        # checking if we found any user
        if len(user) == 0:
            return None
        else:
            return cls(user[0])
    # this method flashed error messages only when invalid credentials have been entered in registration    
    @staticmethod
    def user_validation(user):
        is_valid = True
        # regex to check for names validity
        name_regex = re.compile(r"^[a-zA-Z]")
        # regex to check for email validity
        email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        # regex for password validity 
        password_regex = re.compile(r"^[a-zA-Z0-9]")
        # checking if First Name - letters only, at least 2 characters
        if not (name_regex.match(user["first_name"]) and len(user["first_name"])>=2) :
            flash("- First name must be letters only and at least 2 letters","register-error")
            is_valid = False
        # checking if Last Name - letters only, at least 2 characters
        if not (name_regex.match(user["last_name"]) and len(user["last_name"])>=2):
            # flash message and its category
            flash("- Last name must be letters only and at least 2 letters","register-error")
            is_valid = False
        # checking for email format validity
        if not email_regex.match(user["email"]):
            # flash message and its category
            flash("- Please enter a valid email address example:name@example.com","register-error")
            is_valid = False
        # checking for password validity(8 characters(alphanumeric),includes at least 1 number,at least 1 uppercase)
        if not (password_regex.match(user["password"]) and len(user["password"])>=8 and re.search("[0-9]",user["password"]) is not None and re.search("[A-Z]",user["password"]) is not None):
            # flash message and its category
            flash("- Password must be at least 8 characters(Alphanumeric), at least one number and at least one uppercase letter","register-error")
            is_valid = False
        # checking for match btn password and password confirmation field
        if not user["password"] == user["confirmed_password"]:
            # flash message and its category
            flash("- Entered password must be the same as confirmed password","register-error")
            is_valid = False
        return is_valid
    # this method flashes error messages only when invalid credentials have been entered
    @staticmethod
    def user_login_validation():
            flash("- Invalid Credentials","login-error")
            
    
