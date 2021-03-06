from unicodedata import category
from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models import user,transaction
from flask_bcrypt import Bcrypt
import json        
bcrypt = Bcrypt(app)

# this route redirect users to the index/home page
@app.route("/")
def home():
    return render_template("registration.html")

# this route redirect users to the login
@app.route("/expenses_analyst/login")
def to_login_page():
    return render_template("login.html")

# this route redirect users to the yearly analysis page
@app.route("/expenses_analyst/dashboards/yearly_analysis")
def yearly_analysis():
     # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        data = {
                "id": session.get("user_id")
            }
        year = transaction.Transaction.get_current_year()
        all_years = transaction.Transaction.get_all_years()
        
        # year dictionary for selection
        year_data_income = {
            "category" : "Income",
            "year" : year
        }
        # retrieve income from the database
        total_income = transaction.Transaction.get_yearly_income(year_data_income)
        
        # year dictionary for selection
        year_data_expenses = {
            "amount" : 0,
            "year" : year
        }
        
        # retrieve expenses from the database
        total_expenses = transaction.Transaction.get_yearly_expenses(year_data_expenses)
        
        # checking if we have any data in the database
        if year == None:
            # if no data send the user to the upload page
            return redirect("/expenses_analyst/upload_statement")
        else:
            # print("year is:" + str(year))
            return render_template("dashboard_yearly_analysis.html",user_to_display = user.User.get_one_user_by_id(data),year = year,all_years_to_display = all_years ,total_income = total_income,expenses = total_expenses)

# this route redirect users to the monthly analysis page
@app.route("/expenses_analyst/dashboards/monthly_analysis")
def monthly_analysis():
     # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        data = {
                "id": session.get("user_id")
            }
        current_year = transaction.Transaction.get_current_year()
        year_data = {
            "year" : current_year
        }
        current_month = transaction.Transaction.get_current_month(year_data)
        
        # all_months = transaction.Transaction.get_all_months()
        # all_years = transaction.Transaction.get_all_years()
        # retrieve a list of dictionaries from the database containing months and years
        all_months_years = transaction.Transaction.get_all_years_months_pairs()

        # year dictionary for selection
        month_data_income = {
            "category" : "Income",
            "month": current_month,
            "year" : current_year
        }
        # retrieve income from the database
        total_income = transaction.Transaction.get_monthly_income(month_data_income)
        
        # year dictionary for selection
        month_data_expenses = {
            "amount" : 0,
            "month": current_month,
            "year" : current_year
        }
        
        # retrieve expenses from the database
        total_expenses = transaction.Transaction.get_monthly_expenses(month_data_expenses)

        # checking if we have any data in the database
        if current_month == None:
            # if no data send the user to the upload page
            return redirect("/expenses_analyst/upload_statement")
        else:
            return render_template("dashboard_monthly_analysis.html",user_to_display = user.User.get_one_user_by_id(data),month = current_month,year = current_year,months_years=all_months_years,total_income = total_income,expenses = total_expenses)

# this route redirect users to the edit categories page
@app.route("/expenses_analyst/edit_categories")
def edit_categories():
     # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        # retrieve all transactions for the current month
        current_year = transaction.Transaction.get_current_year()
        # dict for current year
        year_data = {
            "year" : current_year
        }
        current_month = transaction.Transaction.get_current_month(year_data)

        all_months_years = transaction.Transaction.get_all_years_months_pairs()

        # transaction data
        transaction_data = {
            "month" : current_month,
            "year" : current_year
        }
        transactions_to_display = transaction.Transaction.get_transactions_for_month_year(transaction_data)
        
        categories_from_db = transaction.Transaction.get_all_categories_only()

        # checking if we have any data in the database
        if current_month == None:
            # if no data send the user to the upload page
            return redirect("/expenses_analyst/upload_statement")
        else:
            return render_template("dashboard_edit_categories.html",month = current_month,year = current_year,months_years = all_months_years,transactions_from_db = transactions_to_display,categories_to_display = categories_from_db)

# this route redirect users to the edit categories page for a specific month
@app.route("/expenses_analyst/edit_categories_month" ,methods = ["POST"])
def edit_categories_month():
     # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
         # replace single quotes with double and convert a string dict to dict
        month_year_dict = json.loads((request.form["month_year"]).replace("'",'"'))
        
        year = month_year_dict["year"]
        month = month_year_dict["month"]
        # print("MONTH**" + str(month))
        # print("Year**" + str(year))
        # print("DICT **" + request.form["month_year"])
        

        all_months_years = transaction.Transaction.get_all_years_months_pairs()
        # transaction data
        transaction_data = {
            "month" : month,
            "year" : year
        }
        transactions_to_display = transaction.Transaction.get_transactions_for_month_year(transaction_data)
        
        # extracting id and categories
        # id_cat_pairs = []
        # for transaction_ in transactions_to_display:
        #     id_cat_pair = {
        #         "id" : transaction_.id,
        #         "category" : transaction_.category
        #     }
            
        #     id_cat_pairs.append(id_cat_pair)
        
        # print("PAIRS*******************************")
        # print( id_cat_pairs)

        
        categories_from_db = transaction.Transaction.get_all_categories_only()
        
        # checking if we have any data in the database
        if month == None:
            # if no data send the user to the upload page
            return redirect("/expenses_analyst/upload_statement")
        else:
            return render_template("dashboard_edit_categories.html",month = month,year = year,months_years = all_months_years,transactions_from_db = transactions_to_display,categories_to_display = categories_from_db)

# this route update category for a specific transaction
@app.route("/expenses_analyst/update_category" ,methods = ["POST"])
def update_category():
     # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        # id = request.form["transaction_id"]
        # category = request.form["category"]
        # transaction_id = request.form["transaction_id"]
        # print("ID*****  "+ transaction_id)
        # print("CAT*****  "+ category)
        
        category_data = {
            "id" : request.form["transaction_id"] ,
            "category" : request.form["category"]
        }
        # updating
        transaction.Transaction.update_category(category_data)
        
    return redirect("/expenses_analyst/edit_categories")
        
# this route redirect users to the view transactions page
@app.route("/expenses_analyst/view_transactions")
def view_transactions():
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        # retrieve all transactions for the current month
        current_year = transaction.Transaction.get_current_year()
        # dict for current year
        year_data = {
            "year" : current_year
        }
        current_month = transaction.Transaction.get_current_month(year_data)
        # all_months = transaction.Transaction.get_all_months()
        # all_years = transaction.Transaction.get_all_years()
        all_months_years = transaction.Transaction.get_all_years_months_pairs()

        # transaction data
        transaction_data = {
            "month" : current_month,
            "year" : current_year
        }
        transactions_to_display = transaction.Transaction.get_transactions_for_month_year(transaction_data)
        
        # checking if we have any data in the database
        if current_month == None:
            # if no data send the user to the upload page
            return redirect("/expenses_analyst/upload_statement")
        else:
            return render_template("dashboard_view_transactions.html",month = current_month,year = current_year,months_years = all_months_years,transactions_from_db = transactions_to_display)

# this route redirect users to the view transactions page for a specific month
@app.route("/expenses_analyst/view_transactions_month", methods = ["POST"])
def view_transactions_month():
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
         # replace single quotes with double and convert a string dict to dict
        month_year_dict = json.loads((request.form["month_year"]).replace("'",'"'))
        
        year = month_year_dict["year"]
        month = month_year_dict["month"]
        # print("MONTH**" + str(month))
        # print("Year**" + str(year))
        # print("DICT **" + request.form["month_year"])
        

        all_months_years = transaction.Transaction.get_all_years_months_pairs()

        # transaction data
        transaction_data = {
            "month" : month,
            "year" : year
        }
        
        transactions_to_display = transaction.Transaction.get_transactions_for_month_year(transaction_data)
        
        # checking if we have any data in the database
        if month == None:
            # if no data send the user to the upload page
            return redirect("/expenses_analyst/upload_statement")
        else:
            return render_template("dashboard_view_transactions.html",month = month,year = year,months_years = all_months_years,transactions_from_db = transactions_to_display)

# this route redirect users to the upload statement page
@app.route("/expenses_analyst/upload_statement")
def upload_statement_page():
    return render_template("upload_statement.html")

# this method retrieves yearly values for analytics from the database for analysis
@app.route("/expenses-analyst/get_yearly_analysis" ,methods = ["POST"] )
def get_yearly_analysis():    
     # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        data = {
                "id": session.get("user_id")
            }
        year = transaction.Transaction.get_current_year()
        all_years = transaction.Transaction.get_all_years()
        
        # year dictionary for selection
        year_data = {
            "category" : "Income",
            "year" : request.form["year"]
        }
        # retrieve income from the database
        total_income = transaction.Transaction.get_yearly_income(year_data)
        
        # year dictionary for selection
        year_data_expenses = {
            "amount" : 0,
            "year" : request.form["year"]
        }
        
        # retrieve expenses from the database
        total_expenses = transaction.Transaction.get_yearly_expenses(year_data_expenses)
    
        # checking if we have any data in the database
        if year == None:
            # if no data send the user to the upload page
            return redirect("/expenses_analyst/upload_statement")
        else:
            # print("year is:" + str(year))
            return render_template("dashboard_yearly_analysis.html",user_to_display = user.User.get_one_user_by_id(data),year = year_data["year"],all_years_to_display = all_years,total_income = total_income,expenses = total_expenses)

# this method retrieves monthly values for analytics from the database for analysis
@app.route("/expenses-analyst/get_monthly_analysis" ,methods = ["POST"] )
def get_monthly_analysis():    
     # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        data = {
                "id": session.get("user_id")
            }
        # replace single quotes with double and convert a string dict to dict
        month_year_dict = json.loads((request.form["month_year"]).replace("'",'"'))
        
        year = month_year_dict["year"]
        month = month_year_dict["month"]
        # print("MONTH**" + str(month))
        # print("Year**" + str(year))
        # print("DICT **" + request.form["month_year"])
        
        month_year_data = {
            "month" : month,
            "year" : year
        }
        
        # retrieve a list of dictionaries from the database containing months and years
        all_months_years = transaction.Transaction.get_all_years_months_pairs()

        # year dictionary for selection
        month_data_income = {
            "category" : "Income",
            "month": month,
            "year" : year
        }
        # retrieve income from the database
        total_income = transaction.Transaction.get_monthly_income(month_data_income)
        
        # year dictionary for selection
        month_data_expenses = {
            "amount" : 0,
            "month": month,
            "year" : year
        }
        
        # retrieve expenses from the database
        total_expenses = transaction.Transaction.get_monthly_expenses(month_data_expenses)

        # checking if we have any data in the database
        if month == None:
            # if no data send the user to the upload page
            return redirect("/expenses_analyst/upload_statement")
        else:
            return render_template("dashboard_monthly_analysis.html",user_to_display = user.User.get_one_user_by_id(data),month = month,year = year,months_years=all_months_years,total_income = total_income,expenses = total_expenses)
    
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
        # redirecting the user to the yearly analysisi page
    return redirect("/expenses_analyst/dashboards/yearly_analysis")

    
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
        return redirect("/expenses_analyst/login")
    if not bcrypt.check_password_hash(found_user.password,request.form["password"]):
        # flash error message if no match
        user.User.user_login_validation()
        return redirect("/expenses_analyst/login")
    #assigning session to the user
    session["user_id"] = found_user.id
    # redirecting the user to the yearly analysisi page
    return redirect("/expenses_analyst/dashboards/yearly_analysis")

# @app.route("/page4")
# def page4():
#     # check if user is logged in
#     if session.get("user_id")==None: 
#         return redirect("/")
#     else: 
#         data = {
#             "id": session["user_id"]
#         }
#         user_to_display = user.User.get_one_user_by_id(data)
#         # print(f"user is {user_to_display.first_name}")
#         return render_template("page4.html",user_to_display = user.User.get_one_user_by_id(data))

# # this route allows user to access a certain page
# @app.route("/page")
# def page():
#     # check if user is logged in
#     if session.get("user_id")==None:
#         return redirect("/")
#     else:
#         return render_template("page3.html")

# this route clears the sessions
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
# this route redirects the user to the error page if the links is not found
@app.errorhandler(404)
def errors(e):
    return render_template("errorpage.html")