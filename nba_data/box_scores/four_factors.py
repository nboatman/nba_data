from lxml.html import HtmlComment
from lxml import html
import sqlite3
from nba_data import NBAData, nba_database
from typing import Optional


class FourFactorsRecord:
    def __init__(self, game_id, team):
        self.game_id = game_id
        self.date = self.game_id[:8]
        self.team = team

        self.pace = None
        self.efg_pct = None
        self.tov_pct = None
        self.orb_pct = None
        self.ft_rate = None
        self.off_rtg = None

    def format_attr(self):
        self.pace = float_safe(self.pace)
        self.efg_pct = float_safe(self.efg_pct)
        self.tov_pct = float_safe(self.tov_pct)
        self.orb_pct = float_safe(self.orb_pct)
        self.ft_rate = float_safe(self.ft_rate)
        self.off_rtg = float_safe(self.off_rtg)


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

        four_factors_record = FourFactorsRecord(
            game_id,
            team
        )

        data = row.xpath('./td')

        for d in data:
            setattr(four_factors_record, d.attrib['data-stat'], d.text)

        four_factors_record.format_attr()
        four_factors.append(four_factors_record)

    with sqlite3.connect(nba_database) as conn:
        NBAData().four_factors.insert(four_factors, conn)


# TODO - move to utils to reduce duplication
def float_safe(string_rep_of_float: Optional[str]) -> Optional[float]:
    return None if string_rep_of_float is None else float(string_rep_of_float)
