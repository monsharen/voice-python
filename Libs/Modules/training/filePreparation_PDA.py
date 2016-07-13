import os,sys,time

from Modules.training.trainingFilesUtil import *
from Modules.training.trainTestSplitt import *
from Modules.keywordExtraction import extraction, randomSampling, reference, targetSampling
from shutil import copy

if __name__ == "__main__":

    #root = os.path.realpath('../../..')  # sys.path[0]
    #os.chdir(root)
    #sys.path.append(root + '\\Modules')

    #  Trainingset File Preparation config

    #  Input
    dataSetFolder = "PDAm1"
    inputDatasetFolder = os.path.realpath('.') + "\\Datasets\\" + dataSetFolder  + "\\inputData\\"
    trainingSetFolder = os.path.realpath('.') + "\\Datasets\\" + dataSetFolder + "\\TrainingSet\\"
    testSetFolder = os.path.realpath('.') + "\\Datasets\\" + dataSetFolder + "\\TestSet\\"
    metaDataFolder = os.path.realpath('.') + "\\Datasets\\" + dataSetFolder + "\\MetaData\\"

    modelFolder = root + "\\Model\\en-us"
    dictionaryFile = modelFolder + "\\cmudict-en-us.dict"
    sentInputFile = inputDatasetFolder + "PDAm.wsj.transcription"

    #  Output
    trainingTranscriptionOutputFile = trainingSetFolder + "transcription.txt"
    testTranscriptionOutputFile = testSetFolder + "transcription.txt"
    testTranscriptionOutputFile1 = testSetFolder + "transcriptions.txt"
    fullTranscriptionOutputFile = metaDataFolder + "full_transcription.txt"
    trainingFileIdOutputFile = trainingSetFolder + "fileids.txt"
    testFileIdOutputFile = testSetFolder + "fileids.txt"
    kwsFile = metaDataFolder + "kwsfile.txt"
    referenceFile = metaDataFolder + "reference_file.txt"
    testOutputAudioFile = testSetFolder + dataSetFolder + ".wav"

    #  End config

    print("Opening files :" + trainingTranscriptionOutputFile + "\n" + testTranscriptionOutputFile + "\n" + fullTranscriptionOutputFile + "\n" + trainingFileIdOutputFile + "\n" + testFileIdOutputFile)
    trainingTranscriptionFile = open(trainingTranscriptionOutputFile, "w", encoding="utf-8")
    testTranscriptionFile1 = open(testTranscriptionOutputFile1, "w", encoding="utf-8")
    transcriptionRawFile = open(fullTranscriptionOutputFile, "w", encoding="utf-8")
    trainingFileIdsFile = open(trainingFileIdOutputFile, "w", encoding="utf-8")
    testFileIdsFile = open(testFileIdOutputFile, "w", encoding="utf-8")
    transcriptHash,sentArray,wordSpeakerFreq = sent2transcription(sentInputFile)

    def generateFiles(fileIdFile,transcriptionFile,inputarray):
        for (index, value) in enumerate(inputarray):
            fileId = value[0]
            text = value[1]
            generateTrainingTranscription(transcriptionFile, text, fileId)
            generateFileIds(fileIdFile,fileId)
        fileIdFile.close()
        transcriptionFile.close()

    def transferFiles(inputArray, outputFolder):
        for element in inputArray:
            id = element[0]
            originalFileId = id + "_5.wav"
            newFileId = id + ".wav"
            incat,non = id.split('_')
            non,incat = incat.split("m")
            cat = '0' + incat
            source = inputDatasetFolder+cat +"\\" + originalFileId
            destination = outputFolder + newFileId
            copy(source, destination)

    print("Creating Test and Training Split...")
    train, test = PDATrainTestSplit(transcriptionHash=transcriptHash)

    print("Generating training files...")
    generateFiles(trainingFileIdsFile,trainingTranscriptionFile,train)
    generateFiles(testFileIdsFile,testTranscriptionFile1,test)

    print("Done")
    print("Training folder: " + trainingSetFolder)
    print("Test folder: " + testSetFolder)

    print("Processing words...")
    generateTranscript(sentArray, fullTranscriptionOutputFile)

    transferFiles(train,trainingSetFolder)
    transferFiles(test,testSetFolder)
    concatenateAudioFiles(test,testSetFolder,testOutputAudioFile)
    generateTranscript(test, testTranscriptionOutputFile)

    subProcessStartedTime = time.time()
    words = extraction(fullTranscriptionOutputFile, dictionaryFile,wordspeakerFreq=wordSpeakerFreq)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))

    print("Processing keywords...")
    subProcessStartedTime = time.time()
    keywords = targetSampling(words, phones=[5,6], kws=kwsFile)
    kws = open(kwsFile, 'rb')

    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(keywords)

    print("Processing reference...")
    subProcessStartedTime = time.time()
    refs = reference(keyhash=keywords, inputtext=testTranscriptionOutputFile, refsfile=referenceFile)
    print("Process took %s seconds" % (time.time() - subProcessStartedTime))
    print(refs)
