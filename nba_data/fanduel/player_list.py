import os
import sqlite3
import pandas as pd
from nba_data import NBAData, nba_database


class FanduelPlayerRecord:
    def __init__(self, fanduel_player, date):
        self.id = fanduel_player['Id']
        self.date = date
        self.game_id = self.id.split('-')[0]
        self.player_id = self.id.split('-')[1]
        self.position = fanduel_player['Position']
        self.first_name = fanduel_player['First Name']
        self.last_name = fanduel_player['Last Name']
        self.nickname = fanduel_player['Nickname']
        self.fppg = fanduel_player['FPPG']
        self.played = int(0 if pd.isna(fanduel_player['Played']) else fanduel_player['Played'])
        self.salary = int(fanduel_player['Salary'])
        self.game = fanduel_player['Game']
        self.team = fanduel_player['Team']
        self.opponent = fanduel_player['Opponent']
        self.injury_indicator = fanduel_player['Injury Indicator'] if type(fanduel_player['Injury Indicator']) == str else None
        self.injury_details = fanduel_player['Injury Details'] if type(fanduel_player['Injury Details']) == str else None
        self.tier = None if pd.isna(fanduel_player['Tier']) else fanduel_player['Tier']
        self.roster_position = fanduel_player['Roster Position']


def ingest(path):
    files = [f for f in os.listdir(path) if f.endswith('-players-list.csv')]

    for file in files:
        records = parse_records_from_file(os.path.join(path, file))

        with sqlite3.connect(nba_database) as conn:
            NBAData().fanduel_player_list.insert(records, conn)

        os.rename(os.path.join(path, file), os.path.join(path, 'processed', file))


def parse_records_from_file(file_name):
    date = ''.join(file_name.split('NBA-')[-1].split(' ET-')[:3])
    file_content = pd.read_csv(file_name)

    records = []

    for idx, row in file_content.iterrows():
        records.append(FanduelPlayerRecord(row, date))

    return records

