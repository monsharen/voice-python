import sys
import os
import time
import Modules.training.Trainer as trainer

from Modules.Calibration import *
from Modules.speechAnalytics.Config import *
from Modules.keywordExtraction import *
from Modules.training.filePreparation import *
from configuration import *

if __name__ == "__main__":

    processStartedTime = time.time()

    root = os.path.realpath('..')  # sys.path[0]
    os.chdir(root)
    sys.path.append(root + '\\Modules')
    libsFolder = os.path.realpath('.')

    #   Input
    dataSet = get_data_set("PDAm1")
    model = get_model("cmusphinx-en-us-ptm-5.2")
    #modelName = "en-us"
    #model = get_model(modelName)
    print("Executing pipeline")
    print(model.print())
    print(dataSet.print())

    print("Reading keywords...")
    kws = open(dataSet.metaData.optkwsFile, 'r')
    #kws = open(dataSet.metaData.kwsFile, 'r')
    #keywords = [ word for word in " ".join(kws.readlines()).split() ]
    #print(keywords)

    print("Reading reference file...")
    referenceFile = open(dataSet.metaData.referenceFile, 'r')
    referenceArray = [word for word in " ".join(referenceFile.readlines()).split()]
    #print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    #print(referenceArray)

    #config = Config(model.acousticModel, model.dictionaryFile, dataSet.testSet.audioInputFile, dataSet.metaData.optkwsFile)
    config = Config(acousticModel=model.acousticModel,languagedictionary=model.dictionaryFile,kwsfile=dataSet.metaData.kwsFile,audiofile=dataSet.testSet.audioInputFile)
    #config = Config(model.acousticModel, model.dictionaryFile, dataSet.testSet.audioInputFile, dataSet.metaData.kwsFile)
    #config.update({"oog":1e+3, "kws":"test"})
    config.update({"kws":"test"})

    print("Processing speech analytics...")
    subProcessStartedTime = time.time()
    hypothesis = speechanalytics(config)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(hypothesis)
    #print(referenceArray)

    print("Comparing alignment to reference")
    subProcessStartedTime = time.time()
    results = compare(dataSet.metaData.referenceFile, hypothesis)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    #print(results)

    insertions = results['Ins']
    substitutions = results['Subs']
    deletions = results['Del']

    wordErrorRate = float(insertions + deletions + substitutions) / len(referenceArray) * 100
    print("Word error rate:" + str(wordErrorRate))
    print("Entire process completed in %s seconds" % (time.time() - processStartedTime))