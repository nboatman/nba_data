from nba_data.box_scores.html import get_boxscore_html_from_db
import nba_data.box_scores.line_score as ls
import nba_data.box_scores.four_factors as ff
import nba_data.box_scores.basic as bb


def parse_and_ingest(game_id):
    box_html = get_boxscore_html_from_db(game_id)
    teams, num_periods = ls.ingest(box_html, game_id)
    ff.ingest(box_html, game_id)

    periods = ['game', 'h1', 'h2', 'q1', 'q2', 'q3', 'q4']
    for i in range(5, num_periods+1):
        periods.append(f'ot{i-4}')

    for team in teams:
        for period in periods:
            bb.ingest_for_players(box_html, game_id, team, period)
            bb.ingest_for_team(box_html, game_id, team, period)
