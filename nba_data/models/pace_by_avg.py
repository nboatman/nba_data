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

FD_TO_BR = {
 'ATL': 'ATL', 'BKN': 'BRK', 'BOS': 'BOS', 'CHA': 'CHO',
 'CHI': 'CHI', 'CLE': 'CLE', 'DAL': 'DAL', 'DEN': 'DEN',
 'DET': 'DET', 'GS': 'GSW', 'HOU': 'HOU', 'IND': 'IND',
 'LAC': 'LAC', 'LAL': 'LAL', 'MEM': 'MEM', 'MIA': 'MIA',
 'MIL': 'MIL', 'MIN': 'MIN', 'NO': 'NOP', 'NY': 'NYK',
 'OKC': 'OKC', 'ORL': 'ORL', 'PHI': 'PHI', 'PHO': 'PHO',
 'POR': 'POR', 'SA': 'SAS', 'SAC': 'SAC', 'TOR': 'TOR',
 'UTA': 'UTA', 'WAS': 'WAS'
}


class Model(BaseModel):
    def __init__(self):
        super().__init__(MODEL_ID, MODEL_NAME)
        self.model = LinearRegression()
        self.predictor_cols = json.dumps(['pace_recent'])
        self.target_cols = json.dumps(['pace'])

    def get_historical_data(self):
        sql = f"""select game_id, team, pace
                  from {DATA_HANDLER.four_factors.name}
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

    def make_predictions(self, slate_id, game_date):
        sql = f"""select game_id, team, pace
                  from {DATA_HANDLER.four_factors.name}
                  where game_id < '{game_date}'
                  order by game_id;"""

        with sqlite3.connect(nba_database) as conn:
            pace_df = pd.read_sql(sql, conn, index_col=['game_id'])

        pace_team_tmp = pace_df[['team'] + json.loads(self.target_cols)] \
            .groupby('team') \
            .rolling(LOOK_BACK_GAMES, closed='left') \
            .mean() \
            .reset_index()

        recent_pace = pace_team_tmp.groupby('team').last()

        games_sql = f"""select distinct game_id, team, opponent
                        from {DATA_HANDLER.fanduel_player_list.name}
                        where game_id = '{slate_id}';"""

        with sqlite3.connect(nba_database) as conn:
            games_df = pd.read_sql(games_sql, conn)

        games_df['team'] = games_df['team'].map(FD_TO_BR)
        games_df['opponent'] = games_df['opponent'].map(FD_TO_BR)

        games_df['team_pace'] = games_df['team'].map(lambda x: recent_pace.loc[x, 'pace'])
        games_df['opponent_pace'] = games_df['opponent'].map(lambda x: recent_pace.loc[x, 'pace'])

        games_df['pace_recent'] = 1/2 * (games_df['team_pace'] + games_df['opponent_pace'])

        predictions = self.model.predict(games_df[['pace_recent']])
        games_df['pace_predicted'] = predictions
        return games_df
