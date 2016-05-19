import sys
import os
import time
import Modules.training.Trainer as trainer

from Modules.calibration import *
from Modules.speechAnalytics.config import *
from Modules.keywordExtraction import *
from Modules.training.filePreparation import *


if __name__ == "__main__":

    processStartedTime = time.time()

    root = sys.path[0]
    os.chdir(root)
    sys.path.append(root + '\\Modules')
    libsFolder = os.path.realpath('.')
    outputFolder = os.path.realpath('..') + "\\Output\\"

    modelFolder = os.path.realpath('..') + "\\Model\\en-us"



##  Training Model
    sampleRate = 8000
    originalModel = "cmusphinx-en-us-ptm-8khz-5.2"
    originalModelFolder = modelFolder  + originalModel
    sphinxBinPath = root + "\\SphinxTrain\\bin\\Release\\x64"
##
    dictionaryFile = modelFolder + "\\cmudict-en-us.dict"
    acousticModel = modelFolder + "\\en-us"
    transcription = trainingSetFolder + "Test.12.txt"
    recording = trainingSetFolder + "Test.12.wav"
    kwsfile = outputFolder + "kwsfile.txt"
    optkws = outputFolder + "\\optkws.txt"
    refsfile = outputFolder + "\\refs.txt"

    print("Executing pipeline")
    print("dictionaryFile: " + dictionaryFile)
    print("transcription: " + transcription)
    print("recording: " + recording)
    print("kwsfile: " + kwsfile)
    print("optkws: " + optkws)
    print("refsfile: " + refsfile)




    print("Training Model...")
    trainer.run(root, originalModel, originalModelFolder)


    print("Processing words...")
    subProcessStartedTime = time.time()
    words = extraction(transcription, dictionaryFile)
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
    refs = reference(keyhash=keywords, inputtext=transcription, refsfile=refsfile)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(refs)

    print("Processing calibration...")
    subProcessStartedTime = time.time()
    config = Config(acousticModel, dictionaryFile, recording, kwsfile)
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
