import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import Modules

root = os.path.realpath('..')  # sys.path[0]
os.chdir(root)
sys.path.append(root + '\\Modules')
libsFolder = os.path.realpath('.')


def get_data_set(dataSetName):
    #_dataSetFolder = dataSetName
    #_testSetFolder = root + "\\Datasets\\" + _dataSetFolder + "\\TestSet\\"
    #_metaDataFolder = root + "\\Datasets\\" + _dataSetFolder + "\\MetaData\\"
    #_transcriptionInputFile = _testSetFolder + "transcription.txt"
    #_audioInputFile = _testSetFolder + dataSetName + '.wav'

    _dataSet = DataSet()
    _dataSet.name = dataSetName
    _dataSet.testSet.folder = root + "\\Datasets\\" + _dataSet.name + "\\TestSet\\"
    _dataSet.metaData.folder = root + "\\Datasets\\" + _dataSet.name + "\\MetaData\\"
    _dataSet.testSet.transcriptionInputFile = _dataSet.testSet.folder + "transcription.txt"
    _dataSet.testSet.audioInputFile = _dataSet.testSet.folder + dataSetName + '.wav'

    _dataSet.metaData.kwsFile = _dataSet.metaData.folder + "kwsfile.txt"
    _dataSet.metaData.optkwsFile = _dataSet.metaData.folder + "optkws.txt"
    _dataSet.metaData.referenceFile = _dataSet.metaData.folder + "reference_file.txt"

    _dataSet.trainingSet.folder = trainingSetFolder = root + "\\Datasets\\" + _dataSet.name + "\\TrainingSet\\"
    _dataSet.trainingSet.fileIdsFile = trainingSetFolder + "fileids.txt"
    _dataSet.trainingSet.audioInputFile = trainingSetFolder + _dataSet.name + '.wav'

    return _dataSet


def get_model(modelFolderName):
    _modelFolder = root + "\\Model\\" + modelFolderName
    _dictionaryFile = _modelFolder + "\\cmudict-en-us.dict"
    _acousticModel = _modelFolder + "\\en-us"
    model = Model()
    model.folder = _modelFolder
    model.dictionaryFile = _dictionaryFile
    model.acousticModel = _acousticModel
    return model


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




