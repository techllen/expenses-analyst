from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

import re

class Transaction:
    # initializing database name variable
    database_name = "expense_analyst_db"

    def __init__(self,data):
        self.id = data["id"]
        self.month = data["month"]
        self.year = data["year"]
        self.description = data["description"]
        self.amount = data["amount"]
        self.category = data["category"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = data["user_id"]

        
    # this method creates transaction entry in the database
    @classmethod
    def save_transaction(cls,data):
        query = "INSERT INTO transactions (month,year,description,amount,category,user_id) VALUES(%(month)s,%(year)s,%(description)s,%(amount)s,%(category)s,%(user_id)s)" 
        # retrieving the id of created transaction
        result = connectToMySQL(Transaction.database_name).query_db(query,data)
        return None
    
    # this retrieves transactions for specific month
    @classmethod
    def get_transactions_for_month_year(cls,data):
        query = "SELECT * FROM transactions WHERE month = %(month)s AND year = %(year)s" 
        # query = "SELECT * FROM transactions WHERE month = 11 AND year = 2021" 
        transactions_from_db = connectToMySQL(Transaction.database_name).query_db(query,data)
        transactions_list = [ ]
        # checking if we found any transaction
        if transactions_from_db == False:
            return None
        else:
            # turning car results to objects
            for transaction in transactions_from_db:
                # print(transaction)
                # create a transaction object
                this_transaction = cls(transaction)
                # appending the objects to the list
                transactions_list.append(this_transaction)
            # returning list of transaction objects
        return transactions_list
    
     # this retrieves transactions in between months
    @classmethod
    def get_transactions_from_to(cls,data):
        query = "SELECT * FROM transactions WHERE BETWEEN month = %(start_month)s AND month = %(end_month)s" 
        transactions_from_db = connectToMySQL(Transaction.database_name).query_db(query,data)
        transactions_list_btn = [ ]
        # checking if we found any transaction
        if len(transactions_from_db) == 0:
            return None
        else:
            # turning car results to objects
            for transaction in transactions_from_db:
                # create a transaction object
                this_transaction = cls(transaction)
                # appending the objects to the list
                transactions_list_btn.append(this_transaction)
            # returning list of transaction objects
        return transactions_list_btn
    
    # this retrieves a current year from the database
    @classmethod
    def get_current_year(cls):
        query = "SELECT MAX(year) as current_year FROM(SELECT year FROM transactions AS years GROUP BY year) AS year" 
        current_year = connectToMySQL(Transaction.database_name).query_db(query)
        # print("++YT IS:" + str(type(current_year)))
        if current_year == False:
            return None
        else:
            year = current_year[0]["current_year"]
            return year
    
    # this retrieves a current month from the database
    @classmethod
    def get_current_month(cls,data):
        query = "SELECT MAX(month) as current_month FROM(SELECT month FROM transactions AS months WHERE year = %(year)s  GROUP BY month) AS month" 
        current_month = connectToMySQL(Transaction.database_name).query_db(query,data)
        # print("++YT IS:" + str(type(current_month)))
        if current_month == False:
            return None
        else:
            month = current_month[0]["current_month"]
            return month
    
    # this retrieves all years from the database
    @classmethod
    def get_all_years(cls):
        query = "SELECT year FROM transactions GROUP BY year ORDER BY year DESC" 
        years_from_db = connectToMySQL(Transaction.database_name).query_db(query)
        # print(years_from_db)
        # empty list to hold the years
        years = [ ]
        # convert db years to list
        for year in years_from_db:
            years.append(year)
            # print("YEAR:" + str(year))
        return years
    
    # this retrieves all months from the database
    @classmethod
    def get_all_months(cls):
        query = "SELECT month FROM transactions GROUP BY month ORDER BY month ASC" 
        months_from_db = connectToMySQL(Transaction.database_name).query_db(query)
        # empty list to hold the months
        months = [ ]
        # convert db months to list
        for month in months_from_db:
            months.append(month)
        return months
    
    # this retrieves all the incomes from the database
    @classmethod
    def get_yearly_income(cls,data):
        query = "SELECT amount FROM transactions WHERE category = %(category)s AND year = %(year)s " 
        yearly_incomes_from_db = connectToMySQL(Transaction.database_name).query_db(query,data)
        total_income  = 0 
        if yearly_incomes_from_db == False:
            return None
        else:
            for year_income_from_db in yearly_incomes_from_db:
                # print(year_income_from_db["amount"])
                total_income += year_income_from_db["amount"]
            # print("####total is:" + str(total_income))
            return total_income
        
    # this retrieves all the expenses from the database
    @classmethod
    def get_yearly_expenses(cls,data):
        query = "SELECT amount FROM transactions WHERE amount < %(amount)s  AND year = %(year)s " 
        yearly_expenses_from_db = connectToMySQL(Transaction.database_name).query_db(query,data)
        total_expenses  = 0 
        if yearly_expenses_from_db == False:
            return None
        else:
            # print("items " + str(len(yearly_expenses_from_db)))
            for year_expense_from_db in yearly_expenses_from_db:
                # print(year_expense_from_db["amount"])
                total_expenses += year_expense_from_db["amount"]
            # print("####total is:" + str(total_expenses))
            return total_expenses
    
    #this method gets all categories and their total values from the database 
    @classmethod
    def get_all_categories_and_their_total_in_a_year(data):
        query = "SELECT category, SUM(amount) AS category_total FROM transactions WHERE year = %(year)s GROUP BY category " 
        category_and_their_total_from_db = connectToMySQL(Transaction.database_name).query_db(query,data)
        if category_and_their_total_from_db == False:
            return None
        else:
            for category_and_total in category_and_their_total_from_db:
                

    
                    
    # this method converts months from string to numerical values for storing in the database
    @staticmethod
    def month_converter(string_month):
        # regex to extract 3 letters of the month
        # month_re = re.compile(r"[A-Za-z]{3}\s")
        # extracting the 3 letters of the month from string month
        # month_in_letters = month_re.search(string_month).group(0).strip()
        # initializing month dictionary with key value pairs
        months = {
            "Jan" : "1",
            "Feb" : "2",
            "Mar" : "3",
            "Apr" : "4",
            "May" : "5",
            "Jun" : "6",
            "Jul" : "7",
            "Aug" : "8",
            "Sep" : "9",
            "Oct" : "10",
            "Nov" : "11",
            "Dec" : "12"
        }
        
        # iterating through the months dictionary and convert month in letters to numerals using key value pairs
        for month_key,month_numeric in months.items():
            if string_month == month_key:
                return month_numeric
            
    # this method categorizes the transactions description
    @staticmethod
    def transaction_categorizer(transaction_description):
        # transaction categories dictionary
        category = {
            "HEALTHEFTPYMT" : "Income ",
            "ASSOCSPAYROLL" : "Icome",
            "DISCOVERYPLUS" : "Entertainment ",
            "SXCW" : "Fuel ",
            "CAPITALONEMOBILEPMT" : "Credit Cards",
            "Fuel" : "Fuel",
            "ALDIBURLINGTONNCUS" : "Grocery", 
            "DUKE" : "Electricity"    
        }
        
        # iterating through the category dictionary to get respective categories for transactions
        for category_keyword,category in category.items():
            # searching for keywords in descriptions
            if category_keyword in transaction_description:
                return category
            # return no value if no keyword has been configured yet
            else:
                return " "
            
        


