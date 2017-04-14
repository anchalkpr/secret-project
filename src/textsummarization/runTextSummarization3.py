import pickle
from topicModel3 import TopicModel
from documentSummaries3 import DocumentSummaries
import sys
import os
import traceback
import codecs

import re
pattern = re.compile("^[0-9]+ [0-9]+ ")

#DATA_DIR = "../../Data/transliterated_and_segregated/"
DATA_DIR = "example_data/"


def getDocs(language):
    try:
        inputFilesList = [inputfile for inputfile in os.listdir(DATA_DIR) if inputfile.endswith("_"+language+".txt")]
        return inputFilesList
    except:
        errorMsg = "ERROR: Error while I/O %s" %(traceback.format_exc())
        print(errorMsg)


def getComments(language):
    try:
        discussionAndComments = dict()
        comments = list()
        docs = getDocs(language)
        for doc in docs:
            file_name = DATA_DIR + doc
            cmts = []
            for line in codecs.open(file_name, mode='r', encoding="utf-8").readlines():
                cmts.append(re.sub(pattern, "", line))
            discussionAndComments[doc] = cmts
            comments.extend(cmts)
        return discussionAndComments, comments
    except:
        errorMsg = "ERROR: Error while I/O %s" %(traceback.format_exc())
        print(errorMsg)


def main(run_type, num_topics=100):
    languages = ["english", "hindi"]
    
    for language in languages:
    
        discussionAndComments, comments = getComments(language)
        
        topicModel = TopicModel(language, num_topics)
        topicModel.fit(comments, language)

        for docName, document in discussionAndComments.items():
            docSummaries = DocumentSummaries(topicModel, num_dominant_topics=4, number_of_sentences=4)
            docSummaries.summarize(document, language)
            docSummaries.display1(docName)
            if run_type == "demo":
                inp = input("Hit enter to continue:")

        
main(sys.argv[1])

