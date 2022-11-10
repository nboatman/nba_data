from lxml.html import HtmlComment
from lxml import html


def get_line_score_html(boxscore_html):
    box_score_comments = [element for element in boxscore_html.iter() if isinstance(element, HtmlComment)]
    line_score_comments = [element for element in box_score_comments if 'id="div_line_score"' in element.text]
    if len(line_score_comments) != 1:
        raise ValueError("Wrong number of comments")

    return html.fragment_fromstring(line_score_comments[0].text)


