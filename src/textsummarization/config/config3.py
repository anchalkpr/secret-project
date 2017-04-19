import sys


languages = ["english", "hindi"]


# topic model parameters

# default topic model parameters
num_topics = 100
min_word_count = 8
top_most_common_words = 10
'''
if sys.argv[1] is not None:
    num_topics = int(sys.argv[1])
if sys.argv[2] is not None:
    min_word_count = int(sys.argv[2])
if sys.argv[3] is not None:
    top_most_common_words = int(sys.argv[3])
'''

# parameters fixed for topic modelling
min_doc_length = 40
max_doc_length = 1000
random_state = None

# the various values of parameters used for the grid search
# Num_topics, min_word_count, top_most_common_words, random_state
num_topics_list = [60, 80, 100, 120, 140]
min_word_count_list = [2, 4, 6, 8, 10, 12]
top_most_common_words_list = [6, 8, 10, 12, 14]


# DocumentSummaries parameters and Baseline model
num_dominant_topics = 4
number_of_sentences= 4


def clean_text(text):
    text = text.replace(u"\u0964", '')
    text = text.replace(u",", '')
    text = text.replace(u".", '')
    text = text.replace(u"/", '')
    text = text.replace(u"?", '')
    text = text.replace(u"-", '')
    text = text.replace(u":", '')
    text = text.replace(u"(", '')
    text = text.replace(u")", '')
    text = text.replace(u",", '')
    text = text.replace(u";", '')
    text = text.replace(u"'", '')
    text = text.replace(u'"', '')
    text = text.replace(u"|", '')
    return text