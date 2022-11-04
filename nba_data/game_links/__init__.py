import re
import requests
from lxml import html

BASE_URL = 'https://www.basketball-reference.com'


class GameLinkRecord:
    def __init__(self, date, game_id):
        self.date = date
        self.game_id = game_id
        self.url = f"/boxscores/{game_id}.html"
        self.successful_parsing = False


def get_game_urls(game_date):
    schedule_url = f"{BASE_URL}/boxscores/?month={game_date.month}&day={game_date.day}&year={game_date.year}"
    response = requests.get(url=schedule_url, allow_redirects=False)
    schedule_html = html.fromstring(response.content)
    links = schedule_html.iterlinks()
    link_data_list = [l for l in links]

    game_date_string = game_date.strftime('%Y%m%d')
    boxscore_links = {l[2] for l in link_data_list if l[2].startswith(f"/boxscores/{game_date_string}")}

    return boxscore_links


def ingest_links(game_date):
    date_string = game_date.strftime('%Y%m%d')
    boxscore_links = get_game_urls(game_date)

    game_id_matches = [re.search(r"^/boxscores/([^.]*).html", bl) for bl in boxscore_links]
    game_ids = [match_group.groups()[0] for match_group in game_id_matches]

    game_link_records = [GameLinkRecord(date_string, game_id) for game_id in game_ids]
    return game_link_records
