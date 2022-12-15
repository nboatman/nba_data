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
        self.predictor_cols = json.dumps(['mp_proportion_recent', 'is_starter', 'is_starter_recent'])
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

        player_minutes_df = player_minutes_df.merge(team_minutes_df, on=['game_id', 'team'], suffixes=('', '_team'))
        player_minutes_df['mp_proportion'] = player_minutes_df['mp'] / player_minutes_df['mp_team']

        player_minutes_df.sort_index(inplace=True)

        recent_mp = player_minutes_df[['id', 'mp_proportion', 'is_starter']] \
            .groupby('id') \
            .rolling(LOOK_BACK_GAMES, min_periods=5, closed='left') \
            .mean().fillna(0)

        player_minutes_df = player_minutes_df.merge(
            recent_mp,
            on=['id', 'team', 'game_id'],
            suffixes=('', '_recent')
        ).reset_index().dropna()

        return player_minutes_df[player_minutes_df['game_id'] > '202002']
