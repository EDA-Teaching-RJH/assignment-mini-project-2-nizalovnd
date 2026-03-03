import pdfplumber
from pathlib import Path

class Transaction():
    def __init__(self, date,  account, amount):
        self.date = date
        self.account = account
        self.amount = amount

class Income(Transaction):
    def __init__(self, date, account, amount, name):
        super.__init__(date, account, amount)
        self.name = name

class Expense(Transaction):
    def __init__(self, date, account, amount, category, card_type):
        super.__init__(date, account, amount)
        self.category = category
        self.card_type = card_type


def pdf_to_json(file_path):
    #new json file for this file
    with pdfplumber.open(file_path) as pdf:
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            table = page.extract_table()





