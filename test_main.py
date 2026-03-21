import pytest
import main as main_script

from main import file_rename, process_statements, bubble_sort, main

from unittest.mock import patch

def rename_helper_func(fake_path, filename):
    fake_file = fake_path / filename
    fake_file.touch()
    with patch.object(main_script, "statement_dir", fake_path):
        main_script.file_rename()


def test_file_rename(tmp_path):
    rename_helper_func(tmp_path, "account_statement.pdf")
    assert (tmp_path/ "revolut.pdf").exists()
    
    rename_helper_func(tmp_path, "2025-12-12statement.pdf")
    assert (tmp_path / "aqua.pdf").exists()
    rename_helper_func(tmp_path, "2025_12_12statement.pdf")
    assert (tmp_path / "capital_one.pdf").exists()
    rename_helper_func(tmp_path, "Jan 2026 Statement.pdf")
    assert (tmp_path / "nationwide.pdf").exists()
    rename_helper_func(tmp_path, "Statement_23452345_123feb.pdf")
    assert (tmp_path / "natwest.pdf").exists()
    #TODO find out how to mock statement subdir and mock the pdf files to rename

def test_process_statements():
    pass

def test_bubble_sort():
    assert bubble_sort([]) == []
    assert bubble_sort([{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}]) == [{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}]
    assert bubble_sort([{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}, {"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"} ]) == [{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"},{"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"} ]
    assert bubble_sort([{"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"}, {"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}]) == [{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"},{"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"} ]
   
def test_main():
    pass

