import sqlite3

from nba_data.box_scores.html import get_boxscore_html_from_db
import nba_data.box_scores.line_score as ls
import nba_data.box_scores.four_factors as ff
import nba_data.box_scores.basic as bb
import nba_data.box_scores.advanced as ab
from nba_data import NBAData, nba_database


def parse_and_ingest(game_ids=None):
    data_handler = NBAData()

    if game_ids is None:
        sql = f"""select game_id
                  from {data_handler.game_ingestion.name}
                  where boxscore_parsed = 0;"""

        with sqlite3.connect(nba_database) as conn:
            cur = conn.cursor()
            cur.execute(sql)
            unparsed_boxes = cur.fetchall()
    else:
        unparsed_boxes = [(game_id,) for game_id in game_ids]

    for box in unparsed_boxes:
        game_id = box[0]

        box_html = get_boxscore_html_from_db(game_id)
        teams, num_periods = ls.ingest(box_html, game_id)
        ff.ingest(box_html, game_id)

        periods = ['game', 'h1', 'h2', 'q1', 'q2', 'q3', 'q4']
        for i in range(5, num_periods+1):
            periods.append(f'ot{i-4}')

        for team in teams:
            ab.ingest_for_players(box_html, game_id, team)
            ab.ingest_for_team(box_html, game_id, team)
            for period in periods:
                bb.ingest_for_players(box_html, game_id, team, period)
                bb.ingest_for_team(box_html, game_id, team, period)

        with sqlite3.connect(nba_database) as conn:
            cur = conn.cursor()

            NBAData().game_ingestion.update(
                cur,
                ["boxscore_parsed = 1"],
                record_identifier_expressions=[f"game_id = '{game_id}'"]
            )

        print(f"Parsed boxscore for {game_id}")
