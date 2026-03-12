import json

from pathlib import Path

from statement_parse import *


base_dir = Path.cwd()

# for iteration through statements
statement_settings = [("aqua", "aqua.pdf", settings_aqua, AquaFilter(), AquaTableFilter(), AquaTransaction()),
                      ("capital" "capital_one.pdf", settings_capital, CapitalFilter(), CapitalTableFilter(), CapitalTransaction()),
                       ("nationwide", "nationwide.pdf", settings_nationwide, NationwideFilter(), NationwideTableFilter(), NationwideTransaction()),
                       ("natwest", "natwest.pdf", settings_natwest, NatwestFilter(), NatwestTableFilter(), NatwestTransaction()),
                       ("revolut", "revolut.pdf", settings_revolut, RevolutFilter(), RevolutTableFilter(), RevolutTransaction())]


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


def main():
    file_rename()
