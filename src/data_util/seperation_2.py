import os, ntpath
import codecs
from langdetect import detect
import json, urllib
import string
from nltk.tokenize import wordpunct_tokenize
from googletrans import Translator

total_count = 0
english_count = 0
hindi_count = 0
unknown_count = 0
sentences_skipped = 0

def detect_lang_googlepack(text):
    translator = Translator()
    try:
        obj = translator.detect(text)
        return obj.lang
    except:
        print ("Error in "+text)
        #print(traceback.format_exc(3))
        return 'un'

def detect_lang(text):
    try:
        return detect(text)
    except:
        return detect_lang_googlepack(text)

def google_trans_call(word):
    param = "text=" + urllib.parse.quote_plus(word) + "&ime=transliteration_en_hi&ie=utf-8&oe=utf-8"
    url = "http://www.google.com/inputtools/request?" + param
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request).read()
    jsonObj = json.loads(response)
    #print jsonObj
    try:
        val = jsonObj[1][0][1][0]
        return val
    except IndexError:
        return word


def transliterate_google(sentence):
    token_list = wordpunct_tokenize(sentence)
    transliterated_list = []
    for token in token_list:
        if token in string.punctuation:
            transliterated_list.append(token)
        else:
            transliterated_list.append(google_trans_call(token))

    trans_sent = " ".join(transliterated_list)
    return (trans_sent, "google")

def get_comments(path_to_file):
    with codecs.open(path_to_file, 'r', encoding="utf-8") as file:
        data_list = file.readlines()
        final_list = []
        for line in data_list:
            line = line.strip()
            if len(line) < 0:
                continue
            else:
                final_list.append(line)
        return final_list

path_to_dir = "/Users/vault/Desktop/transliterated_and_segregated"
path_to_output = "/Users/vault/Desktop/transliterated_and_segregated_output"
#path_to_dir = "/Users/vault/Desktop/raw"
#path_to_output = "/Users/vault/Desktop/raw_output"
for file_path in os.listdir(path_to_dir):
    file_name = ntpath.basename(file_path)
    if file_name.endswith("english.txt") is False:
        continue
    else:
        base_file_name = file_name.split("_english.txt")[0]
        print("Processing file: " + base_file_name)
        english_file_path = os.path.join(path_to_dir, file_name)
        english_data = get_comments(english_file_path)

        english_list = []
        hindi_list = get_comments(os.path.join(path_to_dir, base_file_name + "_hindi.txt"))
        unknown_list = get_comments(os.path.join(path_to_dir, base_file_name + "_unknown.txt"))

        for line in english_data:
            line = line.strip()
            if len(line) <= 0:
                continue

            split_data = line.split(" ", 2)
            if len(split_data) != 3:
                print("Skipping line: " + line)
                continue
            comment = split_data[2]

            total_count+=1
            language = detect_lang(comment)

            if language == 'en':
                english_list.append(line)
                english_count+=1
                continue

            google_lang = detect_lang_googlepack(comment)
            if google_lang == 'hi':
                try:
                    trans_line = transliterate_google(comment)[0]
                except:
                    print("Error in transliteration. Skipping line: " + line)
                    unknown_list.append(line)
                    sentences_skipped += 1
                    continue
                line = split_data[0] + " " + split_data[1] + " " + trans_line
                hindi_list.append(line)
                hindi_count+=1
            else:
                unknown_list.append(line)
                unknown_count+=1

        english_file_name = os.path.join(path_to_output, base_file_name + "_english.txt")
        hindi_file_name = os.path.join(path_to_output, base_file_name + "_hindi.txt")
        unknown_file_name = os.path.join(path_to_output, base_file_name + "_unknown.txt")

        # print path_to_output_dir
        # print file_name.split(".", 1)[0]+"_english.txt"
        # print os.path.join(path_to_output_dir, file_name.split(".", 1)[0]+"_english.txt")
        # print english_file_name

        with codecs.open(english_file_name, 'w', encoding="utf-8") as english_output_file:
            for line in english_list:
                english_output_file.write(line)
                english_output_file.write("\n")

        with codecs.open(hindi_file_name, 'w', encoding="utf-8") as hindi_output_file:
            for line in hindi_list:
                hindi_output_file.write(line)
                hindi_output_file.write("\n")

        with codecs.open(unknown_file_name, 'w', encoding="utf-8") as unknown_output_file:
            for line in unknown_list:
                unknown_output_file.write(line)
                unknown_output_file.write("\n")


print ("Total count: " + str(total_count))
print ("English count: " + str(english_count))
print ("Hindi count: " + str(hindi_count))
print ("Unknown: "+str(unknown_count))
print ("Sentences skipped: "+str(sentences_skipped))