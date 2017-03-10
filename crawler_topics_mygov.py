import re, json
import urllib.request
from bs4 import BeautifulSoup
import codecs
from nlp_project import crawler_helper as crawler


def extract_topics():
    # for initial set of topics
    url_main = 'https://www.mygov.in/home/61/discuss/'
    data_main = crawler.make_http_call(url_main)
    extract_topics_main(data_main)

    i = 1
    # for comments loaded by ajax calls
    while True:  
        url_ajax_comments = 'https://www.mygov.in/views/ajax/?view_name=discussion&view_display_id=block_1&view_args=61' + \
                            '&view_path=home%2F61%2Fdiscuss&pager_element=0&field_deadline_value_op=empty&' + \
                            'field_deadline_value%5Bvalue%5D=2017-03-10+11%3A26%3A31' + \
                            '&field_deadline_value%5Bmin%5D=2017-03-10+11%3A26%3A31&field_sectors_tid_op=or' + \
                            '&field_sectors_tid=All&sort_by=created&sort_order=DESC&page=' + str(i)

        json_data = crawler.extract_json(url_ajax_comments)
        html_data = json_data[1]['data']

        if re.findall('pager-load-more-empty', html_data, re.I):
            break
        i += 1
        extract_topics_main(html_data)


def extract_topics_main(html_data):
    soup = BeautifulSoup(html_data, "html.parser")

    for row in soup.find_all('div', attrs={"class" : "do_desc"}):
        for link in re.findall('''<a href="(.[^"']+)"''', str(row), re.I):
            print('https://www.mygov.in' + link)


extract_topics()
