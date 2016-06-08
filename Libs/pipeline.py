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
    dataSet = get_data_set("The_Obama_Deception")
    # dataSetFolder, testSetFolder, metaDataFolder, transcriptionInputFile, audioInputFile = get_data_set("The_Obama_Deception")
    # modelFolder, dictionaryFile, acousticModel = get_model("en-us")
    model = get_model("en-us")

    print("Executing pipeline")
    print(model.print())
    print(dataSet.print())

    # print("Processing words...")
    # subProcessStartedTime = time.time()
    # words = extraction(transcriptionInputFile, dictionaryFile)
    # print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    # print(words)

    print("Reading keywords...")
    # subProcessStartedTime = time.time()
    # keywords = randomSampling(words, 5, phones=[6], kws=kwsfile)
    kws = open(dataSet.metaData.optkws, 'r')
    keywords = [ word for word in " ".join(kws.readlines()).split() ]
    # print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(keywords)

    print("Reading reference file...")
    subProcessStartedTime = time.time()
    referenceFile = open(dataSet.metaData.referenceFile, 'r')  # reference(keyhash=keywords, inputtext=transcriptionInputFile, refsfile=refsfile)
    referenceArray = [word for word in " ".join(referenceFile.readlines()).split()]
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(referenceArray)

    config = Config(model.acousticModel, model.dictionaryFile, dataSet.testSet.audioInputFile, dataSet.metaData.optkws)
    config.update({"ogg": 1e+30, "kws": "test"})

    print("Processing speech analytics...")
    subProcessStartedTime = time.time()
    hypothesis = speechanalytics(config)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(hypothesis)
    print(referenceArray)

    print("Comparing kwsfile and adjustedhyp")
    subProcessStartedTime = time.time()
    results = compare(dataSet.metaData.referenceFile, hypothesis)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(results)

    insertions = results['Ins']
    substitutions = results['Subs']
    deletions = results['Del']

    wordErrorRate = float(insertions + deletions + substitutions) / len(referenceArray) * 100
    print("Word error rate:" + str(wordErrorRate))
    print("Entire process completed in %s seconds" % (time.time() - processStartedTime))
