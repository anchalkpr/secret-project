import re, json
import urllib.request
from bs4 import BeautifulSoup
import codecs
from nlp_project import crawler_helper as crawler


def extract_comments(topic_name):
    filename = 'comments/' + topic_name + '.txt'
    with codecs.open(filename, "w", "utf-8") as output_file:
        # for initial set of comments
        url_main = 'https://www.mygov.in/group-issue/' + topic_name + '/'
        print(url_main)
        data_main = crawler.make_http_call(url_main)
        output_file.write(extract_comments_and_metadata(data_main))

        view_args = extract_view_args(data_main)

        i = 1
        # for comments loaded by ajax calls
        while True: 
            url_ajax_comments = 'https://www.mygov.in/views/ajax/?view_name=view_comments&view_display_id=block_2' + \
                                '&view_args=' + view_args + '&view_path=node%2F' + view_args + \
                                '&view_base_path=comment_pdf_export&pager_element=1&sort_by=created&sort_order=DESC' + \
                                '&page=0%2C' + str(i)

            json_data = crawler.extract_json(url_ajax_comments)
            html_data = json_data[1]['data']

            if re.findall('pager-load-more-empty', html_data, re.I):
                break
            i += 1
            output_file.write(extract_comments_and_metadata(html_data))
    output_file.close()


def extract_view_args(html):
    view_args = re.search("view_args\":\"([0-9]+)", html)
    return view_args.group(1)


def extract_votes(html_data, is_upvote):
    votes = []
    soup = BeautifulSoup(html_data, "html.parser")

    upvote_class = 'like_count_value'
    downvote_class = 'dislike_count_value'

    vote_type = upvote_class
    if not is_upvote:
        vote_type = downvote_class

    for row in soup.find_all('span', attrs={"class": vote_type}):
        votes.append(int(row.text[1:len(row.text) - 1]))
    return votes


def extract_comments_and_metadata(html_data):
    """
    get comment, upvotes(likes) and downvotes(dislikes)
    """
    # TODO hashtag handling
    # eg. - <a href="/" class="hashtag_comments" data="#NDTV">#NDTV</a>

    # beautifulsoup to parse html tags
    comments = crawler.extract_comments_text(html_data)
    upvotes = extract_votes(html_data, True)
    downvotes = extract_votes(html_data, False)

    extracted_data = ''
    num_comments = len(comments)
    for i in range(num_comments):
        new_extracted_data = str(upvotes[i])
        new_extracted_data += ' '
        new_extracted_data += str(downvotes[i])
        new_extracted_data += ' '
        new_extracted_data += comments[i].replace('\r', '').replace('\n', '')
        new_extracted_data += '\n'
        extracted_data += new_extracted_data
    return extracted_data


def run_extract_batch():
    comments_file = 'topics_list.txt'
    with open(comments_file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    for topic in content:
        extract_comments(topic)


run_extract_batch()
