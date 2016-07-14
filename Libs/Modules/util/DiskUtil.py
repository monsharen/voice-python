import demjson
import json

def saveToDisk(fileName, data):
    outfile = open(fileName, "w")
    outfile.write(str(data))
    outfile.close()

def readJsonFromDisk(fileName):
    file = open(fileName, "r")  # <--- change filename
    jsonData = file.readline()
    return demjson.decode(jsonData)