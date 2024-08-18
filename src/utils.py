import datetime
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

from config import DATA_DIR, LOG_DIR, ROOT_DIR

load_dotenv()
API_KEY = os.getenv("Alpha_Vantage")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    filename=os.path.join(LOG_DIR, "utils.log"),
    encoding="utf-8",
    filemode="w",
)

greetings = logging.getLogger("app_greeting")
card_transactions_ = logging.getLogger("app_card_transactions")
data_json = logging.getLogger("app_data_json")
exchange_rate = logging.getLogger("app_exchange_rate")
share_price = logging.getLogger("app_share_price")
data_from_file = logging.getLogger("app_data_from_file")


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от текущего времени суток."""
    greetings.info("Запрос приветствия")
    greetings.info("Получение времени суток")
    now = datetime.datetime.now().hour
    greetings.info("Время суток получено")
    if 0 <= now < 6:
        greeting = "Доброй ночи"
    elif 6 <= now < 12:
        greeting = "Доброе утро"
    elif 12 <= now < 18:
        greeting = "Добрый день"
    else:
        greeting = "Добрый вечер"
    greetings.info(f"Приветствие возвращено {greeting}")
    return greeting


def get_card_transactions(date: datetime.date) -> tuple:
    """Возвращает словарь с суммами трат по карточкам за указанный месяц и топ 5 транзакций"""
    try:
        card_transactions_.info("Запрос транзакций по картам")
        start_of_month = datetime.datetime(date.year, date.month, 1, 0, 0, 0)
        card_transactions_.info("Создание датафрейма")
        df = get_data_from_file()
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
        df = df[(df["Дата операции"] >= start_of_month) & (df["Дата операции"] <= date)]
        df_filter_by_card = df.dropna(subset="Номер карты")
        filter_df_status = df_filter_by_card[df_filter_by_card["Статус"] == "OK"]
        filter_df = filter_df_status[filter_df_status["Сумма операции"] < 0]
        grouped_df = filter_df.groupby("Номер карты").agg({"Сумма операции": "sum"})
        card_transactions = grouped_df.to_dict(orient="index")
        card_transactions_dict = {key: round(value["Сумма операции"], 2) for key, value in card_transactions.items()}
        card_transactions_.info("Транзакции по картам получены")

        card_transactions_.info("Создание датафрейма для топ транзакции")
        top_transactions_df = df.copy()
        top_transactions = top_transactions_df.nlargest(5, columns="Сумма операции с округлением", keep="last")
        top_transactions_filter = top_transactions[["Дата платежа", "Сумма операции", "Категория", "Описание"]]
        top_transactions_dict = top_transactions_filter.to_dict(orient="records")
        card_transactions_.info("Топ транзакции получены")

        card_transactions_.info("Словари с транзакциями по картам и топ транзакциями возвращены")
        return card_transactions_dict, top_transactions_dict
    except Exception as e:
        card_transactions_.error(e)
        print(e)


def get_data_json() -> dict:
    """Возвращает данные из JSON."""
    data_json.info("Запрос данных пользовательских настроек из JSON")
    path = os.path.join(ROOT_DIR, "user_settings.json")
    with open(path, "r") as f:
        data = json.load(f)
    data_json.info("Данные пользовательских настроек из JSON получены")
    return data


def get_exchange_rate() -> list:
    """Возвращает курс по указанной валюте."""
    try:
        exchange_rate.info("Запрос курса валют")
        exchange_rate.info("Запрос пользовательских настроек по валютам")
        data_currencies = get_data_json()
        exchange_rate.info("Данные пользовательских настроек получены")

        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        data = requests.get(url).json()

        exchange_rate.info("Отправка запроса курса валют")
        currency_list = []
        for currency in data_currencies["user_currencies"]:
            currency_dict = dict()
            currency_dict["currency"] = currency
            currency_dict["rate"] = round(data["Valute"][currency]["Value"], 2)
            currency_list.append(currency_dict)
        exchange_rate.info("Курс валют получен")
        return currency_list
    except Exception as e:
        exchange_rate.error(e)
        print(e)


def get_share_price() -> list:
    """Возвращает цену акции."""
    try:
        share_price.info("Запрос курса акции")
        share_price.info("Запрос пользовательских настроек по акциям")
        data_stocks = get_data_json()
        share_price.info("Данные пользовательских настроек получены")

        share_price.info("Отправка запроса курса акции")
        stocks_list = []
        for stocks in data_stocks["user_stocks"]:
            stocks_dict = {}
            function = "TIME_SERIES_INTRADAY"
            url = (
                f"https://www.alphavantage.co/query?function="
                f"{function}&symbol={stocks}&interval=5min&apikey={API_KEY}"
            )
            r = requests.get(url)
            data = r.json()
            price = list(data["Time Series (5min)"].values())
            stocks_dict["stock"] = stocks
            stocks_dict["price"] = price[0]["4. close"]
            stocks_list.append(stocks_dict)
        share_price.info("Курс акции получен")
        return stocks_list
    except Exception as e:
        share_price.error(e)
        print(e)


def get_data_from_file() -> pd.DataFrame:
    """Возвращает датафрейм из файла."""
    try:
        data_from_file.info("Запрос данных из файла")
        path = os.path.join(DATA_DIR, "operations.xlsx")
        df = pd.read_excel(path)
        data_from_file.info("Данные из файла получены")
        return df
    except Exception as e:
        data_from_file.error(e)
        print(e)


if __name__ == "__main__":
    g = "2021-04-02 23:00:00"
    j = datetime.datetime.strptime(g, "%Y-%m-%d %H:%M:%S")
    # json_data = json.dumps(l, ensure_ascii=False, indent=4)

    print(get_card_transactions(j))
