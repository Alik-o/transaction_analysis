import json
import logging
from config import LOG_DIR
import os

from src.utils import get_data_from_file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    filename=os.path.join(LOG_DIR, "services.log"),
    encoding="utf-8",
    filemode="w")

services = logging.getLogger('app_service')


def search_transfers_individuals():
    try:
        services.info("Запрос переводов с карты")
        df = get_data_from_file()
        pattern = r"[А-Я][а-я]+\s[А-Я]\."
        df_transfer = df[df["Категория"] == "Переводы"]
        df_filter = df_transfer[df_transfer["Описание"].str.contains(pattern)]
        data = df_filter.to_dict(orient="records")
        data_json = json.dumps(data, ensure_ascii=False, indent=4)
        services.info("Переводы с карты возвращён")
        return data_json
    except Exception as e:
        services.error(e)
        print(e)
