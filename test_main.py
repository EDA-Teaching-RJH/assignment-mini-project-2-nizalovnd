from main import file_rename, process_statements, bubble_sort, main

def test_file_rename():
    pass

def test_process_statements():
    pass

def test_bubble_sort():
    assert bubble_sort([]) == []
    assert bubble_sort([{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}]) == [{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}]
    assert bubble_sort([{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}, {"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"} ]) == [{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"},{"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"} ]
    assert bubble_sort([{"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"}, {"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"}]) == [{"date": "2026-01-08", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -0.35, "category": "expense", "card_type": "credit"},{"date": "2026-01-09", "name": "Millevoglie Venezia ITA\nCurrency conversion rate 4,00 EUR @ 1.1494", "account": "Aqua", "amount": -3.48, "category": "expense", "card_type": "credit"}, {"date": "2026-01-10", "name": "Foreign Exchange Conversion Charge", "account": "Aqua", "amount": -1.0, "category": "expense", "card_type": "credit"} ]
   
def test_main():
    pass

