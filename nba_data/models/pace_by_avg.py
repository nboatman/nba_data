from nba_data.models.base import BaseModel
from nba_data import NBAData, nba_database
import json
from sklearn.linear_model import LinearRegression
import pandas as pd
import sqlite3

MODEL_ID = 'pace_by_avg'
MODEL_NAME = 'Predict pace by averaging recent averages'
DATA_HANDLER = NBAData()
LOOK_BACK_GAMES = 25


class Model(BaseModel):
    def __init__(self):
        super().__init__(MODEL_ID, MODEL_NAME)
        self.model = LinearRegression()
        self.predictor_cols = json.dumps(['pace_recent'])
        self.target_cols = json.dumps(['pace'])

    def get_historical_data(self):
        sql = f"""select game_id, team, pace
                  from four_factors
                  order by game_id;"""

        with sqlite3.connect(nba_database) as conn:
            pace_df = pd.read_sql(sql, conn, index_col=['game_id'])

        pace_team_tmp = pace_df[['team'] + json.loads(self.target_cols)]\
            .groupby('team')\
            .rolling(LOOK_BACK_GAMES, closed='left')\
            .mean()

        pace_df = pace_df.merge(pace_team_tmp, on=['game_id', 'team'], suffixes=('', '_recent'))

        pace_avg_by_game_id = pace_df.dropna()[['pace', 'pace_recent']]\
            .groupby('game_id')\
            .agg(['mean', 'count'])
        filtered = pace_avg_by_game_id[pace_avg_by_game_id[('pace', 'count')] == 2]

        filtered = filtered[[('pace', 'mean'), ('pace_recent', 'mean')]].droplevel(1, axis=1)

        return filtered
