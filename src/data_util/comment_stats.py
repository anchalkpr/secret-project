#Collects stats about the comments in the discussions
import os, ntpath
import codecs

#path to directory with every discussion split into english and hindi sentence
path_to_dir = "/Users/vault/Desktop/transliterated_and_segregated_output"

#list of files without
file_set = set()
for file_path in os.listdir(path_to_dir):
    file_name = ntpath.basename(file_path)
    if file_name.endswith(".txt"):
        file_set.add(file_name.rsplit("_", 1)[0])
total_english_count = 0
total_hindi_count = 0
total_unknown_count = 0

num_of_files = len(file_set)

while len(file_set) > 0:
    file_name = file_set.pop()

    print ("File name: " + file_name)

    english_file_path = os.path.join(path_to_dir, file_name+"_english.txt")
    with codecs.open(english_file_path, 'r', encoding="utf-8") as file:
        data_list = file.readlines()
        total_english_count += len(data_list)
        print ("Number of english comments: " + str(len(data_list)))

    hindi_file_path = os.path.join(path_to_dir, file_name+"_hindi.txt")
    with codecs.open(hindi_file_path, 'r', encoding="utf-8") as file:
        data_list = file.readlines()
        total_hindi_count += len(data_list)
        print ("Number of hindi comments: " + str(len(data_list)))

    unknown_file_path = os.path.join(path_to_dir, file_name+"_unknown.txt")
    if os.path.isfile(unknown_file_path):
        with codecs.open(unknown_file_path, 'r', encoding="utf-8") as file:
            data_list = file.readlines()
            total_unknown_count += len(data_list)
            print ("Number of unknown comments: " + str(len(data_list)))
    else:
        print ("Number of unknown comments: 0")

    print ()

print ("Number of files: " + str(num_of_files))
print ("Total number of English comments: " + str(total_english_count))
print ("Total number of Hindi comments: " + str(total_hindi_count))
print ("Total number of Unknown comments: " + str(total_unknown_count))

