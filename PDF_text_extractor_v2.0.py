# A SCRIPT TO EXTRACT BANK STATEMENT TRANSACTIONS AND CONVERT THEM TO EXCEL FORMAT
import pdfplumber
import pandas as pd
import re
from collections import namedtuple

# CREATING A NAMED TUPLE FOR OUR DATA
column_names = namedtuple('column_names','Activity  Date  Amount  Balance')


with pdfplumber.open("D:/Development/2.Software-Development Projects/Data Science_Python/PDFTextExtractor_V2/test_docs/January 2022.pdf") as pdf:
    document = pdf.pages
    # GETTING THE NUMBER OF PAGES
    maximum_number_of_pages = len(document)
    # CREATING AN EMPTY LIST 
    page_texts = [ ]
    # ITERATING THROUGH PAGES
    for page_number in range(0,maximum_number_of_pages):
        # print(type(pdf.pages))
        # APPEND PAGES TO PAGE TEXTS OBJECT-LIST STORING ALL TEXT PAGE SPECIFIC
        page_texts.append(document[page_number].extract_text()) 
        # SEPARATING THE TEXTS FOR EACH PAGE INTO NEW LINES
        # print extracted texts from each page
        # print(page_texts[page_number].split("\n"))
        # COMPILING A REGEX FOR BANK TRANSACTION
        # AMOUNTS  (\s[-+]?\s)(\$*\d{1,3}(?:,\d{3})*\.\d{2})
        # BALANCE  (\s\$*\d{1,3}(?:,\d{3})*\.\d{2})
        # POS AND NEG SIGNS  \s[-+]?\s
        # SIGN AMOUNT AND BALANCE (\s[-+]?\s)(\$*\d{1,3}(?:,\d{3})*\.\d{2})(\s\$*\d{1,3}(?:,\d{3})*\.\d{2})
        # DATES [A-Za-z]{3}\s\d{1,2}\s
        bank_transaction_regex=re.compile(r'(\d{2}/\d{2}/\d{4}) (\$\(\d{1,3}(?:,\d{3})*\.\d{2}\)|\$\d{1,3}(?:,\d{3})*\.\d{2}) (\$*\d{1,3}(?:,\d{3})*\.\d{2})')
        # COMPILE REGEX FOR ACTIVITY ONLY
        activity_re = re.compile(r'[^\d{2}/\d{2}/\d{4}]+')
        # COMPILE REGEX FOR date ONLY
        date_re = re.compile(r'\d{2}/\d{2}/\d{4} ')
        # COMPILE REGEX FOR amount ONLY
        amount_re = re.compile(r'\$\(\d{1,3}(?:,\d{3})*\.\d{2}\)|\$\d{1,3}(?:,\d{3})*\.\d{2} ')
        # COMPILE REGEX FOR balance ONLY
        balance_re = re.compile(r' \$*\d{1,3}(?:,\d{3})*\.\d{2}')
        # SEARCHING FOR THE PATTERN
        for line in page_texts[page_number].split("\n"):
            if balance_re.search(line):
                # print(line)
                pass
            
    print(page_texts[1])



# FINAL REGEX
 # DATES 
 # '[A-Za-z]{3}\s\d{1,2}\s'
#  AMOUNT
# '\$\(\d{1,3}(?:,\d{3})*\.\d{2}\)|\$\d{1,3}(?:,\d{3})*\.\d{2} '
 
        