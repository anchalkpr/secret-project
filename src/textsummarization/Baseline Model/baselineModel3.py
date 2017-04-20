import re
import sys
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk.data
from collections import Counter
import numpy as np
import polyglot
from polyglot.text import Text, Word
import codecs
from collections import Counter

CONFIG_DIR = "../config/"
sys.path.extend([CONFIG_DIR])
import config3 as cfg
from hindi_stemmer import hi_stem

wnl = WordNetLemmatizer()
lemmatizer = wnl.lemmatize

pattern = re.compile("^[0-9]+ [0-9]+ ")

#OUTPUT_DIR = "summaries/"
OUTPUT_DIR = "../../../data/generated_summaries/"

class Document:
    def __init__(self, language, comments, docName):
        self.tokens = []
        self.sentences = []
        self.language = language
        self.stemSentenceMap = {}
        self.summary = []
        self.documentName = docName
        self.comments = []
        for comment in comments:
            self.comments.append(re.sub(pattern, "", comment))                

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

def tokenizer_hindi(document, sentence):
    stopWords = getHindiStopWords()
    text = cfg.clean_text(sentence)
    if len(text) < 1:
        return []
    tokens = Text(text)
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
    for token in tokens:
            if token in document.stemSentenceMap:
                document.stemSentenceMap[token].append(sentence)
            else:
                document.stemSentenceMap[token] = [sentence]
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
    topWords = document.tokens.most_common()
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
    n = cfg.number_of_sentences
    for word in topWords:
        if n <= 0:
            break
        for i in range(len(document.stemSentenceMap[word])):
            if document.stemSentenceMap[word][i] not in document.summary:
                document.summary.append(document.stemSentenceMap[word][i])
                n -= 1
                break
        
def output_summary(document):
    outputFile = OUTPUT_DIR + document.documentName.replace(".txt","") + "_baseline.txt"
    with codecs.open(outputFile, mode="w", encoding="utf-8") as output:
        output.write("\n".join(document.summary))
        
def document_summarizer(docName, comments, language):
    document = Document(language, comments, docName)
    get_sentences(document)
    document_tokenizer(document)
    generate_summary(document)
    output_summary(document)
    