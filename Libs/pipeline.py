import sys
import os
import time

from Modules.Calibration import *
from Modules.speech import keyword_spotting, detectionconfig, defaultconfig, speechanalytics
from Modules.keywordExtraction import *

if __name__ == "__main__":

    processStartedTime = time.time()

    Root = sys.path[0]
    os.chdir(Root)
    sys.path.append(Root + '\\Modules')
    TrainingSetFolder = os.path.realpath('..') + "\\Datasets\TrainingSet\\"
    ModelFolder = os.path.realpath('..') + "\\Model\\en-us\\"
    LibsFolder = os.path.realpath('.')

    dictionaryFile = ModelFolder + "cmudict-en-us.dict"
    transcription = TrainingSetFolder + "newyork6.txt"
    recording = "newyork6.wav"
    kwsfile = LibsFolder + "\\kwsfile.txt"
    optkws="optkws.txt"
    refsfile = LibsFolder + "\\refs.txt"

    print("Executing pipeline")
    print("dictionaryFile: " + dictionaryFile)
    print("transcription: " + transcription)
    print("recording: " + recording)
    print("kwsfile: " + kwsfile)
    print("optkws: " + optkws)

    print("Processing words...")
    subProcessStartedTime = time.time()
    words = extraction(transcription, dictionaryFile)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(words)

    print("Processing keywords...")
    subProcessStartedTime = time.time()
    keywords = randomSampling(words, 5, phones=[4, 6, 8], kws=kwsfile)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(keywords)

    print("Processing reference...")
    subProcessStartedTime = time.time()
    refs = reference(keyhash=keywords, inputtext=transcription, refsfile=refsfile)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(refs)

    print("Processing calibration...")
    subProcessStartedTime = time.time()
    hyps = calibration(refkeywords="refs.txt", adjustkwsfile=optkws, keywordsfile=kwsfile, recording=recording)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(hyps)

    print("Processing speech analytics...")
    subProcessStartedTime = time.time()
    adjustedhyp = speechanalytics(kwsfile=optkws, audiofile=recording)
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
