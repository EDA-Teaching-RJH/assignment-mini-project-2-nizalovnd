import json

from pathlib import Path

from statement_parse import *


base_dir = Path.cwd()
statement_dir = Path(base_dir / "statements")

# for iteration through statements
statement_settings = [("aqua", "aqua.pdf", settings_aqua, AquaFilter(), AquaTableFilter(), AquaTransaction()),
                      ("capital" "capital_one.pdf", settings_capital, CapitalFilter(), CapitalTableFilter(), CapitalTransaction()),
                       ("nationwide", "nationwide.pdf", settings_nationwide, NationwideFilter(), NationwideTableFilter(), NationwideTransaction()),
                       ("natwest", "natwest.pdf", settings_natwest, NatwestFilter(), NatwestTableFilter(), NatwestTransaction()),
                       ("revolut", "revolut.pdf", settings_revolut, RevolutFilter(), RevolutTableFilter(), RevolutTransaction())]


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


def main():
    expenses = []
    incomes = []
    file_rename()

    for bank, pdf_statement, pdf_settings, page_filter, table_filter, object_creator in statement_settings:
        pdf_path = statement_dir / pdf_statement
        #TODO check exists

        pdf = PDFProcessor(page_filter, pdf_settings)
        table = TableProcessor(table_filter)

        processed_pages = pdf.process_pdf(pdf_path)

        for page in processed_pages:
            for row in table.process(page):
                transaction = object_creator.transaction(row)\
                if isinstance(transaction, Expense):
                    expenses.append(transaction)
                elif isinstance(transaction, Income):
                    incomes.append(transaction)
                else:
                    pass
        #TODO convert to dict form for json serialization
        

