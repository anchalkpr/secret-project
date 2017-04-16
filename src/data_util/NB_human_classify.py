import os, ntpath, codecs
import sys

path_to_NB_english_data = "/Users/vault/Desktop/NB/nb_sent_english_1.txt"
path_to_NB_hindi_data = "/Users/vault/Desktop/NB/nb_sent_hindi_1.txt"

path_to_NB_english_output = "/Users/vault/Desktop/nb_train_english_1.txt"
path_to_NB_hindi_output = "/Users/vault/Desktop/nb_train_hindi_1.txt"

inp = input("Enter E for english data and H for hindi data: ")
path = ""
path_output = ""
if inp.lower().startswith("h"):
    path = path_to_NB_hindi_data
    path_output = path_to_NB_hindi_output
    print ("Displaying Hindi data: ")
else:
    path = path_to_NB_english_data
    path_output = path_to_NB_english_output
    print ("Displaying English data: ")

with codecs.open(path_output, 'w', encoding="utf-8") as output_file:
    with codecs.open(path, 'r', encoding="utf-8") as file:
        data_list = file.readlines()
        if len(data_list)%2 !=0:
            print ("Number of lines in the file not a multiple of 2. Exiting")
            sys.exit(1)
        limit = len(data_list)//2
        for i in range(0, limit):
            file_no = i * 2
            comment_no = (i * 2) +1
            print ("Sentence "+str(i+1) +" of "+str(len(data_list)/2))
            print ("File: "+str(data_list[file_no].strip()))
            print ("Comment: "+str(data_list[comment_no].strip()))
            inp = input("Enter 1 or 0: ")
            output_file.write(inp+" "+data_list[comment_no].strip())
            output_file.write("\n")
            print ("\n"*5)

print ("Done!")