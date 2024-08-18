import datetime
import json
from unittest.mock import patch

from src.views import home_page


@patch("src.views.get_card_transactions")
@patch("src.views.get_greeting")
@patch("src.views.get_exchange_rate")
@patch("src.views.get_share_price")
def test_home_page(mock_get_share_price, mock_get_exchange_rate, mock_get_greeting, mock_get_card_transactions):
    mock_get_greeting.return_value = "Доброе утро"
    mock_get_exchange_rate.return_value = [{"currency": "USD", "rate": 70.5}, {"currency": "EUR", "rate": 80.2}]
    mock_get_share_price.return_value = [{"stock": "AAPL", "price": 100.0}, {"stock": "AMZN", "price": 200.0}]

    mock_get_card_transactions.return_value = (
        {"1234": 100.0, "5678": 200.0},
        [
            {
                "Дата платежа": "01.04.2021",
                "Сумма операции": -1100.0,
                "Категория": "Развлечения",
                "Описание": "Яндекс.Афиша",
            },
            {
                "Дата платежа": "02.04.2021",
                "Сумма операции": -599.9,
                "Категория": "Супермаркеты",
                "Описание": "Prisma",
            },
        ],
    )

    expected_data = json.dumps(
        {
            "greeting": "Доброе утро",
            "cards": [
                {"last_digits": "1234", "total_spent": 100.0, "cashback": 1.0},
                {"last_digits": "5678", "total_spent": 200.0, "cashback": 2.0},
            ],
            "top_transactions": [
                {"date": "01.04.2021", "amount": -1100.0, "category": "Развлечения", "description": "Яндекс.Афиша"},
                {"date": "02.04.2021", "amount": -599.9, "category": "Супермаркеты", "description": "Prisma"},
            ],
            "currency_rates": [{"currency": "USD", "rate": 70.5}, {"currency": "EUR", "rate": 80.2}],
            "stock_prices": [{"stock": "AAPL", "price": 100.0}, {"stock": "AMZN", "price": 200.0}],
        },
        ensure_ascii=False,
        indent=4,
    )

    date = datetime.datetime.strptime("2020-03-03 23:00:00", "%Y-%m-%d %H:%M:%S")

    assert home_page(date) == expected_data
