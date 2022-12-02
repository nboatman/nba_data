import sqlite3
import os
from nba_data.schemas import *
from nba_data.table import Table

root_dir = os.path.dirname(os.path.dirname(__file__))
nba_database = os.path.join(root_dir, "nba_data.db")
fanduel_data_dir = os.path.join(root_dir, "nba_data", "fanduel", "data")


class NBAData:
    def __init__(self):
        self.game_ingestion = Table(GAME_INGESTION_TABLE)
        self.line_score = Table(LINE_SCORE_TABLE)
        self.four_factors = Table(FOUR_FACTORS_TABLE)
        self.basic_boxscore_player = Table(BASIC_BOXSCORE_TABLE_PLAYER)
        self.basic_boxscore_team = Table(BASIC_BOXSCORE_TABLE_TEAM)
        self.advanced_boxscore_player = Table(ADVANCED_BOXSCORE_TABLE_PLAYER)
        self.advanced_boxscore_team = Table(ADVANCED_BOXSCORE_TABLE_TEAM)
        self.fanduel_player_list = Table(FANDUEL_PLAYER_LIST_TABLE)
        self.players = Table(PLAYERS_TABLE)

        self.tables = [
            (self.line_score, 'line_score_tbl'),
            (self.four_factors, 'four_factors_tbl'),
            (self.basic_boxscore_player, 'basic_boxscore_tbl_player'),
            (self.basic_boxscore_team, 'basic_boxscore_tbl_team'),
            (self.advanced_boxscore_player, 'advanced_boxscore_tbl_player'),
            (self.advanced_boxscore_team, 'advanced_boxscore_tbl_team'),
        ]

    def setup(self):
        with sqlite3.connect(nba_database) as conn:
            cur = conn.cursor()
            for tbl, _ in self.tables:
                tbl.create(cur)
            self.game_ingestion.create(cur)
            self.fanduel_player_list.create(cur)
            self.players.create(cur)

    def clear_processed_data(self):
        with sqlite3.connect(nba_database) as conn:
            for tbl, _ in self.tables:
                tbl.delete(conn)

            self.game_ingestion.update(
                conn.cursor(),
                [
                    'boxscore_parsed = 0',
                    'play_by_play_parsed = 0',
                    'shot_chart_parsed = 0',
                    'plus_minus_parsed = 0',
                    'all_parsed = 0'
                ]
            )
