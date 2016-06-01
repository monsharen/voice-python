import os,sys,time

from Modules.training.trainingFilesUtil import *
from Modules.training.trainTestSplitt import *
from Modules.keywordExtraction import extraction, randomSampling, reference

if __name__ == "__main__":

    #  Trainingset File Preparation config

    #  Input
    #trainingSet = "Obama_Cairo_University"
    trainingSet = "The_Obama_Deception"
    #trainingSet = "arctic"
    inputFolder = os.path.realpath('../../../') + "\\Datasets\TrainingSet\\" + trainingSet + "\\"
    testModelFolder = os.path.realpath('../../../') + "\\Datasets\TestSet\\" + trainingSet + "\\"
    root = os.path.realpath('../../..')  # sys.path[0]
    os.chdir(root)
    sys.path.append(root + '\\Modules')
    modelFolder = root + "\\Model\\en-us"
    originalAudioFile = inputFolder + trainingSet +'.wav'
    subsFile = inputFolder + trainingSet + '.srt'
    dictionaryFile = modelFolder + "\\cmudict-en-us.dict"

    #  Output
    outputFolder = inputFolder
    fileIdsInputFile = outputFolder + "fileids.txt"
    transcriptionInputFile = outputFolder + "transcription.txt"
    rawTranscription = outputFolder + "rawtranscription.txt"
    testTranscription = testModelFolder + "transcription.txt"
    kwsfile = outputFolder + "kwsfile.txt"
    refsfile = outputFolder + "refs.txt"
    #  End config

    print("Parsing subs from file '" + subsFile + "'...")
    subArray = subsGeneration(subsFile)

    print("Opening file ids file '" + fileIdsInputFile + "'...")
    fileIdsFile = open(fileIdsInputFile, "w")

    print("Opening transcription file '" + transcriptionInputFile + "'...")
    transcriptionFile = open(transcriptionInputFile, "w", encoding="utf-8")
    transcriptionRawFile = open(rawTranscription, "w", encoding="utf-8")

    print("Opening original audio file '" + originalAudioFile + "'...")
    origAudioFile = wave.open(originalAudioFile, 'r')

    print("Creating Test and Training Split...")
    train, test = trainTestSplit(fileIds=fileIdsInputFile, subArray=subArray)

    print("Generating test files ...")
    generateRawTranscript(test,testTranscription)
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

    print("Processing words...")
    generateRawTranscript(subArray,rawTranscription)

    subProcessStartedTime = time.time()
    words = extraction(rawTranscription, dictionaryFile)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(words)

    print("Processing keywords...")
    subProcessStartedTime = time.time()
    keywords = randomSampling(words, 100, phones=[6], kws=kwsfile)
    kws = open(kwsfile, 'rb')
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(keywords)

    print("Processing reference...")
    subProcessStartedTime = time.time()
    refs = reference(keyhash=keywords, inputtext=rawTranscription, refsfile=refsfile)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(refs)
