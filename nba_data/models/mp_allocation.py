from nba_data.models.base import BaseModel
from nba_data import NBAData, nba_database
import json
from sklearn.linear_model import LinearRegression
import pandas as pd
import sqlite3

MODEL_ID = 'mp_allocation'
MODEL_NAME = 'Predict Player Minutes Played Based on Team Minutes Played'
DATA_HANDLER = NBAData()
LOOK_BACK_GAMES = 15


class Model(BaseModel):
    def __init__(self):
        super().__init__(MODEL_ID, MODEL_NAME)
        self.model = LinearRegression()
        self.predictor_cols = json.dumps(['bpm_recent', 'team_bpm_recent'])
        self.target_cols = json.dumps(['mp_proportion'])

    def get_historical_data(self):
        team_minutes_sql = f"""select game_id, team, mp/5 as mp
                              from {DATA_HANDLER.basic_boxscore_team.name}
                              where period = 'game';"""

        player_minutes_sql = f"""select game_id, team, id, mp, is_starter, bpm
                                 from {DATA_HANDLER.advanced_boxscore_player.name}
                                 where period = 'game'
                                 order by game_id, team, is_starter desc;"""

        with sqlite3.connect(nba_database) as conn:
            team_minutes_df = pd.read_sql(team_minutes_sql, conn, index_col=['game_id', 'team'])
            player_minutes_df = pd.read_sql(player_minutes_sql, conn, index_col=['game_id', 'team'])

        player_avg_bpm = player_minutes_df[['id', 'bpm']]\
            .groupby('id')\
            .rolling(LOOK_BACK_GAMES, min_periods=4)\
            .mean()

        player_minutes_df = player_minutes_df.merge(team_minutes_df, on=['game_id', 'team'], suffixes=('', '_team'))
        player_minutes_df = player_minutes_df.reset_index('team').merge(player_avg_bpm, on=['game_id', 'id'], suffixes=('', '_recent'))
        player_minutes_df['mp_proportion'] = player_minutes_df['mp'] / player_minutes_df['mp_team']
        player_minutes_df['weighted_bpm'] = player_minutes_df['bpm'] * player_minutes_df['mp_proportion']

        team_bpm = player_minutes_df[['team', 'weighted_bpm']]\
            .groupby(['game_id', 'team'])\
            .sum()

        team_recent_bpm = team_bpm.reset_index('team')\
            .groupby('team')\
            .rolling(LOOK_BACK_GAMES)\
            .mean()

        player_minutes_df['team_bpm'] = player_minutes_df.merge(team_bpm, on=['game_id', 'team'], suffixes=('', '_team'))['weighted_bpm_team']

        player_minutes_df['team_bpm_recent'] = player_minutes_df.merge(team_recent_bpm, on=['game_id', 'team'], suffixes=('', '_recent'))['weighted_bpm_recent']

        return player_minutes_df[player_minutes_df['mp'] > 10], team_bpm, team_recent_bpm
