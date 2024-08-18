import datetime
import json
import logging
import os
from typing import Optional

import pandas as pd

from config import LOG_DIR
from src.decorators import log

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    filename=os.path.join(LOG_DIR, "reports.log"),
    encoding="utf-8",
    filemode="w",
)

reports = logging.getLogger("app_reports")


@log()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> str:
    """Функция возвращает средние траты в каждый из дней недели за последние три месяца"""
    try:
        reports.info("Запрос средних трат по дням недели")
        day_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        reports.info("Проверка даты")
        if date is None:
            reports.info("Даты не переданы")
            date = datetime.datetime.now()
        else:
            reports.info("Даты переданы")
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            reports.info("Преобразование даты в нужный формат")
        date_start = date - datetime.timedelta(days=90)
        date_start = datetime.datetime(date_start.year, date_start.month, date.day)
        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
        transactions["День недели"] = transactions["Дата операции"].dt.day_name(locale="ru_RU")
        df = transactions[(transactions["Дата операции"] >= date_start) & (transactions["Дата операции"] <= date)]
        df = df.groupby("День недели")["Сумма операции"].mean()
        data = df.to_dict()
        spending_by_day_of_week = {}
        reports.info("Проверка существуют ли данные для этого периода")
        if data:
            reports.info("Данные для этого периода существуют")
            for day in day_of_week:
                spending_by_day_of_week[day] = round(data[day], 2)
        json_data = json.dumps(spending_by_day_of_week, ensure_ascii=False, indent=4)
        reports.info("Средние траты по дням недели возвращёны")
        return json_data
    except Exception as e:
        reports.error(e)
        print(e)


if __name__ == "__main__":
    from src.utils import get_data_from_file

    p = get_data_from_file()
    d = "2020-01-01 00:00:00"
    print(spending_by_weekday(p, d))
