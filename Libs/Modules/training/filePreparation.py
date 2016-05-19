import os

from Modules.training.trainingFilesUtil import *

if __name__ == "__main__":

    #  Trainingset File Preparation config
    #  Input
    trainingSet = "The Obama Deception"
    inputFolder = os.path.realpath('../../../') + "\\Datasets\TrainingSet\\" + trainingSet + "\\"
    originalAudioFile = inputFolder + 'The_Obama_Deception_HQ_Full_length_version.wav'
    subsFile = inputFolder + "The Obama Deception [English subtitles v7].srt"

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
    transcriptionFile = open(transcriptionInputFile, "w")

    print("Opening original audio file '" + originalAudioFile + "'...")
    origAudioFile = wave.open(originalAudioFile, 'r')

    print("Generating all the files...")
    for (index, value) in enumerate(subArray):
        start, end, text = value
        fileid = trainingSet + "_" + str(index)
        generateAudioFiles(outputFolder, origAudioFile, start, end, fileid)
        generateTranscription(transcriptionFile, text, fileid)
        generateFileIds(fileIdsFile, fileid)
    fileIdsFile.close()
    transcriptionFile.close()
    print("Done")
    print("Output folder: " + outputFolder)



