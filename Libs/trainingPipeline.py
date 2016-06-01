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

    #   Output
    outputFolder = root + "\\Output\\"

    #   Input
    trainingSet = "Obama_Cairo_University"
    #trainingSet = "arctic"
    inputFolder = root + "\\Datasets\TrainingSet\\" + trainingSet + "\\"
    modelFolder = root + "\\Model\\cmusphinx-en-us-5.2"
    fileIdsFile = inputFolder + "fileids.txt"
    transcriptionFile = inputFolder + "transcription.txt"
    originalAudioFile = inputFolder + trainingSet + '.wav'
    kwsfile = outputFolder + "kwsfile.txt"
    optkws = outputFolder + "optkws.txt"

    #   Training Model
    sampleRate = 16000
    originalModel = "cmusphinx-en-us-5.2"
    originalModelFolder = root + "\\model\\" + originalModel  # + originalModel
    sphinxBinPath = root + "\\SphinxTrain\\bin\\Release\\x64"

    dictionaryFile = modelFolder + "\\cmudict-en-us.dict"
    acousticModel = modelFolder + "\\cmusphinx-en-us-5.2"

    kwsfile = outputFolder + "kwsfile.txt"
    optkws = outputFolder + "optkws.txt"
    refsfile = outputFolder + "refs.txt"

    print("Executing pipeline")
    print("dictionaryFile: " + dictionaryFile)
    print("transcriptionFile: " + transcriptionFile)
    print("originalAudioFile: " + originalAudioFile)
    print("kwsfile: " + kwsfile)
    print("optkws: " + optkws)
    print("refsfile: " + refsfile)

    print("Training Model...")
    trainer.run(root, originalModel, originalModelFolder, sampleRate=sampleRate, trainingSet=trainingSet)
