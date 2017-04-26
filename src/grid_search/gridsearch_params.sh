#!/bin/bash
# script executes grid search for params
# before running script - only keep files with reference summaries in the transliterated_and_separated folder
# and empty the generated_summaries folder
# execute from src folder (root of sources)
# Usage: ./grid_search.sh ROUGE_DIR
# ROUGE_DIR is the location rouge 2.0 (Java) installation
# -----------------------------------------------------------------------------
# Num_topics, min_word_count, top_most_common_words

export PYTHONPATH="${PYTHONPATH}:${pwd}"
ROUGE_DIR = $1

for num_topics in 60 80 100 120 140
do
	for min_word_count in 2 4 6 8 10 12
	do
		for top_most_common_words in 6 8 10 12 14
		do
			#echo $num_topics $min_word_count $top_most_common_words

			echo 'python3 textsummarization/config/config3.py' $num_topics $min_word_count $top_most_common_words
			python3 textsummarization/config/config3.py $num_topics $min_word_count $top_most_common_words

			echo 'python3 textsummarization/runTextSummarization3.py test'
			python3 textsummarization/runTextSummarization3.py test

			cp ../data/generated_summaries/*english*.txt   ${ROUGE_DIR}/gridsearch/en/system
			java -jar ${ROUGE_DIR}/rouge2.0_0.2.jar
			cp results.csv ../data/gridsearch_results/results_${num_topics}_${min_word_count}_${top_most_common_words}.csv

		done
	done
done
