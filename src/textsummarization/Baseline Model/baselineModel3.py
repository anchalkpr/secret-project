import re
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import numpy as np
import polyglot
from polyglot.text import Text, Word
import codecs
from hindi_stemmer import hi_stem
from collections import Counter
import config3 as cfg

wnl = WordNetLemmatizer()
lemmatizer = wnl.lemmatize

OUTPUT_DIR = "summaries/"
CONFIG_DIR = ""

class Document:
    def __init__(self, language, comments, docName):
        self.tokens = []
        self.sentences = []
        self.language = language
        self.stemSentenceMap = {}
        self.summary = []
        self.documentName = docName
        self.comments = comments

def getHindiStopWords():
    with codecs.open(CONFIG_DIR + "hindi_stopwords.txt", mode='r', encoding="utf-8") as stopWordsFile:
        stopWords = stopWordsFile.readlines()
    return stopWords
    
def getEnglishStopWords():
        stop_words = set(stopwords.words("english"))
        
        stop_words.add('please')
        stop_words.add('would')
        stop_words.add('use')
        stop_words.add('also')
        stop_words.add('thank')
        stop_words.add('sincerely')
        stop_words.add('regards')
        stop_words.add('hi')
        stop_words.add('hello')
        stop_words.add('greetings')
        stop_words.add('hey')
        stop_words.add('attachment')
        stop_words.add('attached')
        stop_words.add('attached_file')
        stop_words.add('see')
        stop_words.add('file')
        stop_words.add('comment')
        for item in 'abcdefghijklmnopqrstuvwxyz':
            stop_words.add(item)
        return stop_words

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
    return text

def tokenizer_hindi(document, sentence):
    stopWords = getHindiStopWords()
    tokens = Text(clean_text(sentence))
    tokens = [hi_stem(tkn) for tkn in tokens.words]
    tokens = [t for t in tokens if t not in stopWords]
    for token in tokens:
        if token in document.stemSentenceMap:
            document.stemSentenceMap[token].append(sentence)
        else:
            document.stemSentenceMap[token] = [sentence]
    return tokens

def tokenizer_english(document, sentence):
    stopWords = getEnglishStopWords()
    text = re.sub('[^a-zA-Z]', ' ', str(sentence))
    tokens = text.lower().split()
    tokens = [lemmatizer(tkn) for tkn in tokens]
    tokens = [t for t in tokens if t not in stopWords]
    return tokens
    
def document_tokenizer(document):
    tokens = []
    
    if document.language == "english":
        for sentence in document.sentences:
            tokens.extend(tokenizer_english(document, sentence))
    else:
        for sentence in document.sentences:
            tokens.extend(tokenizer_hindi(document, sentence))
            
    document.tokens = Counter(tokens)
    
def get_top_words(document):
    n = cfg.SENTENCES_IN_SUMMARY
    topWords = document.tokens.most_common(n)
    topWords = [word for word, count in topWords]
    return topWords
    
def get_sentences_hindi(document):
    for comment in document.comments:
        sentences = []
        text = Text(comment)
        for s in text.sentences:
            sentences.append(s.raw)
        document.sentences.extend(sentences)

def get_sentences_english(document):
    sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for comment in document.comments:
        sentences = sentence_detector.tokenize(comment)
        document.sentences.extend(sentences)
        
def get_sentences(document):
    if document.language == "english":
        get_sentences_english(document)
    else:
        get_sentences_hindi(document)

def generate_summary(document):
    topWords = get_top_words(document)
    for word in topWords:
        document.summary.append(document.stemSentenceMap[word][0])
        
def output_summary(document):
    outputFile = OUTPUT_DIR + document.documentName.replace(".txt","") + "_summary.txt"
    with codecs.open(outputFile, mode="w", encoding="utf-8") as output:
        output.write("\n".join(document.summary))
        
def document_summarizer(docName, comments, language):
    document = Document(language, comments, docName)
    get_sentences(document)
    document_tokenizer(document)
    generate_summary(document)
    output_summary(document)
    