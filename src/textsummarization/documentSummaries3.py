from topicModel3 import tokenizer_english, tokenizer_hindi
import nltk.data
import numpy as np
import polyglot
from polyglot.text import Text, Word
import codecs
import sys

CONFIG_DIR = "config/"
sys.path.extend([CONFIG_DIR])
import config3 as cfg

#OUTPUT_DIR = "summaries/"
OUTPUT_DIR = "../../Data/generated_summaries/"

class topicSummary(object):

    def __init__(self, language, topic_id, terms, weights, sentences):
        self.topic_id = topic_id
        self.terms = terms
        self.weights = weights
        self.sentences = sentences
        self.language = language

    def __str__(self):
        if self.sentences is None or len(self.sentences) == 0:
            return 'topic does not have any sentences'
        text = str()
        
        for t in self.terms:
            text += '{:s},'.format(t)
        text += '\n'
        
        for w in self.weights:
            text += '{:5.4f},'.format(w)
        text += '\n'
        for sentence in self.sentences:
            text += sentence[2] + ' '
        return text



def innerProduct(bow1, bow2):
    keys1 = set(bow1)
    keys2 = set(bow2)
    keys = keys1.intersection(keys2)
    if not keys:
        return 0.0
    inner_product = 0.0
    for key in keys:
        inner_product += bow1[key] * bow2[key]
    sum1 = 0.0
    sum2 = 0.0
    for v in bow1.values():
        sum1 += v*v
    for v in bow2.values():
        sum2 += v*v
    inner_product /= np.sqrt(sum1 * sum2)
    return inner_product


def cosineSimilarity(sentence_bow, list_of_sentence_bow):
    # check similarity between sentence_bow and items in list_of_sentence_bow
    for bow in list_of_sentence_bow:
        inner_product = innerProduct(sentence_bow, bow)
        if inner_product >= 0.66:
            return True
    return False



class DocumentSummaries(object):
    '''
    Generates summaries for a set of documents given a topic model.
    
    Parameters
    ----------
    model: TopicModel
        a TopicModel object trained on a corpus of documents
      
    num_dominant_topics: int, default: 5
        The number of dominant topics - corresponds to the
        number of summaries that are generated.

    number_of_sentences: int, default: 5
        The number of sentences per summary. 
        
    Attributes
    ----------
    summary_data: dictionary

    
    '''
    
    def __init__(self, model):
        # the bigramizer should be the same object that was trained in TopicModel
        self.num_dominant_topics = cfg.num_dominant_topics
        self.number_of_sentences = cfg.number_of_sentences
        self.lda = model.lda
        self.dictionary = model.dictionary
        self.bigramizer = model.bigramizer
    
    
    def summarize(self, documents, language):
        
        if language == "english":
            tokens = [tokenizer_english(document) for document in documents]
        else:
            tokens = [tokenizer_hindi(document) for document in documents]
        #print("documents: %s" %documents)
        #print("bigramizer: %s" %self.bigramizer)
        tokens = [self.bigramizer[tkn] for tkn in tokens]

        corpus = [self.dictionary.doc2bow(tkn) for tkn in tokens]
        
        self.dominant_topic_ids = self.getDominantTopics(corpus)
            
        self.sentence_groups = self.splitIntoSentences(documents, language)
            
        self.distributions = self.getSentenceDistributions(language)
            
        self.summary_data = self.sentenceSelection(language, verbose=False)
            
    
    def getDominantTopics(self, corpus):
    
        # get topic weight matrix using lda.inference
        # the matrix has dimensions (num documents) x (num topics)
        inference = self.lda.inference(corpus)
        inference = inference[0] # the inference is a tuple, need the first term
        num_topics = self.lda.num_topics
        
        # find dominant topics across documents (vertical sum)
        column_sum_of_weights = np.sum(inference, axis=0)
        sorted_weight_indices = np.argsort(column_sum_of_weights)
        idx = np.arange(num_topics - self.num_dominant_topics, num_topics)
        dominant_topic_ids = sorted_weight_indices[idx]
        # the dominant_topic_ids store the ids in descending order of dominance
        dominant_topic_ids = dominant_topic_ids[::-1]
        
        return dominant_topic_ids.tolist()

    
    def splitIntoSentences(self, documents, language, MIN_SENTENCE_LENGTH = 8, MAX_SENTENCE_LENGTH = 50):
        # splits a document into sentences. Discards sentences that are too short or too long.
        # input: a list of documents
        # output: a list of lists of tuples (sentence #, sentence)
        #
        sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        #
        # discard sentences that have fewer than 10 tokens
        # according to
        # https://strainindex.wordpress.com/2008/07/28/the-average-sentence-length/
        # discard sentences that are longer than appx 20 tokens
        #
        sentence_groups = list()
        for document in documents:
            if language == "english":
                sentences = sentence_detector.tokenize(document)
            else:
                sentences = []
                text = Text(document)
                for s in text.sentences:
                    sentences.append(s.raw)
            sentence_group = list()
            for k, sentence in enumerate(sentences):
                length = len(sentence.split())
                if (length > MIN_SENTENCE_LENGTH and length < MAX_SENTENCE_LENGTH):
                    sentence_group.append((k, sentence))
            sentence_groups.append(sentence_group)
        return sentence_groups
    
    
    def getSentenceDistributions(self, language):
        # computes topic distributions for each sentence
        # output: list of lists
        # each list corresponds to a document and stores a tuple per sentence
        # the 1st element is the sentence number in the group
        # the 2nd element is a tuple of (topic_id, weight)
        distributions = list()
        get_bow = self.dictionary.doc2bow
        get_document_topics = self.lda.get_document_topics
        #print("sentence groups: %s", self.sentence_groups)
        for sentences in self.sentence_groups:
            sentence_distributions = list()
            for k, sentence in sentences:
                #print("$$$$$$$")
                if language == "english":
                    tkns = tokenizer_english(sentence)
                else:
                    tkns = tokenizer_hindi(sentence)
                if tkns is None:
                    continue
                bow = get_bow(tkns)
                dist = get_document_topics(bow)
                # this is to get list of dominant indices in decreasing order
                #dist.sort(key=lambda x: x[1], reverse=True)
                #dist = [d[0] for d in dist]
                #
                # this is to get the dominant index only (not a list)
                try:
                    dist = max(dist, key=lambda x: x[1])
                except ValueError:
                    continue
                sentence_distributions.append((k, dist))
            distributions.append(sentence_distributions)
        return distributions
    
    
    def sentenceSelection(self, language, verbose=False):
        
        results_per_docket = dict()
        results_per_docket['number_of_documents'] = len(self.sentence_groups)
        results_per_docket['dominant_topic_ids'] = self.dominant_topic_ids
        
        for dtid in self.dominant_topic_ids:
            results_per_topic = dict()
            
            top_sentences = self.sentencesPerTopic(dtid)
            
            topic_terms = self.lda.show_topic(dtid)
            terms = [t[0] for t in topic_terms]
            weights = [w[1] for w in topic_terms]
            
            ts = topicSummary(language = language, topic_id = dtid, terms=terms, 
                              weights=weights, sentences=top_sentences)
            
            if verbose:
                print(top_sentences, topic_terms)
            
            results_per_docket[dtid] = ts
        
        return results_per_docket


    def sentencesPerTopic(self, dominant_topic_id):
        
        # get only the document/sentence numbers that are dominated
        # by the dominant topic
        filtered_by_topic_id = self.filterSentencesByTopic(dominant_topic_id)
        #print("filtered sentences: %s", filtered_by_topic_id)
        
        # if the filtered list finds no sentences, move on
        # this event is highly unlikely so this is bad!!
        if len(filtered_by_topic_id) == 0:
            return
        
        # loop until you have collected number_of_sentences sentences
        # sometimes there may be no match between sentence_no and dominant_topic
        sn = 0
        
        similarity_list = list()
        top_sentences = list()
        
        #print("top sentences %s" %top_sentences)
        #print("no of sentences %s", self.number_of_sentences)
        
        while (len(top_sentences) < self.number_of_sentences and sn < len(self.distributions)):
            #print("******")
            filtered_by_sn = [f for f in filtered_by_topic_id if f[1] == sn]
            sorted_by_weight = sorted(filtered_by_sn, key=lambda x: x[2], reverse=True)
            
            if len(sorted_by_weight) == 0:
                if sn == len(self.distributions) - 1:
                    print ('No results in filtered set for sentence:', sn)
                sn += 1
                continue
            
            document_id = sorted_by_weight[0][0]
            passage = self.sentence_groups[document_id]
            sentence = [p[1] for p in passage if p[0] == sn]
            assert len(sentence) == 1
            sentence = sentence[0]
            sentence_bow = self.dictionary.doc2bow(tkns for tkns in sentence.lower().split())
            sentence_bow = dict(sentence_bow)

            if cosineSimilarity(sentence_bow, similarity_list):
                sn += 1
                continue
            similarity_list.append(sentence_bow)
            #print("sentence %s" %sentence)
            top_sentences.append((document_id, sn, sentence))
            sn += 1
        return top_sentences
    
    def filterSentencesByTopic(self, topic_id):
        # get only the document/sentence numbers in distributions
        # that match the given topic_id
        #
        # the output is a list of triplets:
        # (document number, sentence number, weight)
        filtered_by_topic_id = list()
        #print("distributions %s", self.distributions)
        for k, distribution in enumerate(self.distributions):
            filtered = [d for d in distribution if d[1][0] == topic_id]
            for item in filtered:
                filtered_by_topic_id.append((k, item[0], item[1][1]))
        return filtered_by_topic_id
    
    """    
    def display(self, doc_id):
        '''
        '''
        print("summarizing discussion: %s" %doc_id)
        outputFileName = OUTPUT_DIR + doc_id.replace(".txt", "") + "_lda" + ".txt"
        with codecs.open(outputFileName, mode='w', encoding="utf-8") as outputFile:
            print ('The dominant topics in descending order are:')
            #outputFile.write("The dominant topics in descending order are:\n")
            for dtid in self.dominant_topic_ids:
                print (dtid,)
                #outputFile.write("%s" %dtid)
            print ('')
            #outputFile.write('\n')
            
            for k in range(self.num_dominant_topics):
                if k!=None:
                    dtid = self.dominant_topic_ids[k]
                    topicSummary = self.summary_data[dtid]
                    terms = topicSummary.terms
                    if not terms:
                        #print("1111")
                        continue
                    weights = topicSummary.weights
                    num_terms = len(terms)
                    sentences = topicSummary.sentences
                    if not sentences:
                        #print("2222")
                        continue
                
                    print ('\nTopic {:d}'.format(dtid))
                    #outputFile.write('\n\nTopic {:d}'.format(dtid))
                    print ('The top {:d} terms and corresponding weights are:'.format(num_terms))
                    #outputFile.write('\nThe top {:d} terms and corresponding weights are:'.format(num_terms))
                    for term, weight in zip(terms, weights):
                        print (' * {:s} ({:5.4f})'.format(term, weight))
                        #outputFile.write('\n')
                        #outputFile.write(' * {:s} ({:5.4f})'.format(term, weight))
                    
                    print ('\n\nThe selected sentences are:',)
                    #outputFile.write('\n\nThe selected sentences are:\n')
                    n_sentences = len(sentences)
                    for j in range(n_sentences):
                        item = sentences[j]
                        #outputFile.write('{:d},'.format(item[0]))
                        print ('{:d},'.format(item[0]),)
                    print (' ')
                    #outputFile.write('\n ')
                    for j in range(n_sentences):
                        item = sentences[j]
                        sentence = item[2]
                        print (sentence)
                        outputFile.write(sentence)
                        outputFile.write('\n ')
                    print()
                    outputFile.write('\n')
    """
                    
    def display(self, doc_id):
        '''
        '''
        print("summarizing discussion: %s" %doc_id)
        topic_sentences = []
        summary = []
        outputFileName = OUTPUT_DIR + doc_id.replace(".txt", "") + "_lda" + ".txt"
        with codecs.open(outputFileName, mode='w', encoding="utf-8") as outputFile:
            print ('The dominant topics in descending order are:')
            #outputFile.write("The dominant topics in descending order are:\n")
            for dtid in self.dominant_topic_ids:
                print (dtid,)
                #outputFile.write("%s" %dtid)
            print ('')
            #outputFile.write('\n')
            
            for k in range(self.num_dominant_topics):
                if k!=None:
                    dtid = self.dominant_topic_ids[k]
                    topicSummary = self.summary_data[dtid]
                    terms = topicSummary.terms
                    if not terms:
                        #print("1111")
                        continue
                    weights = topicSummary.weights
                    num_terms = len(terms)
                    sentences = topicSummary.sentences
                    if not sentences:
                        #print("2222")
                        continue
                
                    print ('\nTopic {:d}'.format(dtid))
                    #outputFile.write('\n\nTopic {:d}'.format(dtid))
                    print ('The top {:d} terms and corresponding weights are:'.format(num_terms))
                    #outputFile.write('\nThe top {:d} terms and corresponding weights are:'.format(num_terms))
                    for term, weight in zip(terms, weights):
                        print (' * {:s} ({:5.4f})'.format(term, weight))
                        #outputFile.write('\n')
                        #outputFile.write(' * {:s} ({:5.4f})'.format(term, weight))
                    
                    print ('\n\nThe selected sentences are:',)
                    #outputFile.write('\n\nThe selected sentences are:\n')
                    n_sentences = len(sentences)
                    for j in range(n_sentences):
                        item = sentences[j]
                        #outputFile.write('{:d},'.format(item[0]))
                        print ('{:d},'.format(item[0]),)
                    print (' ')
                    #outputFile.write('\n ')
                    s = []
                    for j in range(n_sentences):
                        item = sentences[j]
                        sentence = item[2]
                        s.append(sentence)
                        print (sentence)
                        #outputFile.write(sentence)
                        #outputFile.write('\n ')
                    print()
                    topic_sentences.append(s)
                    #outputFile.write('\n')
            n = cfg.number_of_sentences
            for k in range(len(topic_sentences)):
                if n <= 0:
                    break
                for i in range(len(topic_sentences[k])):
                    if topic_sentences[k][i] not in summary:
                        summary.append(topic_sentences[k][i])
                        n -= 1
                        break
            outputFile.write('\n'.join(summary))
                   
