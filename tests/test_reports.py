import json

import pandas as pd

from src.reports import spending_by_weekday


def test_spending_by_weekday():
    transactions = pd.DataFrame(
        {
            "Дата операции": [
                "2022-01-01 12:00:00",
                "2022-02-01 12:00:00",
                "2022-03-01 12:00:00",
                "2022-04-01 12:00:00",
                "2022-05-01 12:00:00",
                "2022-06-01 12:00:00",
                "2022-07-01 12:00:00",
                "2022-08-01 12:00:00",
                "2022-09-01 12:00:00",
            ],
            "Сумма операции": [100, 200, 300, 400, 500, 600, 700, 800, 900],
        }
    )
    date = "2022-02-20 23:00:00"
    result = spending_by_weekday(transactions, date)
    assert result == json.dumps(
        {
            "Понедельник": 300.0,
            "Вторник": 400.0,
            "Среда": 500.0,
            "Четверг": 600.0,
            "Пятница": 700.0,
            "Суббота": 450.0,
            "Воскресенье": 550.0,
        },
        ensure_ascii=False,
        indent=4,
    )


def test_spending_by_weekday_date_in_future():
    transactions = pd.DataFrame(
        {
            "Дата операции": ["2020-01-01 12:00:00", "2020-02-01 12:00:00", "2020-03-01 12:00:00"],
            "Сумма операции": [100, 200, 300],
        }
    )
    date = "2022-02-20 23:00:00"
    result = spending_by_weekday(transactions, date)
    assert result == json.dumps({})
