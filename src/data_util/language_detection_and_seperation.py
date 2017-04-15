import os, ntpath, codecs, traceback
import json, urllib
import string
from nltk.tokenize import wordpunct_tokenize
from googletrans import Translator
from langdetect import detect


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
    param = "text=" + urllib.quote_plus(word) + "&ime=transliteration_en_hi&ie=utf-8&oe=utf-8"
    url = "http://www.google.com/inputtools/request?" + param
    jsonObj = json.loads(urllib.request(url).read())
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
    trans_sent = string.join(transliterated_list)
    return (trans_sent, "google")


def transliterate_to_hindi(sentence):
    global total_count
    trans_sent = transliterate_google(sentence)
    total_count+=1
    return trans_sent


total_count = 0
package_count = 0
sentences_skipped = 0

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
    unknown_list = []
    file_name = ""
    with codecs.open(file_path, 'r', encoding="utf-8") as file:
        file_name = ntpath.basename(file.name)
        print (file.name)
        data_list = file.readlines()
        count = 1;
        for line in data_list:
            try:
                line = line.strip()
                if len(line) <= 0:
                    continue

                split_data = line.split(" ", 2)
                if len(split_data) != 3:
                    print ("Skipping line: " + line)
                    continue
                comment = split_data[2]

                language = detect_lang(comment)
                if language == "en":
                    english_list.append(line)
                elif language == "hi":
                    hindi_list.append(line)
                else:
                    google_lang = detect_lang_googlepack(comment)
                    #for a hindi comment in Latin - google detects the language as Hindi
                    if google_lang == "hi":
                        try:
                            transliterated_line = transliterate_to_hindi(comment)[0]
                        except:
                            print("Error in transliteration. Skipping line: " + line)
                            unknown_list.append(line)
                            sentences_skipped += 1
                            continue
                        line = split_data[0] + " " + split_data[1] + " " + transliterated_line
                        hindi_list.append(line)
                    else:
                        unknown_list.append(line)
                count+=1
            except:
                print (traceback.format_exc(3))
                print ("Except - Skipping line ("+str(count)+"): "+ line)

    english_file_name = os.path.join(path_to_output_dir, file_name.split(".", 1)[0]+"_english.txt")
    hindi_file_name = os.path.join(path_to_output_dir, file_name.split(".", 1)[0]+"_hindi.txt")
    unknown_file_name = os.path.join(path_to_output_dir, file_name.split(".", 1)[0] + "_unknown.txt")

    #print path_to_output_dir
    #print file_name.split(".", 1)[0]+"_english.txt"
    #print os.path.join(path_to_output_dir, file_name.split(".", 1)[0]+"_english.txt")
    #print english_file_name

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

print
print ("Sentences transliterated: "+str(total_count))
print ("Sentence transliterated through polyglot: "+str(package_count))
print ("Sentences skipped: "+str(sentences_skipped))

