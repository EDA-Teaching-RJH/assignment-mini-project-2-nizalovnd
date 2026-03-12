import json

from multiprocessing import Pool
from pathlib import Path

from statement_parse import *


base_dir = Path.cwd()
statement_dir = Path(base_dir / "statements")
output_dir = Path(base_dir / "output")

# for iteration through statements
statement_settings = [( "aqua.pdf", settings_aqua, AquaFilter(), AquaTableFilter(), AquaTransaction()),
                      ("capital_one.pdf", settings_capital, CapitalFilter(), CapitalTableFilter(), CapitalTransaction()),
                       ("nationwide.pdf", settings_nationwide, NationwideFilter(), NationwideTableFilter(), NationwideTransaction()),
                       ("natwest.pdf", settings_natwest, NatwestFilter(), NatwestTableFilter(), NatwestTransaction()),
                       ("revolut.pdf", settings_revolut, RevolutFilter(), RevolutTableFilter(), RevolutTransaction())]


def file_rename():
    dir_path = statement_dir
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


def process_statements(pdf_name, pdf_settings, page_filter, table_filter, object_creator ):
    
    
        expenses = []
        incomes = []
        pdf_path = statement_dir / pdf_name
        if not pdf_path.exists():
            return incomes, expenses
        

        pdf = PDFProcessor(page_filter, pdf_settings)
        table = TableProcessor(table_filter)

        processed_pages = pdf.process_pdf(pdf_path)

        for page in processed_pages:
            for row in table.process(page):
                transaction = object_creator.transaction(row)
                if transaction is None:
                    continue
                transaction_dict = {"date": transaction.date.strftime("%Y-%m-%d"),
                                    "name": transaction.name,
                                    "account": transaction.account,
                                    "amount": transaction.amount}
                if isinstance(transaction, Expense):
                    transaction_dict["category"] = transaction.category
                    transaction_dict["card_type"] = transaction.card_type
                    expenses.append(transaction_dict)
                elif isinstance(transaction, Income):
                    incomes.append(transaction_dict)
                else:
                    pass
        return incomes, expenses
        #TODO convert to dict form for json serialization

        

        
def main():
    
    
    file_rename()

    with Pool(processes=5) as pool:

   #     for pdf_statement, pdf_settings, page_filter, table_filter, object_creator in statement_settings:
            
   
        results = pool.starmap(process_statements, statement_settings)
            
       # expenses =  [expenses for _, expenses in results]
        #final_expenses = [*e for e in expenses]
    expenses = [e for _, expenses in results for e in expenses]
    incomes = [i for incomes, _ in results for i in incomes]


    with open("expenses.json", "w") as file:
            json.dump(expenses, file)

    with open("incomes.json", "w") as file:
        json.dump(incomes, file)