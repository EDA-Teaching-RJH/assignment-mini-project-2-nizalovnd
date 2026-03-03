import pdfplumber
import json
import re
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
    "explicit_vertical_lines": [53, 86, 252, 307, 363],  # Date | Description | Amount
    "snap_tolerance": 5,
    "intersection_y_tolerance": 10,
    "explicit_horizontal_lines": [190, 472 ]
}
settings_natwest = {
    "vertical_strategy": "explicit",
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [55, 94, 359, 396, 462],  # Date | Description | Amount
    "snap_tolerance": 5,
    "intersection_y_tolerance": 10,
    #"explicit_horizontal_lines": [190, 472 ]
}


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



def pdf_to_json(file_path):
    #new json file for this file
    intermediate_list = []
    json_filename = "db1.json"
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            if i == 0:
                continue
            page_text = page.extract_text()
            if "Your account in detail" not in page_text or "Your interest rates" in page_text:
                break
            table = page.extract_table(table_settings=settings_aqua)
            intermediate_list.append(table)

    try:
        with open(json_filename, "w") as file:
            json.dump(intermediate_list, file, )
    except IOError:
        print("Error writing json file")


