import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
import numpy as np


def svm_classifiy():
    spam_train = load_files(container_path='/Users/anshulip/GitHub/nlp-mygov/data/NB/traning_data',
                                              categories=['train_en_negative', 'train_en_positive'], shuffle='False', encoding='utf-8')
    spam_train.data = spam_train.data[0].split("\n")
    print(spam_train.data)
    i = 0
    target = []
    for data in spam_train.data:
        try:
            target.append(data[0:1] + "")
        except ValueError:
            print("ERROR " + data)
        i += 1
    spam_train.target = target

    print("target ")
    print(spam_train.target)
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(spam_train.data)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    clf = MultinomialNB().fit(X_train_tfidf, spam_train.target)

    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB()),])
    text_clf = text_clf.fit(spam_train.data, spam_train.target)

    spam_test = load_files(container_path='/Users/anshulip/GitHub/nlp-mygov/data/NB/',
                           categories=['testing_data'], shuffle='False', encoding='utf-8')
    spam_test.data = spam_test.data[0].split("\n")
    i = 0
    target = []
    for data in spam_test.data:
        try:
            target.append(data[0:1] + "")
        except ValueError:
            print("ERROR " + data)
        i += 1
    spam_test.target = target
    docs_test = spam_test.data
    predicted = text_clf.predict(docs_test)
    print("predicted:")
    print(predicted)
    print("-------------------")
    print(np.mean(predicted == spam_test.target))

    from sklearn.linear_model import SGDClassifier
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha = 1e-3, n_iter = 5, random_state = 42)),])
    text_clf.fit(spam_train.data, spam_train.target)
    predicted = text_clf.predict(docs_test)
    print(np.mean(predicted == spam_test.target))


svm_classifiy()


