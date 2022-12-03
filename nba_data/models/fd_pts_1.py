from nba_data.models.base import BaseModel
from nba_data import NBAData, nba_database
import json
from sklearn.linear_model import LinearRegression
import pandas as pd
import sqlite3

MODEL_ID = 'fd_pts_1'
MODEL_NAME = 'Simple prediction of Fanduel Points'
DATA_HANDLER = NBAData()
LOOK_BACK_GAMES = 25

# Move all the Fanduel scoring stuff somewhere else (utils?)
fd_scoring = {'pts': 1, 'ast': 1.5, 'blk': 3, 'trb': 1.2, 'stl': 3, 'tov': -1}


def compute_fd_pts(box_df):
    box_df['fd_pts'] = 0

    for k in fd_scoring:
        box_df['fd_pts'] += box_df[k] * fd_scoring[k]


class Model(BaseModel):
    def __init__(self):
        super().__init__(MODEL_ID, MODEL_NAME)
        self.model = LinearRegression()
        self.predictor_cols = json.dumps(['fd_pts_recent'])
        self.target_cols = json.dumps(['fd_pts'])

    def get_historical_data(self):
        sql = f"""select game_id, id, pts, ast, blk, trb, stl, tov
                  from {DATA_HANDLER.basic_boxscore_team.name}
                  where period ='game'
                  order by game_id;"""

        with sqlite3.connect(nba_database) as conn:
            bb_team = pd.read_sql(sql, conn, index_col=['game_id'])

        compute_fd_pts(bb_team)

        bb_team_tmp = bb_team\
            .groupby('id')\
            .rolling(LOOK_BACK_GAMES, closed='left')\
            .mean()

        bb_team = bb_team.merge(bb_team_tmp, on=['id', 'game_id'], suffixes=('', '_recent'))
        bb_team_filtered = bb_team[json.loads(self.predictor_cols) + json.loads(self.target_cols)].dropna()
        return bb_team_filtered
