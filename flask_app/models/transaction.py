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
        self.user = None

        
    # this method creates transaction entry in the database
    @classmethod
    def save_transaction(cls,data):
        query = "INSERT INTO transactions (month,year,description,amount,category,user_id) VALUES(%(month)s,%(year)s,%(description)s,%(amount)s,%(category)s,%(user_id)s)" 
        # retrieving the id of created transaction
        result = connectToMySQL(Transaction.database_name).query_db(query,data)
        return None
    
                    
    # this method converts months from string to numerical values for storing in the database
    @staticmethod
    def month_converter(string_month):
        # regex to extract 3 letters of the month
        # month_re = re.compile(r"[A-Za-z]{3}\s")
        # extracting the 3 letters of the month from string month
        # month_in_letters = month_re.search(string_month).group(0).strip()
        # initializing month dictionary with key value pairs
        months = {
            "Jan" : "1 ",
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
            


