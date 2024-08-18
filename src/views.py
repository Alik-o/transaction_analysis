import json
import logging
import os

from config import LOG_DIR
from src.utils import get_card_transactions, get_exchange_rate, get_greeting, get_share_price

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    filename=os.path.join(LOG_DIR, "views.log"),
    encoding="utf-8",
    filemode="w",
)

home_page_ = logging.getLogger("app_home_page")


def home_page(date):
    try:
        home_page_.info("Запрос транзакций по картам и топ транзакции")
        data, top = get_card_transactions(date)
        home_page_.info("Запрос транзакций по картам и топ транзакции возвращён")

        home_page_.info("Запрос приветствия")
        greeting = get_greeting()
        home_page_.info("Запрос приветствия возвращён")

        data_dict = [
            {"last_digits": key, "total_spent": abs(value), "cashback": round(abs(value) * 0.01, 2)}
            for key, value in data.items()
        ]

        top_dict = [
            {
                "date": elemnt["Дата платежа"],
                "amount": elemnt["Сумма операции"],
                "category": elemnt["Категория"],
                "description": elemnt["Описание"],
            }
            for elemnt in top
        ]

        home_page_.info("Запрос курса валют")
        currency_rates = get_exchange_rate()
        home_page_.info("Запрос курса валют возвращён")

        home_page_.info("Запрос курса акции")
        stock_prices = get_share_price()
        home_page_.info("Запрос курса акции возвращён")

        dict_ = {
            "greeting": greeting,
            "cards": data_dict,
            "top_transactions": top_dict,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        }

        home_page_.info("Формирование JSON")
        json_data = json.dumps(dict_, ensure_ascii=False, indent=4)
        home_page_.info("Формирование JSON успешно завершено")

        return json_data
    except Exception as e:
        home_page_.error(e)
        print(e)
