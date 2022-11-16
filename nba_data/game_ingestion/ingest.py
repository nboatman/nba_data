import re
import sqlite3

import requests
from lxml import html
from nba_data import NBAData, nba_database

BASE_URL = 'https://www.basketball-reference.com'


class GameIngestionRecord:
    def __init__(self, date_string, game_id):
        self.date = date_string
        self.game_id = game_id
        self.boxscore = None
        self.play_by_play = None
        self.shot_chart = None
        self.plus_minus = None

        self.boxscore_ingested = False
        self.boxscore_parsed = False
        self.play_by_play_ingested = False
        self.play_by_play_parsed = False
        self.shot_chart_ingested = False
        self.shot_chart_parsed = False
        self.plus_minus_ingested = False
        self.plus_minus_parsed = False


def get_schedule_response(game_date):
    schedule_url = f"{BASE_URL}/boxscores/?month={game_date.month}&day={game_date.day}&year={game_date.year}"
    return requests.get(url=schedule_url, allow_redirects=False)


def get_game_ids(schedule_response, game_date):
    schedule_html = html.fromstring(schedule_response.content)
    links = schedule_html.iterlinks()
    link_data_list = [l for l in links]

    boxscore_links = {l[2] for l in link_data_list if l[2].startswith(f"/boxscores/{game_date}")}

    game_id_matches = [re.search(r"^/boxscores/([^.]*).html", bl) for bl in boxscore_links]
    game_ids = [match_group.groups()[0] for match_group in game_id_matches]

    return game_ids


def ingest_schedule(game_date):
    date_string = game_date.strftime('%Y%m%d')
    schedule_response = get_schedule_response(game_date)
    game_ids = get_game_ids(schedule_response, date_string)

    game_ingestion_records = [GameIngestionRecord(date_string, game_id) for game_id in game_ids]

    with sqlite3.connect(nba_database) as conn:
        NBAData().game_ingestion.insert(game_ingestion_records, conn)
