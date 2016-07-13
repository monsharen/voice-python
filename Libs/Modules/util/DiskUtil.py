import demjson
import json

def saveToDisk(fileName, data):
    #outfile = open("C:/Users/a.ericsson/PycharmProjects/SpeechAnalytics/Voice_Python/Datasets/PDAm1/MetaData/serialhyps1.txt", "w")   # <--- change filename
    outfile = open(fileName, "w")
    outfile.write(str(data))
    outfile.close()

def readJsonFromDisk(fileName):
    file = open(fileName, "r")  # <--- change filename
    jsonData = file.readline()
    return demjson.decode(jsonData)