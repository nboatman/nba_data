import sqlite3
from nba_data import NBAData, nba_database


class BasicBoxScore:
    def __init__(self, game_id, period, team, opponent, id, name, is_starter):
        self.game_id = game_id
        self.date = self.game_id[:8]
        self.period = period
        self.team = team
        self.opponent = opponent
        self.id = id
        self.name = name

        self.mp = None
        self.fg = None
        self.fga = None
        self.fg_pct = None
        self.fg3 = None
        self.fg3a = None
        self.fg3_pct = None
        self.ft = None
        self.fta = None
        self.ft_pct = None
        self.orb = None
        self.drb = None
        self.trb = None
        self.ast = None
        self.stl = None
        self.blk = None
        self.tov = None
        self.pf = None
        self.pts = None
        self.plus_minus = None
        self.is_starter = is_starter

    def format_attr(self):
        mp_min_and_sec = list(map(int, self.mp.split(':'))) + [0]
        self.mp = round(mp_min_and_sec[0] + mp_min_and_sec[1] / 60, 2)
        self.fg = int(self.fg)
        self.fga = int(self.fga)
        self.fg_pct = None if self.fg_pct is None else float(self.fg_pct)
        self.fg3 = int(self.fg3)
        self.fg3a = int(self.fg3a)
        self.fg3_pct = None if self.fg3_pct is None else float(self.fg3_pct)
        self.ft = int(self.ft)
        self.fta = int(self.fta)
        self.ft_pct = None if self.ft_pct is None else float(self.ft_pct)
        self.orb = int(self.orb)
        self.drb = int(self.drb)
        self.trb = int(self.trb)
        self.ast = int(self.ast)
        self.stl = int(self.stl)
        self.blk = int(self.blk)
        self.tov = int(self.tov)
        self.pf = int(self.pf)
        self.pts = int(self.pts)
        self.plus_minus = int(self.plus_minus) if self.plus_minus is not None else None


def ingest_for_players(boxscore_html, game_id, team, opponent, period):
    basic_box_table = boxscore_html.xpath(f'//table[@id="box-{team}-{period}-basic"]')[0]
    table_rows = basic_box_table.xpath('./tbody/tr')
    basic_box_scores = []

    starter_rows = table_rows[:5]
    reserve_rows = table_rows[6:]
    for sr in starter_rows:
        boxscore = parse_boxscore_row_player(sr, game_id, period, team, opponent, True)
        basic_box_scores.append(boxscore)

    for rr in reserve_rows:
        boxscore = parse_boxscore_row_player(rr, game_id, period, team, opponent, False)
        if boxscore is not None:
            basic_box_scores.append(boxscore)

    with sqlite3.connect(nba_database) as conn:
        NBAData().basic_boxscore_player.insert(basic_box_scores, conn)


def ingest_for_team(boxscore_html, game_id, team, opponent, period):
    basic_box_team_table = boxscore_html.xpath(f'//table[@id="box-{team}-{period}-basic"]')[0]
    basic_box_team_row = basic_box_team_table.xpath('.//tfoot/tr')[0]
    basic_box_scores = [parse_boxscore_row_team(basic_box_team_row, game_id, period, team, opponent)]

    with sqlite3.connect(nba_database) as conn:
        NBAData().basic_boxscore_team.insert(basic_box_scores, conn)


def parse_boxscore_row_team(row_html, game_id, period, team, opponent):

    boxscore = BasicBoxScore(
        game_id,
        period,
        team,
        opponent,
        team,
        team,
        None
    )

    data = row_html.xpath('./td')

    for d in data:
        setattr(boxscore, d.attrib['data-stat'], d.text)

    boxscore.format_attr()
    return boxscore


def parse_boxscore_row_player(row_html, game_id, period, team, opponent, is_starter):
    th = row_html.xpath('./th')[0]
    id = th.attrib.get('data-append-csv')
    player_name = th.xpath('./a')[0].text

    boxscore = BasicBoxScore(
        game_id,
        period,
        team,
        opponent,
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
