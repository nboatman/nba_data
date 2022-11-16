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
        'parsing': ['all_parsed', 'game_id']
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
        'game_id': 'text', 'date': 'text',
        'team': 'text', 'key': 'text',
        'value': 'real'
    },
    'pk': ['game_id', 'team', 'key'],
    'nonnull': ['game_id', 'team', 'key'],
    'indices': {
        'by_team': ['team', 'date', 'key']
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

BASIC_BOXSCORE_TABLE_TEAM = deepcopy(BASIC_BOXSCORE_TABLE_PLAYER)
BASIC_BOXSCORE_TABLE_TEAM['name'] = 'basic_boxscore_team'

