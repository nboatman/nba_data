import json
from lxml import html
import random
import requests
import sqlite3
import time
from nba_data import NBAData, nba_database

BASE_URL = r"https://www.basketball-reference.com/players"


class PlayerRecord:
    def __init__(self, br_id, player_details):
        self.br_id = br_id
        self.br_name = player_details['name']
        self.fd_id = None
        self.fd_name = None
        self.date_of_birth = player_details['birthDate'].replace('-', '')
        self.height_inches = handle_height_string(player_details["height"]["value"])
        self.weight_lbs = player_details["weight"]["value"].split(" ")[0]


def ingest():
    data_handler = NBAData()

    sql = f"""select distinct bb.id
              from {data_handler.basic_boxscore_player.name} bb
              left join {data_handler.players.name} p
              on bb.id = p.br_id
              where p.br_id is NULL;"""

    with sqlite3.connect(nba_database) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        players_to_add = cur.fetchall()

    for (player_id,) in players_to_add:
        print(f"player_id {player_id}")
        player_html = get_player_html(player_id)
        player_data_dict = json.loads(
            player_html.xpath('//script[@type="application/ld+json"]')[0].text_content()
        )

        player_records = [PlayerRecord(player_id, player_data_dict)]

        with sqlite3.connect(nba_database) as conn:
            data_handler.players.insert(player_records, conn)


def form_player_url(player_id):
    initial = player_id[0]
    return f"{BASE_URL}/{initial}/{player_id}.html"


def get_player_html(player_id):
    url = form_player_url(player_id)
    response = requests.get(url=url, allow_redirects=False)

    # Sleep to avoid getting rate limited
    time.sleep(random.randint(1, 3))

    response.raise_for_status()
    return html.fromstring(response.content)

def handle_height_string(h):
    ft, inches = map(int, h.split('-'))
    return 12 * ft + inches
