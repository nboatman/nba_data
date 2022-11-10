GAME_LINK_TABLE = {
    'name': 'game_links',
    'columns': {
        'game_id': 'text', 'date': 'text',
        'url': 'text', 'successful_parsing': 'integer'
    },
    'pk': ['game_id'],
    'nonnull': ['game_id']
}

LINE_SCORE_TABLE = {
    'name': 'line_score',
    'columns': {
        'game_id': 'text', 'date': 'text',
        'team': 'text', 'period': 'text',
        'points': 'integer'
    },
    'pk': ['game_id', 'team', 'period'],
    'nonnull': ['game_id', 'team', 'period'],
    'indices': {
        'by_team': ['team', 'date', 'period'],
    }
}
