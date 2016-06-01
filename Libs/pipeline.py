import sys
import os
import time
import Modules.training.Trainer as trainer

from Modules.Calibration import *
from Modules.speechAnalytics.Config import *
from Modules.keywordExtraction import *
from Modules.training.filePreparation import *


if __name__ == "__main__":

    processStartedTime = time.time()

    root = os.path.realpath('..')  # sys.path[0]
    os.chdir(root)
    sys.path.append(root + '\\Modules')
    libsFolder = os.path.realpath('.')

    #   Input
    dataSetFolder = "The_Obama_Deception"
    testSetFolder = root + "\\Datasets\\" + dataSetFolder + "\\TestSet\\"
    metaDataFolder = root + "\\Datasets\\" + dataSetFolder + "\\MetaData\\"

    trainingSetFolder = root + "\\Datasets\\" + dataSetFolder + "\\TrainingSet\\"
    modelFolder = root + "\\Model\\en-us"
    fileIdsFile = trainingSetFolder + "fileids.txt"
    transcriptionInputFile = trainingSetFolder + "transcription.txt"
    audioInputFile = trainingSetFolder + 'The_Obama_Deception.wav'

    dictionaryFile = modelFolder + "\\cmudict-en-us.dict"
    acousticModel = modelFolder + "\\en-us"

    kwsfile = metaDataFolder + "kwsfile.txt"
    optkws = metaDataFolder + "optkws.txt"
    refsfile = metaDataFolder + "refs.txt"

    print("Executing pipeline")
    print("dictionaryFile: " + dictionaryFile)
    print("transcriptionInputFile: " + transcriptionInputFile)
    print("kwsfile: " + kwsfile)
    print("optkws: " + optkws)
    print("refsfile: " + refsfile)

    print("Processing words...")
    subProcessStartedTime = time.time()
    words = extraction(transcriptionInputFile, dictionaryFile)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(words)

    print("Processing keywords...")
    subProcessStartedTime = time.time()
    keywords = randomSampling(words, 5, phones=[6], kws=kwsfile)
    kws = open(kwsfile,'rb')
    #keywords = [ word for word in " ".join(kws.readlines()).split() ]
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(keywords)

    print("Processing reference...")
    subProcessStartedTime = time.time()
    refs = reference(keyhash=keywords, inputtext=transcriptionInputFile, refsfile=refsfile)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(refs)

    print("Processing calibration...")
    subProcessStartedTime = time.time()
    config = Config(acousticModel, dictionaryFile, audioInputFile, kwsfile)
    alignments, hyps = calibration(refkeywords=refsfile, config=config, parameter='oog',optkws=optkws)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(hyps)
    print(alignments)

    print("Processing speech analytics...")
    subProcessStartedTime = time.time()
    adjustedhyp = speechanalytics(config)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(adjustedhyp)

    print("Comparing kwsfile and adjustedhyp")
    subProcessStartedTime = time.time()
    results = compare(kwsfile, adjustedhyp)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(results)

    insertions = results['Ins']
    substitutions = results['Subs']
    deletions = results['Del']

    wordErrorRate = float(insertions + deletions + substitutions) / len(refs) * 100
    print("Word error rate:" + str(wordErrorRate))
    print("Entire process completed in %s seconds" % (time.time() - processStartedTime))
