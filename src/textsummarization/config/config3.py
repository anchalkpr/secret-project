languages = ["english", "hindi"]

#topic model parameters
num_topics=100 
min_word_count=8 
top_most_common_words=10
min_doc_length=40 
max_doc_length=1000
random_state=None

#DocumentSummaries parameters and Baseline model
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