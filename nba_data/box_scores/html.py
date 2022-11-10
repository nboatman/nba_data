import requests
from lxml import html


def get_boxscore_html(url):
    response =  requests.get(url=url, allow_redirects=False)
    return html.fromstring(response.content)
