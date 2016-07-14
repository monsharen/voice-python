import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import Modules
from time import strftime

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
    model.modelFolderName = modelFolderName
    model.folder = _modelFolder
    model.dictionaryFile = _dictionaryFile
    model.acousticModel = _acousticModel
    return model


def get_result(dataSet, model):
    _resultFolder = root + "\\Result\\" + dataSet.name + "_" + model.modelFolderName # + "__" + strftime("%Y-%m-%d_%H%M%S")
    result = Result()
    result.dataSet = dataSet
    result.model = model
    result.resultFolder = _resultFolder
    result.configurationOutputFile = _resultFolder + "\\configuration.txt"
    result.serialHypsFile = _resultFolder + "\\serialhyps.txt"
    return result


class Model():
    modelFolderName = ""
    folder = ""
    dictionaryFile = ""
    acousticModel = ""

    def print(self):
        print("folder: " + self.folder)
        print("dictionaryFile: " + self.dictionaryFile)
        print("acousticModel: " + self.acousticModel)
        print("modelFolderName: " + self.modelFolderName)


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

class Result:
    model = None
    dataSet = None
    configurationOutputFile = ""
    resultFolder = ""
    serialHypsFile = ""


    def print(self):
        print("Result")
        print("configurationFile: " + self.configurationOutputFile)
        print("resultFolder: " + self.resultFolder)
        print("serialHyps: " + self.serialHypsFile)

