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
    "intersection_y_tolerance": 10,
    #"explicit_horizontal_lines": [190, 472 ]
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
    def keep(list):
        pass

class AquaTableFilter(TableFilter):
    def keep(list):
        if re.search(r"^\d+\s[a-zA-Z]{3}\s20\d{2}",list[0]):
            return True
        else:
            return False

class CapitalTableFilter(TableFilter):
    def keep(list):
        if re.search(r"^\d+\s[a-zA-Z]{3}",list[0]):
            return True
        else:
            return False

class NationwideTableFilter(TableFilter):
    def keep(list):
        if re.search(r"\d+.\d{2}$", list[2]) or re.search(r"\d+.\d{2}$", list[3]):
            return True
        else:
            return False



class NatwestTableFilter(TableFilter):
    def keep(list):
        if re.search(r"\d+.\d{2}$", list[2]) or re.search(r"\d+.\d{2}$", list[3]):
            return True
        else:
            return False


class RevolutTableFilter(TableFilter):
    def keep(list):
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


"""
        try:
            with open(json_filename, "w") as file:
                json.dump(intermediate_list, file, )
        except IOError:
            print("Error writing json file")
"""



    

