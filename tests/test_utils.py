from unittest.mock import Mock, patch

import pandas as pd

from src.utils import get_data_from_file, get_data_json, get_exchange_rate, get_greeting, get_share_price


@patch("src.utils.datetime.datetime")
def test_get_greeting_morning(mock_datetime):
    mock_datetime.now.return_value.hour = 10
    assert get_greeting(), "Доброе утро"


@patch("pandas.read_excel")
def test_get_data_from_file(mock_read_excel):
    mock_read_excel.return_value = pd.DataFrame({"column": [1, 2, 3]})
    result = get_data_from_file()
    assert result.equals(pd.DataFrame({"column": [1, 2, 3]}))


@patch("requests.get")
def test_get_share_price(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"Time Series (5min)": {"2022-01-01 00:00:00": {"4. close": 100.0}}}
    mock_get.return_value = mock_response

    data_stocks = get_data_json()
    data_stocks["user_stocks"] = ["AAPL"]

    result = get_share_price()
    assert result[0]["stock"] == "AAPL"
    assert result[0]["price"] == 100.0


@patch("src.utils.requests.get")
def test_get_exchange_rate(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"Valute": {"USD": {"Value": 70.5}, "EUR": {"Value": 80.2}}}
    mock_get.return_value = mock_response

    data_currencies = {"user_currencies": ["USD", "EUR"]}
    with patch("src.utils.get_data_json", return_value=data_currencies):
        result = get_exchange_rate()
        assert result[0]["currency"] == "USD"
        assert result[0]["rate"] == 70.5
        assert result[1]["currency"] == "EUR"
        assert result[1]["rate"] == 80.2
