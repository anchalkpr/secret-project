import re
import codecs
import os
import traceback

pattern1 = re.compile("^0 ")
pattern2 = re.compile("^1 ")

DATA_DIR = "../../data/NB/traning_data/"

def getTrainingDataFiles():
    try:
        inputFilesList = {"english":[], "hindi":[]}
        for file in os.listdir(DATA_DIR):
            if file.split("_")[-2] == "english":
                inputFilesList["english"].append(file)
            elif file.split("_")[-2] == "hindi":
                inputFilesList["hindi"].append(file)
        print(inputFilesList)
        return inputFilesList
    except:
        errorMsg = "ERROR: Error while I/O %s" %(traceback.format_exc())
        print(errorMsg)

def segregateIntoClasses():
    filesPerLanguage = getTrainingDataFiles()
    
    for language, files in filesPerLanguage.items():
        validData = []
        invalidData = []
        for file in files:
            dataFile = codecs.open(DATA_DIR+file, mode='r', encoding='utf-8')
            data = dataFile.readlines()
            for line in data:
                line=line.strip()
                if re.match(pattern1, line):
                    invalidData.append(re.sub(pattern1, "", line))
                elif re.match(pattern2, line):
                    validData.append(re.sub(pattern2, "", line))
            dataFile.close()
        validDataOutputFile = codecs.open(DATA_DIR+"valid_data_"+language+".txt", mode='w', encoding='utf-8')
        validDataOutputFile.write('\n'.join(validData))
        invalidDataOutputFile = codecs.open(DATA_DIR+"invalid_data_"+language+".txt", mode='w', encoding='utf-8')
        invalidDataOutputFile.write('\n'.join(invalidData))
        validDataOutputFile.close()
        invalidDataOutputFile.close()
        
segregateIntoClasses()