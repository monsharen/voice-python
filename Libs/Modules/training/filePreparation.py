import os,sys,time

from Modules.training.trainingFilesUtil import *
from Modules.training.trainTestSplitt import *
from Modules.keywordExtraction import extraction, randomSampling, reference

root = os.path.realpath('../../..')  # sys.path[0]
os.chdir(root)
sys.path.append(root + '\\Modules')

if __name__ == "__main__":

    #  Trainingset File Preparation config

    #  Input
    #trainingSet = "Obama_Cairo_University"
    dataSetFolder = "The_Obama_Deception"
    #trainingSet = "arctic"
    trainingSetFolder = os.path.realpath('../../../') + "\\Datasets\\" + dataSetFolder + "\\TrainingSet\\"
    testSetFolder = os.path.realpath('../../../') + "\\Datasets\\" + dataSetFolder + "\\TestSet\\"
    metaDataFolder = os.path.realpath('../../../') + "\\Datasets\\" + dataSetFolder + "\\MetaData\\"

    modelFolder = root + "\\Model\\en-us"
    audioInputFile = trainingSetFolder + dataSetFolder + '.wav'
    subtitlesFile = trainingSetFolder + dataSetFolder + '.srt'
    dictionaryFile = modelFolder + "\\cmudict-en-us.dict"

    #  Output
    fileIdsInputFile = trainingSetFolder + "fileids.txt"
    trainingTranscriptionOutputFile = trainingSetFolder + "transcription.txt"
    fullTranscriptionOutputFile = metaDataFolder + "full_transcription.txt"
    testTranscriptionFile = testSetFolder + "transcription.txt"
    kwsFile = metaDataFolder + "kwsfile.txt"
    referenceFile = metaDataFolder + "reference_file.txt"
    #  End config

    print("Parsing subs from file '" + subtitlesFile + "'...")
    subtitlesArray = subtitleGeneration(subtitlesFile)

    print("Opening file ids file '" + fileIdsInputFile + "'...")
    fileIdsFile = open(fileIdsInputFile, "w")

    print("Opening transcription file '" + trainingTranscriptionOutputFile + "'...")
    transcriptionFile = open(trainingTranscriptionOutputFile, "w", encoding="utf-8")
    transcriptionRawFile = open(fullTranscriptionOutputFile, "w", encoding="utf-8")

    print("Opening audio input file '" + audioInputFile + "'...")
    audioFile = wave.open(audioInputFile, 'r')

    print("Creating Test and Training Split...")
    train, test = trainTestSplit(fileIds=fileIdsInputFile, subArray=subtitlesArray)

    print("Generating test files ...")
    generateTranscript(test, testTranscriptionFile)
    start = test[0][0]
    end = test[-1][1]
    generateAudioFiles(testSetFolder, audioFile, start, end, dataSetFolder)

    print("Generating training files...")
    for (index, value) in enumerate(train):
        start, end, text = value
        fileid = dataSetFolder + "_" + str(index)
        generateAudioFiles(trainingSetFolder, audioFile, start, end, fileid)
        generateTrainingTranscription(transcriptionFile, text, fileid)
        generateFileIds(fileIdsFile, fileid)
    fileIdsFile.close()
    transcriptionFile.close()
    print("Done")
    print("Training folder: " + trainingSetFolder)
    print("Test folder: " + testSetFolder)

    print("Processing words...")
    generateTranscript(subtitlesArray, fullTranscriptionOutputFile)

    subProcessStartedTime = time.time()
    words = extraction(fullTranscriptionOutputFile, dictionaryFile)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(words)

    print("Processing keywords...")
    subProcessStartedTime = time.time()
    keywords = randomSampling(words, 100, phones=[6], kws=kwsFile)
    kws = open(kwsFile, 'rb')
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(keywords)

    print("Processing reference...")
    subProcessStartedTime = time.time()
    refs = reference(keyhash=keywords, inputtext=fullTranscriptionOutputFile, refsfile=referenceFile)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(refs)
