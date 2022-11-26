from copy import deepcopy

GAME_INGESTION_TABLE = {
    'name': 'game_ingestion',
    'columns': {
        'game_id': 'text', 'date': 'text',
        'boxscore': 'text', 'boxscore_ingested': 'integer', 'boxscore_parsed': 'integer',
        'play_by_play': 'text', 'play_by_play_ingested': 'integer', 'play_by_play_parsed': 'integer',
        'shot_chart': 'text', 'shot_chart_ingested': 'integer', 'shot_chart_parsed': 'integer',
        'plus_minus': 'text', 'plus_minus_ingested': 'integer', 'plus_minus_parsed': 'ingested',
        'all_ingested': 'integer', 'all_parsed': 'integer'
    },
    'pk': ['game_id'],
    'nonnull': ['game_id'],
    'indices': {
        'ingestion': ['all_ingested', 'game_id'],
        'parsing': ['all_parsed', 'game_id'],
        'boxscore_parsing': ['boxscore_parsed', 'game_id']
    }
}

LINE_SCORE_TABLE = {
    'name': 'line_score',
    'columns': {
        'game_id': 'text', 'date': 'text',
        'team': 'text', 'period': 'integer',
        'points': 'integer'
    },
    'pk': ['game_id', 'team', 'period'],
    'nonnull': ['game_id', 'team', 'period'],
    'indices': {
        'by_team': ['team', 'date', 'period'],
    }
}

FOUR_FACTORS_TABLE = {
    'name': 'four_factors',
    'columns': {
        'game_id': 'text', 'date': 'text', 'team': 'text',
        'pace': 'real', 'efg_pct': 'real',
        'tov_pct': 'real', 'orb_pct': 'real',
        'ft_rate': 'real', 'off_rtg': 'real'
    },
    'pk': ['game_id', 'team'],
    'nonnull': ['game_id', 'team'],
    'indices': {
        'by_team': ['team', 'date']
    }
}

BASIC_BOXSCORE_TABLE_PLAYER = {
    'name': 'basic_boxscore_player',
    'columns': {
        'game_id': 'text', 'date': 'text', 'period': 'text',
        'id': 'text', 'name': 'text',
        'team': 'text', 'mp': 'real',
        'fg': 'integer', 'fga': 'integer', 'fg_pct': 'real',
        'fg3': 'integer', 'fg3a': 'integer', 'fg3_pct': 'real',
        'ft': 'integer', 'fta': 'integer', 'ft_pct': 'real',
        'orb': 'integer', 'drb': 'integer', 'trb': 'integer',
        'ast': 'integer', 'stl': 'integer', 'blk': 'integer',
        'tov': 'integer', 'pf': 'integer', 'pts': 'integer',
        'plus_minus': 'integer', 'is_starter': 'integer'
    },
    'pk': ['game_id', 'team', 'period', 'id'],
    'nonnull': ['game_id', 'team', 'period', 'id'],
    'indices': {
        'by_player': ['id', 'date', 'period']
    }
}

ADVANCED_BOXSCORE_TABLE_PLAYER = {
    'name': 'advanced_boxscore_player',
    'columns': {
        'game_id': 'text', 'date': 'text', 'period': 'text',
        'id': 'text', 'name': 'text',
        'team': 'text', 'mp': 'real',
        'ts_pct': 'real', 'efg_pct': 'real',
        'fg3a_per_fga_pct': 'real', 'fta_per_fga_pct': 'real',
        'orb_pct': 'real', 'drb_pct': 'real', 'trb_pct': 'real',
        'ast_pct': 'real', 'stl_pct': 'real', 'blk_pct': 'real', 'tov_pct': 'real',
        'usg_pct': 'real', 'off_rtg': 'real', 'def_rtg': 'real', 'bpm': 'real'
    },
    'pk': ['game_id', 'team', 'period', 'id'],
    'nonnull': ['game_id', 'team', 'period', 'id'],
    'indices': {
        'by_player': ['id', 'date', 'period']
    }
}

BASIC_BOXSCORE_TABLE_TEAM = deepcopy(BASIC_BOXSCORE_TABLE_PLAYER)
BASIC_BOXSCORE_TABLE_TEAM['name'] = 'basic_boxscore_team'

ADVANCED_BOXSCORE_TABLE_TEAM = deepcopy(ADVANCED_BOXSCORE_TABLE_PLAYER)
ADVANCED_BOXSCORE_TABLE_TEAM['name'] = 'advanced_boxscore_team'

MODELS_TABLE = {
    'name': 'models',
    'columns': {
        'model_id': 'text', 'model_name': 'text', 'target_variable': 'text'
    },
    'pk': ['model_id'],
    'nonnull': ['model_id', 'model_name', 'target_variable'],
    'indices': {
        'name': ['model_name'],
        'target': ['target_variable']
    }
}

MODEL_DATA_CATALOG_TABLE = {
    'name': 'model_data_catalog',
    'columns': {
        'model_id': 'text', 'table_name_relative': 'text',
        'table_name_full': 'text'
    },
    'pk': ['model_id', 'table_name_relative'],
    'nonnull': ['model_id', 'table_name_relative', 'table_name_full']
}

FANDUEL_PLAYER_LIST_TABLE = {
    'name': 'fanduel_player_list',
    'columns': {
        'id': 'text', 'date': 'text',
        'game_id': 'text', 'player_id': 'text',
        'position': 'text', 'first_name': 'text', 'last_name': 'text',
        'nickname': 'text', 'fppg': 'real', 'played': 'integer',
        'salary': 'integer', 'game': 'text',
        'team': 'text', 'opponent': 'text',
        'injury_indicator': 'text', 'injury_details': 'text',
        'tier': 'text', 'roster_position': 'text'
    },
    'pk': ['id'],
    'nonnull': ['id'],
    'indices': {
        'by_game': ['game_id'],
        'by_date': ['date']
    }
}

PLAYERS_TABLE = {
    'name': 'players',
    'columns': {
        'br_id': 'text', 'br_name': 'text',
        'fd_id': 'text', 'fd_name': 'text',
        'date_of_birth': 'text',
        'height_inches': 'integer', 'weight_lbs': 'integer'
    },
    'pk': ['br_id'],
    'nonnull': ['br_id'],
    'indices': {
        'fd_id': ['fd_id']
    }
}
