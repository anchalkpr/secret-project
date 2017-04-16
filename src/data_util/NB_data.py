import os, ntpath, codecs
import random

path_to_dir = "/Users/vault/Desktop/transliterated_and_separated"
#path_to_dir = "/Users/vault/Desktop/temp"
path_to_output_file = "/Users/vault/Desktop/nb_sent"

base_file_list = []
for file_path in os.listdir(path_to_dir):
    file_name = ntpath.basename(file_path)
    if file_name.endswith("english.txt"):
        base_file_list.append(os.path.join(path_to_dir, file_name.split("_english.txt")[0]))

english_data_map = {}
hindi_data_map = {}
total_comments = 0
for file_path in base_file_list:
    print ("Processing file: "+file_path+"...",end='')
    english_file_path = file_path + "_english.txt"
    hindi_file_path = file_path + "_hindi.txt"
    unknown_file_path = file_path + "_unknown.txt"

    english_data_list = []
    hindi_data_list = []
    with codecs.open(english_file_path, 'r', encoding="utf-8") as english_file:
        comment_list = english_file.readlines()
        if len(comment_list) > 0:
            random.shuffle(comment_list)
            for i in range(0, min(20, len(comment_list))):
                comment = comment_list[i].strip()
                if len(comment) <= 0:
                    continue
                comment = comment.split(" ", 2)[2]
                english_data_list.append(comment)
                total_comments+=1
            for i in range(len(comment_list)-1, len(comment_list)-6, -1):
                comment = comment_list[i].strip()
                if len(comment) <= 0:
                    continue
                comment = comment.split(" ", 2)[2]
                if comment not in english_data_list:
                    english_data_list.append(comment)
                    total_comments+=1

    with codecs.open(hindi_file_path, 'r', encoding="utf-8") as hindi_file:
        comment_list = hindi_file.readlines()
        if len(comment_list) > 0:
            random.shuffle(comment_list)
            for i in range(0, min(5, len(comment_list))):
                comment = comment_list[i].strip()
                if len(comment) <= 0:
                    continue
                comment = comment.split(" ", 2)[2]
                hindi_data_list.append(comment)
                total_comments += 1

    english_data_map[ntpath.basename(file_path)] = english_data_list
    hindi_data_map[ntpath.basename(file_path)] = hindi_data_list
    print ("done")

total_english_lines = 0
with codecs.open(path_to_output_file+"_english.txt", 'w', encoding="utf-8") as output_file:
        for key, value in english_data_map.items():
            for line in value:
                output_file.write(key)
                output_file.write("\n")
                output_file.write(line)
                output_file.write("\n")
                total_english_lines+=1

total_hindi_lines = 0
with codecs.open(path_to_output_file+"_hindi.txt", 'w', encoding="utf-8") as output_file:
    for key, value in hindi_data_map.items():
        for line in value:
            output_file.write(key)
            output_file.write("\n")
            output_file.write(line)
            output_file.write("\n")
            total_hindi_lines += 1

print ("Total comments added to lists: "+str(total_comments))
print ("Total english lines written: "+str(total_english_lines))
print ("Total hindi lines written: "+str(total_hindi_lines))