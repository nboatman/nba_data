import re
import sqlite3

import requests
from lxml import html
from nba_data import NBAData, nba_database
from nba_data.box_scores.html import get_response

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

        self.all_ingested = False
        self.all_parsed = False


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


def ingest_html_responses(game_ids=None):
    data_handler = NBAData()

    if game_ids is None:
        sql = f"""select game_id, boxscore_ingested, play_by_play_ingested,
                    shot_chart_ingested, plus_minus_ingested
                  from {data_handler.game_ingestion.name}
                  where all_ingested = 0"""

        with sqlite3.connect(nba_database) as conn:
            cur = conn.cursor()
            cur.execute(sql)
            ingestion_records = cur.fetchall()
    else:
        ingestion_records = [(game_id, 0, 0, 0, 0) for game_id in game_ids]

    responses = [get_responses_for_data(ingestion_record) for ingestion_record in ingestion_records]

    for response in responses:
        (game_id, box_response, pbp_response, shot_chart_response, pm_response) = response

        with sqlite3.connect(nba_database) as conn:
            cur = conn.cursor()

            for (col, resp) in zip(('boxscore', 'play_by_play', 'shot_chart', 'plus_minus'), response[1:]):
                if resp is None:
                    continue
                NBAData().game_ingestion.update(
                    cur,
                    [f"{col} = ?", f"{col}_ingested = ?"],
                    record_identifier_expressions = [f"game_id = '{game_id}'"],
                    values=(resp.content, 1)
                )


def get_responses_for_data(record_tuple):
    (game_id, boxscore_ingested, play_by_play_ingested,
     shot_chart_ingested, plus_minus_ingested) = record_tuple

    responses = [game_id]

    responses.append(None if boxscore_ingested else get_response(f'/boxscores/{game_id}.html'))
    responses.append(None if play_by_play_ingested else get_response(f'/boxscores/pbp/{game_id}.html'))
    responses.append(None if shot_chart_ingested else get_response(f'/boxscores/shot-chart/{game_id}.html'))
    responses.append(None if plus_minus_ingested else get_response(f'/boxscores/plus-minus/{game_id}.html'))

    return responses
