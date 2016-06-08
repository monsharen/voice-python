import Modules.training.Trainer as trainer

from Modules.training.filePreparation import *
from Modules.Calibration import *
from Modules.speechAnalytics.Config import *

if __name__ == "__main__":

    processStartedTime = time.time()

    root = os.path.realpath('..')  # sys.path[0]
    os.chdir(root)
    sys.path.append(root + '\\Modules')
    libsFolder = os.path.realpath('.')

    dataSetFolder = "The_Obama_Deception"

    #   Output
    outputFolder = root + "\\Output\\"
    testSetFolder = root + "\\Datasets\\" + dataSetFolder + "\\TestSet\\"
    metaDataFolder = root + "\\Datasets\\" + dataSetFolder + "\\MetaData\\"

    #   Input
    trainingSetFolder = root + "\\Datasets\\" + dataSetFolder + "\\TrainingSet\\"
    fileIdsFile = trainingSetFolder + "fileids.txt"
    transcriptionInputFile = trainingSetFolder + "transcription.txt"
    kwsInputFile = metaDataFolder + "kwsfile.txt"
    optkwsOutputFile = metaDataFolder + "optkws.txt"
    referenceInputfile = metaDataFolder + "reference_file.txt"
    audioInputFile = trainingSetFolder + dataSetFolder + '.wav'

    #   Training Model
    sampleRate = 16000
    originalModel = "cmusphinx-en-us-5.2"
    originalModelFolder = root + "\\Model\\" + originalModel  # + originalModel
    sphinxBinPath = root + "\\SphinxTrain\\bin\\Release\\x64"
    acousticModel = root + "\\Model\\" + originalModel + "_Adapt_" + dataSetFolder + "\\" + originalModel
    dictionaryFile = originalModelFolder + "\\cmudict-en-us.dict"

    print("Executing pipeline")
    print("transcriptionFile: " + transcriptionInputFile)
    print("kwsfile: " + kwsInputFile)
    print("optkws: " + optkwsOutputFile)

    print("Training Model...")
    trainer.run(root, originalModel, originalModelFolder, sampleRate=sampleRate, trainingSet=dataSetFolder)

    print("Processing calibration...")
    config = Config(acousticModel, dictionaryFile, audioInputFile, kwsInputFile)
    alignments, hyps = calibration(refkeywords=referenceInputfile, config=config, parameter='oog', optkws=optkwsOutputFile)
    print("Process took %s seconds" % (time.time() - processStartedTime))
    print(hyps)
    print(alignments)
