from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
class Category:
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
