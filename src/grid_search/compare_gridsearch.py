import sys, codecs, os, ntpath
from collections import OrderedDict


"""
Sample results.csv file:
ROUGE-Type,Task Name,System Name,Avg_Recall,Avg_Precision,Avg_F-Score,Num Reference Summaries
ROUGE-2+StopWordRemoval+Stemming,GIVE-INPUTS-HINDI-AND-TAMIL-ONLINE-HANDWRITING-RECOGNITION-SYSTEM-ENGLISH,LDA.TXT,0.00000,0.00000,0.00000,2
ROUGE-2+StopWordRemoval+Stemming,GIVE-SUGGESTIONS-CREATION-CONTENT-DIGITAL-MARKETING-COURSE-USING-E-COMMERCE-SITE-ENGLISH,LDA.TXT,0.00000,0.00000,0.00000,1
ROUGE-2+StopWordRemoval+Stemming,GIVE-SUGGESTIONS-NEW-ACTIVITIES-UNDER-FORTHCOMING-OIL-GAS-CONSERVATION-FORTNIGHT-OGCF-%E2%80%93-ENGLISH,LDA.TXT,0.01911,0.02083,0.01994,2
ROUGE-2+StopWordRemoval+Stemming,LET-WORLD-SEE-INCREDIBLEINDIA-THROUGH-YOUR-OWN-EYES-ENGLISH,LDA.TXT,0.00000,0.00000,0.00000,1
ROUGE-2+StopWordRemoval+Stemming,REPUBLIC-DAY-WALKING-DOWN-MEMORY-LANE-ENGLISH,LDA.TXT,0.02632,0.01408,0.01835,1
ROUGE-2+StopWordRemoval+Stemming,INVITING-SUGGESTIONS-MANUAL-PROCUREMENT-GOODS-ENGLISH,LDA.TXT,0.00000,0.00000,0.00000,1
ROUGE-2+StopWordRemoval+Stemming,.DS,STORE,�,�,0.00000,0
"""


def compare_results():
    pass


def compute_average_fscore():
    pass


def read_score(filename, dir_path):
    with codecs.open(dir_path + filename, 'r', encoding="utf-8") as f:
        lines = [line[:-1] for line in f]

    fscore_sum = 0
    fscore_num = len(lines) - 2
    for i in range(1, len(lines) - 1):
        comma_splitter = lines[i].split(',')
        fscore = float(comma_splitter[-2])
        fscore_sum += fscore
    return fscore_sum / fscore_num


def batch_read(dir_path):
    file_set = set()
    print("reading from " + str(len(os.listdir(dir_path))) + " results.csv files")
    for file_path in os.listdir(dir_path):
        file_name = ntpath.basename(file_path)
        if file_name.endswith(".csv") and file_name.startswith("results"):
            file_set.add(file_name)

    fscores = {}
    while len(file_set) > 0:
        filename = file_set.pop()
        fscores[filename] = read_score(filename, dir_path)

    return fscores


def get_best_results(dir_path):
    fscores_dict = batch_read(dir_path)
    top_num_scores = 5
    sorted_scores = [(k, fscores_dict[k]) for k in sorted(fscores_dict, key=fscores_dict.get, reverse=True)]

    for key in sorted_scores:
        if top_num_scores < 0:
            break

        print(key)
        top_num_scores -= 1


results_dir_path = "../data/gridsearch_results/"

#print(read_score("results_60_2_6.csv", results_dir_path))
get_best_results(results_dir_path)
