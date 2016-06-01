import Modules.training.Trainer as trainer

from Modules.training.filePreparation import *


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
    modelFolder = root + "\\Model\\cmusphinx-en-us-5.2"
    fileIdsFile = trainingSetFolder + "fileids.txt"
    transcriptionInputFile = trainingSetFolder + "transcription.txt"
    kwsInputFile = metaDataFolder + "kwsfile.txt"
    optkwsOutputFile = metaDataFolder + "optkws.txt"

    #   Training Model
    sampleRate = 16000
    originalModel = "cmusphinx-en-us-5.2"
    originalModelFolder = root + "\\model\\" + originalModel  # + originalModel
    sphinxBinPath = root + "\\SphinxTrain\\bin\\Release\\x64"

    print("Executing pipeline")
    print("transcriptionFile: " + transcriptionInputFile)
    print("kwsfile: " + kwsInputFile)
    print("optkws: " + optkwsOutputFile)

    print("Training Model...")
    trainer.run(root, originalModel, originalModelFolder, sampleRate=sampleRate, trainingSet=dataSetFolder)
