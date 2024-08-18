import json
from unittest.mock import patch

import pandas as pd

from src.services import search_transfers_individuals


@patch("src.services.get_data_from_file")
def test_search_transfers_individuals_pattern_match(mock_get_data_from_file):
    mock_df = pd.DataFrame({"Категория": ["Переводы", "Каршеринг"], "Описание": ["Иван А.", "Ситидрайв"]})
    mock_get_data_from_file.return_value = mock_df
    expected_data = json.dumps([{"Категория": "Переводы", "Описание": "Иван А."}], ensure_ascii=False, indent=4)
    assert search_transfers_individuals() == expected_data
