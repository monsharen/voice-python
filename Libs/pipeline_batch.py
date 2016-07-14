__author__ = 'a.ericsson'
import sys
import os
import time
import Modules.training.Trainer as trainer

from Modules.Calibration import *
from Modules.speechAnalytics.Config import *
from Modules.keywordExtraction import *
from Modules.training.filePreparation import *
from configuration import *
from Modules.speechAnalytics.pocketsphinx_batch import *

if __name__ == "__main__":

    processStartedTime = time.time()

    root = os.path.realpath('.')  # sys.path[0]
    os.chdir(root)
    sys.path.append(root + '\\Modules')
    libsFolder = os.path.realpath('.')

    #   Input
    dataSet = get_data_set("PDAm1")
    model = get_model("cmusphinx-en-us-ptm-5.2")
    result = get_result(dataSet, model)
    print("Executing pipeline")
    print(model.print())
    print(dataSet.print())
    print(result.print())

    print("Reading keywords...")
    kws = open(dataSet.metaData.kwsFile, 'r')

    print("Reading reference file...")
    referenceFile = open(dataSet.metaData.kwsReferenceFile, 'r')
    referenceArray = [word for word in " ".join(referenceFile.readlines()).split()]
    print("Processing speech analytics...")
    #pocketbatch = pocketsphinx_batch(root,dataSet.trainingSet.folder,dataSet.trainingSet.fileIdsFile,dataSet.metaData.optkwsFile,model.acousticModel,model.dictionaryFile)
    pocketbatch = pocketsphinx_batch(root, dataSet, model, result)
    pocketbatch.applyconfig()
    pocketbatch.run()

    print("Comparing alignment to reference")
    results = compare_transcription(dataSet.metaData.kwsReferenceFile, result.serialHypsFile)
    print("=== result ===")
    print(results)
    ins,dels,subs = [sum(results['total']['Ins']), sum(results['total']['Del']),sum(results['total']['Subs'])]
    print("Insertions :" + str(ins))
    print("Deletions :" + str(dels))
    print("Substitions :" +  str(subs))
    refsCount = results['total']['totalC']
    print(refsCount)
    WER = float((ins+dels+subs) / refsCount)
    print("WER: " + str(WER))