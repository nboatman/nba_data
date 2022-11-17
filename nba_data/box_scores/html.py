import sqlite3

import requests
from lxml import html
from nba_data import NBAData, nba_database

BASE_URL = 'https://www.basketball-reference.com'


def get_boxscore_html_from_db(game_id):
    sql = f"""select boxscore
              from {NBAData().game_ingestion.name}
              where game_id = '{game_id}';"""

    with sqlite3.connect(nba_database) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        boxscore = cur.fetchall()[0][0]

    return html.fromstring(boxscore)


def get_response(relative_url):
    absolute_url = f"{BASE_URL}{relative_url}"
    return requests.get(url=absolute_url, allow_redirects=False)
