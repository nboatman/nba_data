import sqlite3
from nba_data import NBAData, nba_database
from typing import Optional

class AdvancedBoxScore:
    def __init__(self, game_id, period, team, id, name, is_starter):
        self.game_id = game_id
        self.date = self.game_id[:8]
        self.period = period
        self.team = team
        self.id = id
        self.name = name

        self.mp = None
        self.ts_pct = None
        self.efg_pct = None
        self.fg3a_per_fga_pct = None
        self.fta_per_fga_pct = None
        self.orb_pct = None
        self.drb_pct = None
        self.trb_pct = None
        self.ast_pct = None
        self.stl_pct = None
        self.blk_pct = None
        self.tov_pct = None
        self.usg_pct = None
        self.off_rtg = None
        self.def_rtg = None
        self.bpm = None,
        self.is_starter = is_starter

    def format_attr(self):
        mp_min_and_sec = list(map(int, self.mp.split(':'))) + [0]
        self.mp = round(mp_min_and_sec[0] + mp_min_and_sec[1] / 60, 2)
        self.ts_pct = float_safe(self.ts_pct)
        self.efg_pct = float_safe(self.efg_pct)
        self.fg3a_per_fga_pct = float_safe(self.fg3a_per_fga_pct)
        self.fta_per_fga_pct = float_safe(self.fta_per_fga_pct)
        self.orb_pct = float_safe(self.orb_pct)
        self.drb_pct = float_safe(self.drb_pct)
        self.trb_pct = float_safe(self.trb_pct)
        self.ast_pct = float_safe(self.ast_pct)
        self.stl_pct = float_safe(self.stl_pct)
        self.blk_pct = float_safe(self.blk_pct)
        self.tov_pct = float_safe(self.tov_pct)
        self.usg_pct = float_safe(self.usg_pct)
        self.off_rtg = float_safe(self.off_rtg)
        self.def_rtg = float_safe(self.def_rtg)
        self.bpm = float_safe(self.bpm)


def ingest_for_players(boxscore_html, game_id, team):
    period = 'game'  # Advanced boxscores only available at the game level
    basic_box_table = boxscore_html.xpath(f'//table[@id="box-{team}-{period}-advanced"]')[0]
    table_rows = basic_box_table.xpath('./tbody/tr')
    advanced_box_scores = []

    starter_rows = table_rows[:5]
    reserve_rows = table_rows[6:]
    for sr in starter_rows:
        boxscore = parse_boxscore_row_player(sr, game_id, period, team, True)
        advanced_box_scores.append(boxscore)

    for rr in reserve_rows:
        boxscore = parse_boxscore_row_player(rr, game_id, period, team, False)
        if boxscore is not None:
            advanced_box_scores.append(boxscore)

    with sqlite3.connect(nba_database) as conn:
        NBAData().advanced_boxscore_player.insert(advanced_box_scores, conn)


def ingest_for_team(boxscore_html, game_id, team):
    period = 'game'
    advanced_box_team_table = boxscore_html.xpath(f'//table[@id="box-{team}-{period}-advanced"]')[0]
    advanced_box_team_row = advanced_box_team_table.xpath('.//tfoot/tr')[0]
    advanced_box_scores = [parse_boxscore_row_team(advanced_box_team_row, game_id, period, team)]

    with sqlite3.connect(nba_database) as conn:
        NBAData().advanced_boxscore_team.insert(advanced_box_scores, conn)


def parse_boxscore_row_team(row_html, game_id, period, team):

    boxscore = AdvancedBoxScore(
        game_id,
        period,
        team,
        team,
        team,
        None
    )

    data = row_html.xpath('./td')

    for d in data:
        setattr(boxscore, d.attrib['data-stat'], d.text)

    boxscore.format_attr()
    return boxscore


def parse_boxscore_row_player(row_html, game_id, period, team, is_starter):
    th = row_html.xpath('./th')[0]
    id = th.attrib.get('data-append-csv')
    player_name = th.xpath('./a')[0].text

    boxscore = AdvancedBoxScore(
        game_id,
        period,
        team,
        id,
        player_name,
        is_starter
    )

    data = row_html.xpath('./td')

    for d in data:
        setattr(boxscore, d.attrib['data-stat'], d.text)

    if hasattr(boxscore, 'reason'):
        return None

    boxscore.format_attr()

    return boxscore


# TODO - move to utils to reduce duplication
def float_safe(string_rep_of_float: Optional[str]) -> Optional[float]:
    return None if string_rep_of_float is None else float(string_rep_of_float)
