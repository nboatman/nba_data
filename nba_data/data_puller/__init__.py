from nba_data import fanduel_data_dir, NBAData, nba_database
import datetime as dt
import nba_data.box_scores as bs
import nba_data.fanduel.player_list as fpl
import nba_data.game_ingestion.ingest as gi_ingest
import nba_data.players as players
import sqlite3

# Assume previous day's data is available after 8 a.m.
# (On the computer doing the pulling - typically Central time from personal machine)
PREV_DAY_DATA_AVAILABILITY_CUTOFF = dt.time(8)


def get_and_parse_data(first_date=None, last_date=None, do_log=True):
    if first_date is None:
        first_date = get_default_first_date()
        print(f"First date for ingestion set to {first_date}")

    if last_date is None:
        last_date = get_default_last_date()
        print(f"Last date for ingestion set to {last_date}")

    current_date = first_date

    while current_date <= last_date:
        gi_ingest.ingest_schedule(current_date)
        if do_log:
            print(f"Ingested schedule for {current_date}")
        current_date += dt.timedelta(1, 0, 0)

    gi_ingest.ingest_html_responses()
    bs.parse_and_ingest()
    players.ingest()
    fpl.ingest(fanduel_data_dir)
    players.match_with_fanduel_data()


def get_default_first_date():
    gi = NBAData().game_ingestion.name
    sql = f"""select date from {gi}
              where game_id = (select max(game_id) from {gi});"""

    with sqlite3.connect(nba_database) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        (game_date,) = cur.fetchone()
        game_date = dt.datetime.strptime(game_date, '%Y%m%d')

    return (game_date + dt.timedelta(days=1)).date()


def get_default_last_date():
    now = dt.datetime.now()
    now_time = now.time()

    offset_from_now = (1 + (now_time < PREV_DAY_DATA_AVAILABILITY_CUTOFF)) * dt.timedelta(days=-1)

    return (now + offset_from_now).date()
