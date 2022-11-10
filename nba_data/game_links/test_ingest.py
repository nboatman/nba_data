import pytest
import pickle
import datetime
from .ingest import get_game_urls


def test_get_game_urls():
    with open(r"game_list_response_20221101.txt", 'rb') as rf:
        response = pickle.loads(rf.read())
    urls = get_game_urls(
        response,
        datetime.date(2022, 11, 1)
    )
    assert urls == {}
