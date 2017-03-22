import codecs
import os
import traceback
import re

p = re.compile("\d+ \d+ ")

DATA_DIR = "../../Data/"
STRIPPED_DATA_DIR = "../../Stripped_Data/"

def strip_data(inputFile):
    output_file_data = []
    output_line = ""
    with codecs.open(inputFile, mode="r", encoding="utf-8") as inputFile:
        lines = inputFile.readlines()
    for line in lines:
        line = line.strip()
        if p.match(line):
            output_file_data.append(output_line)
            output_line = ""
        output_line += line + " "
        
    return output_file_data[1:]

def read_files():
    try:
        inputFilesList = [inputfile for inputfile in os.listdir(DATA_DIR)]
        
        for inputFile in inputFilesList:
            output_file_path = STRIPPED_DATA_DIR + inputFile
            output_file_data = strip_data(DATA_DIR + inputFile)
            with codecs.open(output_file_path, mode="w", encoding="utf-8") as outputFile:
                outputFile.write("\n".join(output_file_data))
                print("stripping file: %s" %output_file_path)
            
    except:
        errorMsg = "ERROR: Error while I/O %s" %(traceback.format_exc())
        print(errorMsg)
        
read_files()