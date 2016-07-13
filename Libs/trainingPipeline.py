import Modules.training.Trainer as trainer

from Modules.training.filePreparation import *
from Modules.Calibration import *
from Modules.speechAnalytics.Config import *
from configuration import *

if __name__ == "__main__":

    processStartedTime = time.time()

    dataSetFolder = "PDAm1"
    dataSet = get_data_set(dataSetFolder)


    #modelName = "cmusphinx-en-us-5.2"
    modelName = "cmusphinx-en-us-ptm-5.2"
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
    # trainer.run(root, modelName, model.folder, sampleRate=sampleRate, trainingSet="PDAm1")

    print("Processing calibration...")
    config = Config(model.acousticModel, model.dictionaryFile, dataSet.testSet.audioInputFile, dataSet.metaData.kwsFile)

    wrapper = SpeechAnalyticsWrapper()
    parameterRange = np.logspace(-20, 50, 8)
    hypsforpar = wrapper.parameterOptimization(config, parameterRange=parameterRange, parameter='oog')
    saveToDisk("C:/Users/monsharen/Dropbox/projects/voice-python/Datasets/PDAm1/MetaData/serialhyps1.txt", hypsforpar)
    # alignments, hyps = calibration(refkeywords=dataSet.metaData.referenceFile, config=config, parameter='oog', optkws=dataSet.metaData.optkwsFile)
    calibration(refkeywords=dataSet.metaData.referenceFile, outputFile=dataSet.metaData.optkwsFile, parameter='oog')

    #refs = open(dataSet.metaData.referenceFile, "r")
    #hyps = readJsonFromDisk("C:/Users/monsharen/Dropbox/projects/voice-python/Datasets/PDAm1/MetaData/serialhyps1.txt")

    # performanceStats, bestOogForWord = OogCalibaration(refs, hyps)

    print("Process took %s seconds" % (time.time() - processStartedTime))

