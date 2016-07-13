import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import Modules

root = os.path.realpath('..')  # sys.path[0]
os.chdir(root)
sys.path.append(root + '\\Modules')
libsFolder = os.path.realpath('.')


def get_data_set(dataSetName):

    _dataSet = DataSet()
    _dataSet.name = dataSetName
    _dataSet.testSet.folder = root + "\\Datasets\\" + _dataSet.name + "\\TestSet\\"
    _dataSet.metaData.folder = root + "\\Datasets\\" + _dataSet.name + "\\MetaData\\"
    _dataSet.testSet.transcriptionInputFile = _dataSet.testSet.folder + "transcription.txt"
    _dataSet.testSet.audioInputFile = _dataSet.testSet.folder + dataSetName + '.wav'

    _dataSet.metaData.kwsFile = _dataSet.metaData.folder + "kwsfile.txt"
    _dataSet.metaData.optkwsFile = _dataSet.metaData.folder + "optkws.txt"
    _dataSet.metaData.referenceFile = _dataSet.metaData.folder + "reference_file.txt"
    _dataSet.metaData.kwsReferenceFile = _dataSet.metaData.folder + "kwsReference.txt"

    _dataSet.trainingSet.folder = trainingSetFolder = root + "\\Datasets\\" + _dataSet.name + "\\TrainingSet\\"
    _dataSet.trainingSet.fileIdsFile = trainingSetFolder + "fileids.txt"
    _dataSet.trainingSet.audioInputFile = trainingSetFolder + _dataSet.name + '.wav'
    _dataSet.trainingSet.transcriptionInputFile = trainingSetFolder + "transcription.txt"

    return _dataSet


def get_model(modelFolderName):
    _modelFolder = root + "\\Model\\" + modelFolderName
    _dictionaryFile = _modelFolder + "\\cmudict-en-us.dict"
    _acousticModel = _modelFolder + "\\" + modelFolderName
    model = Model()
    model.folder = _modelFolder
    model.dictionaryFile = _dictionaryFile
    model.acousticModel = _acousticModel
    return model

def get_result(dataSet,name):

    _result = _resultFolder + "result.txt"
    Result.name=_name
    Result.configurationFolder=_configurationFolder
    Result.resultFolder=_resultFolder
    Result.result=_result

class Model():
    folder = ""
    dictionaryFile = ""
    acousticModel = ""

    def print(self):
        print("folder: " + self.folder)
        print("dictionaryFile: " + self.dictionaryFile)
        print("acousticModel: " + self.acousticModel)


class MetaData:
    folder = ""
    fullTranscriptionInputFile = ""
    kwsFile = ""
    optkwsFile = ""
    referenceFile = ""
    kwsReferenceFile=""

    def print(self):
        print("MetaData")
        print("folder: " + self.folder)
        print("fullTranscriptionInputFile: " + self.fullTranscriptionInputFile)
        print("kwsFile: " + self.kwsFile)
        print("optkwsFile: " + self.optkwsFile)
        print("referenceFile: " + self.referenceFile)


class TestSet:
    folder = ""
    transcriptionInputFile = ""
    audioInputFile = ""

    def print(self):
        print("TestSet")
        print("folder: " + self.folder)
        print("transcriptionInputFile: " + self.transcriptionInputFile)
        print("audioInputFile: " + self.audioInputFile)


class TrainingSet:
    folder = ""
    fileIdsFile = ""
    audioInputFile = ""
    transcriptionInputFile = ""

    def print(self):
        print("TrainingSet")

class DataSet:
    name = ""
    testSet = TestSet()
    metaData = MetaData()
    trainingSet = TrainingSet()

    def print(self):
        print("DataSet")
        print("name: " + self.name)
        self.testSet.print()
        self.metaData.print()
        self.trainingSet.print()

class Result():
    dataSet=""
    name=""
    configurationFolder = ""
    resultFolder = ""
    result = ""

    def __init__(self,dataSet,name):
        _dataSet=root + "\\Results\\" + dataSet
        _name = root  +"\\Results\\" + dataSet + "\\" + name
        _resultFolder = _name + "\\result\\"
        _configurationFolder = _name + "\\configurationFolder"
        _result= _resultFolder + "results.txt"

        self.name = _name
        self.configurationFolder = _configurationFolder
        self.resultFolder = _resultFolder
        self.result = _result

    def print(self):
        print("Name: " + self.name)
        print("configurationFolder: " + self.configurationFolder)
        print("Result: " + self.resultFolder)

