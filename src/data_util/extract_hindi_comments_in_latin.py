#use python2

from polyglot.text import Text

import os
import ntpath
import traceback
import codecs
import urllib2, json, urllib
from polyglot.transliteration import Transliterator
from nltk.tokenize import wordpunct_tokenize
import string

total_count = 0
package_count = 0

def google_trans_call(word):
    param = "text=" + urllib.quote_plus(word) + "&ime=transliteration_en_hi&ie=utf-8&oe=utf-8"
    url = "http://www.google.com/inputtools/request?" + param
    jsonObj = json.loads(urllib2.urlopen(url).read())
    #print jsonObj
    try:
        val = jsonObj[1][0][1][0]
        return val
    except IndexError:
        return word
    except:
        print word
        print jsonObj
        print traceback.format_exc(3)

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
    total_count+=1
    try:
        return transliterate_google(sentence)
    except:
        global package_count
        package_count+=1
        english_hindi_transliterator = Transliterator(source_lang="en", target_lang="hi")
        token_list = sentence.split(' ')
        transliterated_sent = ""
        for token in token_list:
            transliterated_sent += english_hindi_transliterator.transliterate(token) + " "
        return (transliterated_sent.strip(), "polyglot")

print "Extracting hindi comments in Latin"

path_to_dir = "/Users/vault/Desktop/Data"
path_to_output_file = "/Users/vault/Desktop/transliteration.txt"

file_list = []
for file_path in os.listdir(path_to_dir):
    file_name = ntpath.basename(file_path)
    if file_name.endswith(".txt"):
        file_list.append(os.path.join(path_to_dir, file_name))

#print str(file_list)

google_list = []
polyglot_list = []

for file_path in file_list:
    with codecs.open(file_path, 'r', encoding="utf-8") as file:
        file_name = ntpath.basename(file.name)
        print file.name
        data_list = file.readlines()
        count = 1;
        for line in data_list:
            try:
                line = line.strip()
                if len(line) <= 0:
                    continue

                split_data = line.split(" ", 2)
                if len(split_data) != 3:
                    print "Skipping line: " + line
                    continue
                comment = split_data[2]

                text = Text(comment)

                if text.language.code != "hi" and text.language.code != "en":
                    transliterated_line, tool = transliterate_to_hindi(comment)
                    transliterated_lang = Text(transliterated_line)
                    if transliterated_lang.language.code == "hi":
                        if tool == "google":
                            google_list.append((comment, transliterated_line))
                        else:
                            polyglot_list.append((comment, transliterated_line))

            except:
                print traceback.format_exc(3)
                print "Except - Skipping line ("+str(count)+"): "+ line


with codecs.open(path_to_output_file, 'w', encoding="utf-8") as output_file:
    for comment, trans in google_list:
        output_file.write("G "+comment)
        output_file.write("\n")
        output_file.write("G " + trans)
        output_file.write("\n")
        output_file.write("\n")

    for comment, trans in polyglot_list:
        output_file.write("P " + comment)
        output_file.write("\n")
        output_file.write("P " + trans)
        output_file.write("\n")
        output_file.write("\n")


print
print "Sentences transliterated: "+str(total_count)
print "Sentence transliterated through polyglot: "+str(package_count)
