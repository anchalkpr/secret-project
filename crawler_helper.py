import urllib.request
from bs4 import BeautifulSoup


def make_http_call(url):
    f = urllib.request.urlopen(url)
    data = f.read()

    encoding = f.info().get_content_charset('utf-8')
    return data.decode(encoding)


def extract_comments_text(html_data):
    soup = BeautifulSoup(html_data, "html.parser")
    extracted_comments = []
    for row in soup.find_all('div', attrs={"class": "comment_body"}):
        extracted_comments.append(row.text)

    return extracted_comments
