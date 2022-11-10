import requests
from lxml import html

BASE_URL = 'https://www.basketball-reference.com'


def get_boxscore_html(relative_url):
    absolute_url = f"{BASE_URL}{relative_url}"
    response =  requests.get(url=absolute_url, allow_redirects=False)
    return html.fromstring(response.content)
