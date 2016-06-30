import Modules.training.Trainer as trainer

from Modules.training.filePreparation import *
from Modules.Calibration import *
from Modules.speechAnalytics.Config import *
from configuration import *

if __name__ == "__main__":

    processStartedTime = time.time()

    #root = os.path.realpath('..')  # sys.path[0]
    #os.chdir(root)
    #sys.path.append(root + '\\Modules')
    #libsFolder = os.path.realpath('.')

    dataSetFolder = "PDAm"
    dataSet = get_data_set(dataSetFolder)

    #modelName = "cmusphinx-en-us-5.2"
    modelName = "en-us"
    model = get_model(modelName)

    #   Output
    outputFolder = root + "\\Output\\"

    #   Training Model
    sampleRate = 16000

    sphinxBinPath = root + "\\SphinxTrain\\bin\\Release\\x64"
    acousticModel = root + "\\Model\\" + modelName + "_Adapt_" + dataSetFolder + "\\" + modelName
    dictionaryFile = model.folder + "\\cmudict-en-us.dict"

    print("Executing pipeline")
    dataSet.print()

    print("Training Model...")
   # trainer.run(root, modelName, model.folder, sampleRate=sampleRate, trainingSet=dataSetFolder)

    print("Processing calibration...")
    config = Config(model.acousticModel, model.dictionaryFile, dataSet.testSet.audioInputFile, dataSet.metaData.kwsFile)
    #alignments, hyps = calibration(refkeywords=dataSet.metaData.referenceFile, config=config, parameter='oog', optkws=dataSet.metaData.optkwsFile)
    accuracyWord,bestOogForWord = calibration(refkeywords=dataSet.metaData.referenceFile, config=config, parameter='oog', optkws=dataSet.metaData.optkwsFile)
    print("Process took %s seconds" % (time.time() - processStartedTime))
    print(bestOogForWord)
    #print(alignments)
