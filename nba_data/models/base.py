from sklearn.model_selection import train_test_split
from nba_data.schemas import MODELS_TABLE
from nba_data.table import Table
from nba_data import nba_database
import json
import pickle
import random
import sqlite3

MODELS_TBL = Table(MODELS_TABLE)


def setup():
    with sqlite3.connect(nba_database) as conn:
        cur = conn.cursor()
        MODELS_TBL.create(cur)


class Model:
    def __init__(self, model_id=None, model_name=None, random_state=None):
        self.model_id = model_id
        self.model_name = model_name
        self.model = None
        self.model_serialized = None

        # Each of predictors_cols and target_cols is a string representing a list of strings
        self.predictor_cols: str = '[]'
        self.target_cols: str = '[]'
        self.random_state = random_state or random.randint(1, 10**6)
        self.model_score = None

    def fit_model(self, data_df):
        x = data_df[json.loads(self.predictor_cols)]
        y = data_df[json.loads(self.target_cols)]

        x_train, _, y_train, _ = train_test_split(x, y, random_state=self.random_state)
        self.model.fit(x_train, y_train)
        self.model_serialized = pickle(self.model)

    def score_model(self, data_df):
        x = data_df[json.loads(self.predictor_cols)]
        y = data_df[json.loads(self.target_cols)]

        _, x_test, _, y_test = train_test_split(x, y, random_state=self.random_state)
        self.model_score = self.model.score(x_test, y_test)

    def write_to_db(self):
        with sqlite3.connect(nba_database) as conn:
            MODELS_TBL.insert([self], conn)


def read_from_db(model_id):
    sql = f"""select * from {MODELS_TBL.name}
              where model_id='{model_id}';"""

    with sqlite3.connect(nba_database) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql)
        model_record = cur.fetchone()

    # Initialized model
    model = Model()

    for col in MODELS_TBL.columns:
        setattr(model, col, model_record[col])

    model.model = pickle.loads(model.model_serialized)

    return model


# Set up the table on import
setup()
