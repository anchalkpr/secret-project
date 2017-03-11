from polyglot.text import Text, Word
from polyglot.transliteration import Transliterator
import os
import ntpath

def transliterate_to_hindi(sentence):
    english_hindi_transliterator = Transliterator(source_lang="en", target_lang="hi")
    token_list = sentence.split(' ')
    transliterated_sent = ""
    for token in token_list:
        transliterated_sent+=english_hindi_transliterator.transliterate(token)+" "
    return transliterated_sent.strip()


path_to_dir = "/Users/vault/Desktop/Data"
path_to_output_dir = "/Users/vault/Desktop/Data_output"

file_list = []
for file_path in os.listdir(path_to_dir):
    file_name = ntpath.basename(file_path)
    if file_name.endswith(".txt"):
        file_list.append(os.path.join(path_to_dir, file_name))

for file_path in file_list:
    hindi_list = []
    english_list = []
    file_name = ""
    with open(file_path) as file:
        file_name = ntpath.basename(file.name)
        print file.name
        data_list = file.readlines()

        for line in data_list:
            line = line.strip()
            if len(line) <= 0:
                continue

            split_data = line.split(" ", 2)
            if len(split_data) != 3:
                print "Skipping line: " + line
                continue
            comment = split_data[2]

            text = Text(comment)
            if text.language.code == "hi":
                hindi_list.append(line)
                hindi_list.append("\n")
            elif text.language.code == "en":
                english_list.append(line)
                english_list.append("\n")
            else:
                transliterated_line = transliterate_to_hindi(line)
                transliterated_lang = Text(transliterated_line)
                if transliterated_lang.language.code == "hi":
                    hindi_list.append(line)
                    hindi_list.append("\n")
                else:
                    english_list.append(line)
                    english_list.append("\n")

    english_file_name = os.path.join(path_to_output_dir, file_name.split(".", 1)[0]+"_english.txt")
    hindi_file_name = os.path.join(path_to_output_dir, file_name.split(".", 1)[0]+"_hindi.txt")

    print path_to_output_dir
    print file_name.split(".", 1)[0]+"_english.txt"
    print os.path.join(path_to_output_dir, file_name.split(".", 1)[0]+"_english.txt")
    print english_file_name

    with open(english_file_name, 'w') as english_output_file:
        for line in english_list:
            english_output_file.write(line)
            english_output_file.write("\n")

    with open(hindi_file_name, 'w') as hindi_output_file:
        for line in hindi_list:
            hindi_output_file.write(line)
            hindi_output_file.write("\n")





