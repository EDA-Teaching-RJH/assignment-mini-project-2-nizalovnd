import pytest

from datetime import datetime
from unittest.mock import patch, MagicMock

import main as main_script

from main import file_rename, process_statements, bubble_sort, main



#helper function for test_file_rename that mocks a file and subs a temporary dir for the statement_dir in the main file
def rename_helper_func(fake_path, filename):
    fake_file = fake_path / filename
    fake_file.touch()
    with patch.object(main_script, "statement_dir", fake_path):
        file_rename()


#tests the file_rename function 
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
    rename_helper_func(tmp_path, "unknown_file.pdf")
    assert (tmp_path / "unknown_file.pdf").exists()



def test_process_statements(tmp_path):
    fake_file = tmp_path / "aqua.pdf"
    fake_file.touch()
    
    with patch.object(main_script, "statement_dir", tmp_path):
        incomes, expenses = process_statements("random.pdf", main_script.settings_aqua, main_script.AquaFilter(), main_script.AquaTableFilter(), main_script.AquaTransaction())
        assert incomes == []
        assert expenses == []

    fake_file = tmp_path / "revolut.pdf"
    fake_file.touch()

    mock_pdf_processor = MagicMock()
    mock_table_processor = MagicMock()
    mock_page_filter = MagicMock()
    mock_table_filter = MagicMock()
    mock_object_creator = MagicMock()
        
    mock_income = main_script.Income(datetime(2026, 3, 5), "Mock Income", "Revolut", 1000.00)

    mock_object_creator.transaction.return_value = mock_income
    mock_pdf_processor.process_pdf.return_value = [["3 Mar", "Mock Income", "Revolut", 1000.00]]
    mock_table_processor.process.return_value = [["3 Mar", "Mock Income", "Revolut", 1000.00]]

    with patch.object(main_script, "statement_dir", tmp_path) , patch("main.PDFProcessor", return_value = mock_pdf_processor), patch("main.TableProcessor", return_value = mock_table_processor):
        
        incomes, expenses = main_script.process_statements("revolut.pdf", main_script.settings_revolut, mock_page_filter, mock_table_filter, mock_object_creator)

    assert incomes[0]["date"] == "2026-03-05"
    assert incomes[0]["name"] == "Mock Income"
    assert incomes[0]["account"] == "Revolut"
    assert incomes[0]["amount"] == 1000.00
    assert expenses == []

    mock_expense = main_script.Expense(datetime(2026, 3, 5), "Mock Expense", "Revolut", -100.00, "expense", "credit")

    mock_object_creator.transaction.return_value = mock_expense
    mock_pdf_processor.process_pdf.return_value = [["3 Mar", "Mock Expense", "Revolut", -100.00]]
    mock_table_processor.process.return_value = [["3 Mar", "Mock Expense", "Revolut", -100.00]]

    with patch.object(main_script, "statement_dir", tmp_path), patch("main.PDFProcessor", return_value = mock_pdf_processor), patch("main.TableProcessor", return_value = mock_table_processor):
        
        

        incomes, expenses = main_script.process_statements("revolut.pdf", main_script.settings_revolut, mock_page_filter, mock_table_filter, mock_object_creator)

    assert expenses[0]["date"] == "2026-03-05"
    assert expenses[0]["name"] == "Mock Expense"
    assert expenses[0]["account"] == "Revolut"
    assert expenses[0]["amount"] == -100.00
    assert expenses[0]["category"] == "expense"
    assert expenses[0]["card_type"] == "credit"
    assert incomes == []



   
def test_bubble_sort():
    assert bubble_sort([]) == []
    assert bubble_sort([{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}]) == [{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}]
    assert bubble_sort([{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}, {"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"} ]) == [{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"},{"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"} ]
    assert bubble_sort([{"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"}, {"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}]) == [{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"},{"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"} ]
   
def test_main(tmp_path):

    mock_pool = MagicMock()
    mock_pool.__enter__.return_value = mock_pool
    mock_pool.starmap.return_value = [([],[])] * 5

    with patch("main.file_rename"), patch("main.Pool", return_value = mock_pool), patch("json.dump"), patch("builtins.open", MagicMock()):
        main()
    

