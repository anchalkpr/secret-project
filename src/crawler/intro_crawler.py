import re
from bs4 import BeautifulSoup
import codecs
from crawler import crawler_helper as crawler


# TODO modify for Hindi and English


def extract_intros(topic_name):
    filename = '../../data/raw/intros/' + topic_name + '.txt'
    with codecs.open(filename, "w", "utf-8") as output_file:
        # for introductory paragraph for topics
        url_main = 'https://www.mygov.in/group-issue/' + topic_name + '/'
        print(url_main)
        data_main = crawler.make_http_call(url_main)
        output_file.write(extract_intros_text(data_main))

    output_file.close()


def extract_intros_text(html_data):
    soup = BeautifulSoup(html_data, "html.parser")
    intros = ""
    for row in soup.find_all('div', attrs={"class": "node-details"}):
        for p in row.find_all('p'):

            intros += p.text
            intros += "\n"
    return intros


def run_extract_batch():
    comments_file = '../../data/topics_list.txt'
    with open(comments_file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for topic in content:
        extract_intros(topic)


run_extract_batch()
