import pdfplumber
import json
import re
from datetime import datetime
from pathlib import Path

base_dir = Path.cwd()


settings_aqua = {
    "vertical_strategy": "explicit",
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [28, 95, 500, 568],
    "snap_tolerance": 5,
    "intersection_y_tolerance": 10,
    "explicit_horizontal_lines": [795]
}
settings_capital = {
    "vertical_strategy": "explicit",
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [43, 72, 295, 355, 395], 
    "snap_tolerance": 5,
    "intersection_y_tolerance": 10,
    "explicit_horizontal_lines": [190, 472 ]
}

settings_nationwide = {
    "vertical_strategy": "explicit",
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [53, 86, 252, 307, 363], 
    "snap_tolerance": 5,
    "intersection_y_tolerance": 10,
    "explicit_horizontal_lines": [190, 472 ]
}
settings_natwest = {
    "vertical_strategy": "explicit",
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [55, 94, 359, 396, 462], 
    "snap_tolerance": 5,
    "intersection_y_tolerance": 10
}
settings_revolut = {
    "vertical_strategy": "explicit",
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [40, 94, 329, 396, 462],  
    "snap_tolerance": 5,
    "intersection_y_tolerance": 10,
    "explicit_horizontal_lines": [ 732 ]
}

class Transaction():
    def __init__(self, date, name, account, amount):
        self.date = date
        self.name = name
        self.account = account
        self.amount = amount

class Income(Transaction):
    def __init__(self, date, name, account, amount):
        super().__init__(date, name, account, amount)
        

class Expense(Transaction):
    def __init__(self, date, name, account, amount, category, card_type):
        super().__init__(date, name, account, amount)
    
        self.category = category
        self.card_type = card_type

def file_rename():
    dir_path = Path(base_dir/"statements")
    for file in dir_path.iterdir():
        if not file.is_file():
            continue
        elif re.search(r"\Aaccount",file.name):
            #revolut
            new_name = dir_path / "revolut.pdf"
            file.rename(new_name)
        elif re.search(r"\d{4}-\d{2}-\d{2}",file.name):
            #aqua
            new_name = dir_path / "aqua.pdf"
            file.rename(new_name)
        elif re.search(r"\d{4}_\d{2}_\d{2}",file.name):
            #capital_one
            new_name = dir_path / "capital_one.pdf"
            file.rename(new_name)
        
        elif re.search(r"\d{4}\sStatement.pdf\Z",file.name):
            #nationwide
            new_name = dir_path / "nationwide.pdf"
            file.rename(new_name)
        elif re.search(r"\bStatement",file.name):
            #natwest
            new_name = dir_path / "natwest.pdf"
            file.rename(new_name)
        else:
            print("Unknown Statement")
            continue

class PageFilter():
    def keep(self, page):
        pass

class AquaFilter(PageFilter):
    def keep(self, page, i):
        if i == 0:
            return False
        page_text = page.extract_text()
        if "Your account in detail" not in page_text or "Your interest rates" in page_text:
            return False
        else:
            return True

        
class CapitalFilter(PageFilter):
    def keep(self, page, i):
        if i == 0:
            return False
        else:
            return True
        
class NationwideFilter(PageFilter):
    def keep(self, page, i):
        page_text = page.extract_text()
        if "Balance from statement" not in page_text:
            return False
        else:
            return True

class NatwestFilter(PageFilter):
    def keep(self, page, i):
        page_text = page.extract_text()
        if "Dispute Resolution" in page_text:
            return False
        else:
            return True
class RevolutFilter(PageFilter):
    def keep(self, page, i):
        return True

class PDFProcessor():
    def __init__ (self, filter: PageFilter, table_settings):
        self.filter = filter
        self.table_settings = table_settings
    
    def process_pdf(self, file_path):
        intermediate_list = []
        #json_filename = "db1.json"
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                if not self.filter.keep(page, i):
                    continue
                table = page.extract_table(table_settings=self.table_settings)
                intermediate_list.append(table)

        return intermediate_list


class TableFilter():
    def keep(self, list):
        pass

class AquaTableFilter(TableFilter):
    def keep(self, list):
        if re.search(r"^\d+\s[a-zA-Z]{3}\s20\d{2}",list[0]):
            return True
        else:
            return False

class CapitalTableFilter(TableFilter):
    def keep(self, list):
        if re.search(r"^\d+\s[a-zA-Z]{3}",list[0]):
            return True
        else:
            return False

class NationwideTableFilter(TableFilter):
    def keep(self, list):
        if re.search(r"\d+.\d{2}$", list[2]) or re.search(r"\d+.\d{2}$", list[3]):
            return True
        else:
            return False



class NatwestTableFilter(TableFilter):
    def keep(self, list):
        if re.search(r"\d+.\d{2}$", list[2]) or re.search(r"\d+.\d{2}$", list[3]):
            return True
        else:
            return False


class RevolutTableFilter(TableFilter):
    def keep(self, list):
        if re.search(r"^\d+\s[a-zA-Z]{3}\s20\d{2}",list[0]):
            return True
        else:
            return False

class TableProcessor():
    def __init__(self, filter: TableFilter):
        self.filter = filter

    def process(self, table):
        intermediate_list = []
        for sublist in table:
            if not self.filter.keep(sublist):
                continue
            else:
                intermediate_list.append(sublist)
        return intermediate_list


class RowToObject():
    def transaction(self, row) -> Transaction:
        pass

class AquaTransaction(RowToObject):
    def transaction(self, row):
        date_old = row[0]
        date_new = datetime.strptime(date_old, "%d %b %Y")
        name = row[1]
        amount_old = re.match(r"\d+\.\d{2}", row[2])
        if amount_old:
            amount_new = float(amount_old.group()) * -1
        expense = Expense(date_new, name, "Aqua", amount_new, "expense", "credit")
        return expense

class CapitalTransaction(RowToObject):
    def transaction(self, row):
        date_old = row[0]
        date_new = datetime.strptime(date_old, "%d %b")
        name = row[1]
        if not row[3] == "":

            amount_old = re.match(r"\d+\.\d{2}", row[3])
            if amount_old:
                amount_new = float(amount_old.group()) * -1
            expense = Expense(date_new, name, "Capital", amount_new, "expense", "credit")
            return expense

class NatwestTransaction(RowToObject):
    #this clss needs to persists over all transactions in the natwest statement, so that there is a variable last seen date that can fill in the date for transactions that have the date cell blank
    def __init__(self):
        self.last_date = None

    def transaction(self, row):
        if row[0] != "":
            self.last_date = datetime.strptime(row[0], "%d %b")
        if self.last_date == None:
            return None
        name = row[1]
        if not row[2] == "":

            amount_old = re.match(r"\d+\.\d{2}", row[2])
            if amount_old:
                amount_new = float(amount_old.group())
            income = Income(self.last_date, name, "Natwest", amount_new)
            return income
        
        if not row[3] == "":

            amount_old = re.match(r"\d+\.\d{2}", row[3])
            if amount_old:
                amount_new = float(amount_old.group()) * -1
            expense = Expense(self.last_date, name, "Natwest", amount_new, "expense", "debit")
            return expense
        #need logic for replicating date for same day transactions

class NationwideTransaction(RowToObject):
    def transaction(self, row):
        date_old = row[0]
        date_new = datetime.strptime(date_old, "%d %b")
        name = row[1]
        if not row[2] == "":

            amount_old = re.match(r"\d+\.\d{2}", row[2])
            if amount_old:
                amount_new = float(amount_old.group())
            income = Income(date_new, name, "Nationwide", amount_new)
            return income
        
        if not row[3] == "":

            amount_old = re.match(r"\d+\.\d{2}", row[3])
            if amount_old:
                amount_new = float(amount_old.group()) * -1
            expense = Expense(date_new, name, "Nationwide", amount_new, "expense", "debit")
            return expense

class RevolutTransaction(RowToObject):
    def transaction(self, row):
        date_old = row[0]
        date_new = datetime.strptime(date_old, "%d %b %Y")
        name = row[1]
        if not row[2] == "":

            amount_old = re.match(r"\d+\.\d{2}", row[2])
            if amount_old:
                amount_new = float(amount_old.group())
            income = Income(date_new, name, "Revolut", amount_new)
            return income
        
        if not row[3] == "":

            amount_old = re.match(r"\d+\.\d{2}", row[3])
            if amount_old:
                amount_new = float(amount_old.group()) * -1
            expense = Expense(date_new, name, "Revolut", amount_new, "expense", "debit")
            return expense

#separate json files for expenses and income
#do i need income file?


"""
        try:
            with open(json_filename, "w") as file:
                json.dump(intermediate_list, file, )
        except IOError:
            print("Error writing json file")
"""



    

