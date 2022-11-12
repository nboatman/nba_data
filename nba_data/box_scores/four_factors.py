from lxml.html import HtmlComment
from lxml import html
import sqlite3
from nba_data import NBAData, nba_database


class FourFactorsRecord:
    def __init__(self, game_id, team, key, value):
        self.game_id = game_id
        self.date = self.game_id[:8]
        self.team = team
        self.key = key
        self.value = value


def get_four_factors_html(boxscore_html):
    box_score_comments = [element for element in boxscore_html.iter() if isinstance(element, HtmlComment)]
    four_factors_comments = [element for element in box_score_comments if 'id="div_four_factors"' in element.text]
    assert len(four_factors_comments) == 1, "Wrong number of Four Factors comments."

    return html.fragment_fromstring(four_factors_comments[0].text)


def ingest(boxscore_html, game_id):
    four_factors_html = get_four_factors_html(boxscore_html)
    four_factors = []

    table_body = four_factors_html.xpath('//tbody')[0]
    table_rows = table_body.xpath('./tr')
    assert len(table_rows) == 2

    for row in table_rows:
        team = row.xpath('./th/a')[0].text
        factors = {entry.attrib['data-stat']: float(entry.text) for entry in row.xpath('./td')}

        for factor in factors:
            four_factors.append(
                FourFactorsRecord(
                    game_id,
                    team,
                    factor,
                    factors[factor]
                )
            )

    with sqlite3.connect(nba_database) as conn:
        NBAData().four_factors.insert(four_factors, conn)
