from flask_app import app
from flask import render_template,redirect,session,request,url_for,flash,jsonify
from flask_app.models import user,transaction
from flask_app.controllers import users

import os
from werkzeug.utils import secure_filename

import pdfplumber,re



# configuring path to save the file
# upload_folder = r"D:\Development\9.CODING_DOJO\6.Projects\expenses_analyst\project_repository\expenses-analyst\uploads"

upload_folder=r"D:\Development\9.CODING_DOJO\6.Projects\1.Solo Project\expenses_analyst\project_repository\expenses-analyst\uploads"

# restriction uploads to pdfs
allowed_extensions = {"pdf"}
# below method checks if uploaded file has the allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
           
# this route will receive uploaded bank statement from frontend
@app.route("/upload", methods = ["POST"])
def upload():
     # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file uploaded')
                return redirect("/expenses_analyst/dashboards/yearly_analysis")
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect("/expenses_analyst/dashboards/yearly_analysis")
            # checking if a file part is present with the allowed extension
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # saving the files
                file.save(os.path.join(upload_folder, filename))
                # getting the path to the saved file
                path = find_file_path()
                # parsing the PDF
                # print(str(path))
                pdf_parser(path)
                # delete all files after parsing no need to store the file
                clear_directory()
        return redirect("/expenses_analyst/dashboards/yearly_analysis")

# this route retrieves list of categories and their total from db
@app.route("/get_all_categories/<int:year>")
def get_all_categories_and_their_total(year):
    # year dictionary
    year_data = {
        "year" : year
    }
    # retrieve categories from db and put the data in JSON format
    categories_and_total_list_JSON = jsonify(transaction.Transaction.get_all_categories_and_their_total_in_a_year(year_data))
    return categories_and_total_list_JSON

# this route retrieves list of categories and their total from db
@app.route("/get_all_categories/<int:month>/<int:year>")
def get_all_categories_and_their_total_in_a_month(month,year):
    # month dictionary
    month_data = {
        "month" : month,
        "year" : year
    }
    # retrieve categories from db and put the data in JSON format
    categories_and_total_list_JSON = jsonify(transaction.Transaction.get_all_categories_and_their_total_in_a_month(month_data))
    return categories_and_total_list_JSON

# this method parses pdf files
def pdf_parser(pdf_file_path):
    with pdfplumber.open(pdf_file_path) as pdf:
        document = pdf.pages
        # getting the number of pages in the document
        maximum_number_of_pages = len(document)
        # this list will store the extracted texts
        page_texts = [ ]
        # period regex
        period_re = re.compile(r"([A-Za-z]{3})(\s\d{1,2}\s\-\s[A-Za-z]{3}\s\d{1,2}\,\s)(\d{4})")
        #date regex
        date_re = re.compile(r"[A-Za-z]{3}\s\d{1,2}\s")
        #amount regex
        amount_re = re.compile(r"(\s[-+]?\s)(\$*\d{1,3}(?:,\d{3})*\.\d{2}) ")   
        # description regex
        # description_re = re.compile(r"^(?!.*\d{3}).*")
        #transaction regex including date and amount
        transaction_re = re.compile(r"([A-Za-z]{3}\s\d{1,2}\s)|((\s[-+]?\s)(\$*\d{1,3}(?:,\d{3})*\.\d{2}) )")
        # ITERATING THROUGH PAGES
        for page_number in range(0,maximum_number_of_pages):
            # print(type(pdf.pages))
            # storing all extracted texts in a list
            page_texts.append(document[page_number].extract_text()) 
            # obtaining the period of the bank statement
            period =  period_re.search(page_texts[0]).group(0).strip()
            # extracting month and year from period and get its numeric value by calling the month converter
            month = transaction.Transaction.month_converter(period_re.search(page_texts[0]).group(1).strip())
            year =  period_re.search(page_texts[0]).group(3).strip()
            # print(f"PERIOD FOR THIS BANK STATEMENT IS : {period}")
            # print(f"MONTH FOR THIS BANK STATEMENT IS : {month}")
            # print(f"YEAR FOR THIS BANK STATEMENT IS : {year}")

            # SEARCHING FOR THE PATTERN
            for line in page_texts[page_number].split("\n"):
                if transaction_re.search(line) and amount_re.search(line):
                    # print(line)
                    # print("****DATE="+ transaction_re.search(line).group(1).strip())
                    # print("****DATE="+ date_re.search(line).group(0).strip())
                    # remove dollar sign,spece and comma and convert amount to float type
                    amount = float((re.sub("\s\$","",amount_re.search(line).group(0).strip()).replace(",","")))
                    # print("****AMOUNT="+ str(amount))
                    # extracting description replace non numeric with space and remove space at the beginning and the end of the string
                    # spaces are used in order to make description readable
                    description=(((re.sub("[^A-Za-z]"," ",line))[3:]).rstrip(" ")).lstrip(" ")
                    # print("********DESCR="+ description)
                    # print(type(line))
                    # print("Month in numeric is" + str(Transaction.month_converter(date_re.search(line).group(0).strip())))
                    # 
                    user_id = str(session.get("user_id"))
                    transaction_data = {
                        "month" : month,
                        "year" : year,
                        "description" : description,
                        "amount" : amount,
                        # run the categorizer method to get the category by passing the description
                        "category" : transaction.Transaction.transaction_categorizer(description),
                        # "category" : "",
                        "user_id" : user_id
                    }
                    # print(transaction_data)
                    # print("********USER_ID IS: " + str(session.get("user_id")))
                    # saving the transactions in the database
                    transaction.Transaction.save_transaction(transaction_data)
                    # insert categories
                    # transaction.Transaction.insert_categories_to_transactions()
                    
# this method searches for the file paths to parse
def find_file_path():
    # iterating through the upload files directory
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder,filename)
        # print("######" + file_path)
        if os.path.isfile(file_path):
            # print("######" + file_path)
            return file_path 
        
# this method clears everything in a directory
def clear_directory():
    # iterating through the upload files directory
    for filename in os.listdir(upload_folder):
        os.remove(os.path.join(upload_folder,filename))

