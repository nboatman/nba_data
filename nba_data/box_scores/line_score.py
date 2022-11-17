from lxml.html import HtmlComment
from lxml import html
import sqlite3
from nba_data import NBAData, nba_database

PERIODS = {str(i): i for i in range(1, 5)}

for i in range(1, 10):
    PERIODS[str(f"{i}OT")] = i + 4


class LineScoreRecord:
    def __init__(self, game_id, team, period, points):
        self.game_id = game_id
        self.date = self.game_id[:8]
        self.team = team
        self.period = period
        self.points = points


def get_line_score_html(boxscore_html):
    box_score_comments = [element for element in boxscore_html.iter() if isinstance(element, HtmlComment)]
    line_score_comments = [element for element in box_score_comments if 'id="div_line_score"' in element.text]
    assert len(line_score_comments) == 1, "Wrong number of Line Score comments"

    return html.fragment_fromstring(line_score_comments[0].text)


def ingest(boxscore_html, game_id):
    line_score_html = get_line_score_html(boxscore_html)
    line_scores = []

    table_body = line_score_html.xpath('//tbody')[0]
    table_rows = table_body.xpath('./tr')
    assert len(table_rows) == 2

    teams = []
    num_periods = 4

    for row in table_rows:
        team = row.xpath('./th/a')[0].text
        teams.append(team)
        period_scores = {PERIODS[s.attrib['data-stat']]: int(s.text) for s in row.xpath('./td') if s.attrib['data-stat'] in PERIODS}

        for period in period_scores:
            line_scores.append(
                LineScoreRecord(
                    game_id,
                    team,
                    period,
                    period_scores[period]
                )
            )

            num_periods = max(num_periods, period)

    with sqlite3.connect(nba_database) as conn:
        NBAData().line_score.insert(line_scores, conn)

    return teams, num_periods
