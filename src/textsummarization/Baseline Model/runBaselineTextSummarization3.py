import os
import traceback
import codecs
from baselineModel3 import document_summarizer

DATA_DIR = "../../../data/transliterated_and_separated/"
#DATA_DIR = "example_data/"

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
        docs = getDocs(language)
        for doc in docs:
            file_name = DATA_DIR + doc
            cmts = codecs.open(file_name, mode='r', encoding="utf-8").readlines()
            discussionAndComments[doc] = cmts
        return discussionAndComments
    except:
        errorMsg = "ERROR: Error while I/O %s" %(traceback.format_exc())
        print(errorMsg)


def main():
    languages = ["hindi", "english"]
    
    for language in languages:
    
        discussionAndComments = getComments(language)

        for docName, comments in discussionAndComments.items():
            document_summarizer(docName, comments, language)

        
main()