from flask_app import app
from flask import render_template,redirect,session,request,url_for,flash
from flask_app.models import user,transaction
from flask_app.controllers import users

import os
from werkzeug.utils import secure_filename

import pdfplumber
import re

# configuring path to save the file
upload_folder = r"D:\Development\9.CODING_DOJO\6.Projects\expenses_analyst\project_repository\expenses-analyst\uploads"
# restriction uploads to pdfs
allowed_extensions = {"pdf"}
# below method checks if uploaded file has the allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
           
# this route will receive uploaded bank statement from frontend
@app.route("/upload", methods = ["POST"])
def upload():
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
            pdf_parser(r"D:\Development\9.CODING_DOJO\6.Projects\expenses_analyst\project_repository\expenses-analyst\uploads\April_2022.pdf")
    return redirect("/expenses_analyst/dashboards/yearly_analysis")

# this method parses pdf files
def pdf_parser(pdf_file_path):
    with pdfplumber.open(pdf_file_path) as pdf:
        document = pdf.pages
        # getting the number of pages in the document
        maximum_number_of_pages = len(document)
        # this list will store the extracted texts
        page_texts = [ ]
            # ITERATING THROUGH PAGES
        for page_number in range(0,maximum_number_of_pages):
        # print(type(pdf.pages))
            # storing all extracted texts in a list
            page_texts.append(document[page_number].extract_text()) 
            #date regex
            date_re = re.compile(r"[A-Za-z]{3}\s\d{1,2}\s")
            #amount regex
            amount_re = re.compile(r"(\s[-+]?\s)(\$*\d{1,3}(?:,\d{3})*\.\d{2}) ")   
        # SEARCHING FOR THE PATTERN
        for line in page_texts[page_number].split("\n"):
             if date_re.search(line):
                # print(line)
                pass
            
        # print(page_texts[1])

