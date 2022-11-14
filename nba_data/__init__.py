import sqlite3
import os
from nba_data.schemas import *

db_path = os.path.dirname(os.path.dirname(__file__))
nba_database = os.path.join(db_path, "nba_data.db")


class NBAData:
    def __init__(self):
        self.game_links = Table(GAME_LINK_TABLE)
        self.line_score = Table(LINE_SCORE_TABLE)
        self.four_factors = Table(FOUR_FACTORS_TABLE)
        self.basic_boxscore_player = Table(BASIC_BOXSCORE_TABLE_PLAYER)

        self.tables = [
            (self.line_score, 'line_score_tbl'),
            (self.four_factors, 'four_factors_tbl'),
            (self.basic_boxscore_player, 'basic_boxscore_tbl_player')
        ]

    def setup(self):
        with sqlite3.connect(nba_database) as conn:
            cur = conn.cursor()
            for tbl, _ in self.tables:
                tbl.create(cur)
            self.game_links.create(cur)

    def clear_processed_data(self):
        with sqlite3.connect(nba_database) as conn:
            for tbl, _ in self.tables:
                tbl.delete(conn)
            self.game_links.update(conn.cursor(), ['successful_parsing = 0'])


class Table:
    def __init__(self, schema_dict):
        self.name = schema_dict['name']
        self.columns = schema_dict['columns'].copy()
        self.column_names = list(self.columns.keys())
        self.primary_key = schema_dict['pk'].copy()
        self.nonnull = schema_dict.get('nonnull', [])
        self.indices = schema_dict.get('indices', {})

    def create(self, db_cursor):
        query = f"""CREATE TABLE IF NOT EXISTS {self.name}
                ({", ".join([x + " " + self.columns[x] for x in self.columns])},
                PRIMARY KEY({", ".join(self.primary_key)}))
                WITHOUT ROWID;"""

        db_cursor.execute(query)

        for table_index in self.indices:
            query = f"""CREATE INDEX IF NOT EXISTS ind_{self.name}_{table_index}
                    ON {self.name}
                        ({', '.join(self.indices[table_index])})"""
            db_cursor.execute(query)

    def delete(self, db_connection):
        sql_command = f"DROP TABLE IF EXISTS {self.name}"
        db_cursor = db_connection.cursor()
        db_cursor.execute(sql_command)
        db_connection.commit()

    def insert(self, data, db_connection, batch_insert=True):
        db_cursor = db_connection.cursor()
        columns = ",".join(self.column_names)
        q_marks = ",".join(['?'] * len(self.column_names))
        values_to_insert = {}

        for record in data:
            if self.is_nonnull_where_required(record):
                values_to_insert[self.get_primary_key_value(record)] = self.get_values_to_insert(record)

        if batch_insert:
            try:
                db_cursor.executemany(
                    f"""INSERT INTO {self.name} ({columns}) VALUES ({q_marks})""", list(values_to_insert.values()))
            except sqlite3.IntegrityError as err:
                print(err)
                print(f"{list(values_to_insert.values())[0]}")

        db_connection.commit()

    def is_nonnull_where_required(self, record):
        for nonnull_column in self.nonnull:
            if getattr(record, nonnull_column, None) is None:
                return False
        else:
            return True

    def get_primary_key_value(self, record):
        return tuple([getattr(record, pk_component, None) for pk_component in self.primary_key])

    def get_values_to_insert(self, record):
        return tuple([getattr(record, column, None) for column in self.column_names])

    def update(self, db_cursor, value_expressions, record_identifier_expressions=None):
        if record_identifier_expressions is None:
            where_clause = ""
        else:
            where_clause = f"WHERE {' AND '.join(record_identifier_expressions)}"

        query = f"""UPDATE {self.name}
                    SET {', '.join(value_expressions)}
                    {where_clause};"""
        db_cursor.execute(query)
