import os

from Modules.training.trainingFilesUtil import *
from Modules.training.trainTestSplitt import *

if __name__ == "__main__":

    #  Trainingset File Preparation config

    #  Input
    #trainingSet = "Obama_Cairo_University"
    trainingSet="The_Obama_Deception"
    #trainingSet = "arctic"
    inputFolder = os.path.realpath('../../../') + "\\Datasets\TrainingSet\\" + trainingSet + "\\"
    testModelFolder = os.path.realpath('../../../') + "\\Datasets\TestSet\\" + trainingSet + "\\"
    originalAudioFile = inputFolder + trainingSet +'.wav'
    subsFile = inputFolder + trainingSet + '.srt'

    #  Output
    outputFolder = inputFolder
    fileIdsInputFile = outputFolder + "fileids.txt"
    transcriptionInputFile = outputFolder + "transcription.txt"
    #  End config

    print("Parsing subs from file '" + subsFile + "'...")
    subArray = subsGeneration(subsFile)

    print("Opening file ids file '" + fileIdsInputFile + "'...")
    fileIdsFile = open(fileIdsInputFile, "w")

    print("Opening transcription file '" + transcriptionInputFile + "'...")
    transcriptionFile = open(transcriptionInputFile, "w", encoding="utf-8")

    print("Opening original audio file '" + originalAudioFile + "'...")
    origAudioFile = wave.open(originalAudioFile, 'r')

    print("Creating Test and Training Split...")
    train, test = trainTestSplit(fileIds=fileIdsInputFile,subArray=subArray)

    print("Generating test files ...")
    generateTestTranscript(test,testModelFolder=testModelFolder)
    start = test[0][0]
    end = test[-1][1]
    generateAudioFiles(testModelFolder,origAudioFile,start,end,trainingSet)

    print("Generating training files...")
    for (index, value) in enumerate(train):
        start, end, text = value
        fileid = trainingSet + "_" + str(index)
        generateAudioFiles(outputFolder, origAudioFile, start, end, fileid)
        generateTranscription(transcriptionFile, text, fileid)
        generateFileIds(fileIdsFile, fileid)
    fileIdsFile.close()
    transcriptionFile.close()
    print("Done")
    print("Training folder: " + outputFolder)
    print("Test folder: " + testModelFolder)