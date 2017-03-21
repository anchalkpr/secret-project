import pickle
from topicModel3 import TopicModel
from documentSummaries3 import DocumentSummaries

def getFederalDockets():
    dockets = ['discussion-simultaneous-elections']
    return dockets

def getComments():
    regulations = dict()
    comments = list()
    dockets = getFederalDockets()
    for docket in dockets:
        file_name = 'example_data/' + docket + '.txt'
        cmts = open(file_name, 'r').readlines()
        print(type(cmts))
        regulations[docket] = cmts
        comments.extend(cmts)
    return regulations, comments


def main(num_topics=10):
    
    regulations, comments = getComments()
    
    topicModel = TopicModel(num_topics)
    topicModel.fit(comments)

    for docket_id, document in regulations.items():
        docSummaries = DocumentSummaries(topicModel, num_dominant_topics=3, number_of_sentences=4)
        docSummaries.summarize(document)
        print (docket_id)
        docSummaries.display()
        
main()

