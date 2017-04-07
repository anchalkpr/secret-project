import pickle
from topicModel3 import TopicModel
from documentSummaries3 import DocumentSummaries

import os
import traceback
import codecs

#DATA_DIR = "../../Data/Transliterated and segregated/"
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
            cmts = codecs.open(file_name, mode='r', encoding="utf-8").readlines()
            discussionAndComments[doc] = cmts
            comments.extend(cmts)
        return discussionAndComments, comments
    except:
        errorMsg = "ERROR: Error while I/O %s" %(traceback.format_exc())
        print(errorMsg)


def main(num_topics=10):
    languages = ["english", "hindi"]
    
    for language in languages:
    
        discussionAndComments, comments = getComments(language)
        
        topicModel = TopicModel(language, num_topics)
        topicModel.fit(comments, language)

        for docName, document in discussionAndComments.items():
            docSummaries = DocumentSummaries(topicModel, num_dominant_topics=3, number_of_sentences=4)
            docSummaries.summarize(document, language)
            docSummaries.display(docName)

        
main()

