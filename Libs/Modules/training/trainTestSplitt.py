__author__ = 'a.ericsson'

## method to create train test split, input train,test portion
### read the file ide file, create an int split
### cut original file and pass to test folder, read and merge all subs into one file.
### adjust fileid file and transcription file

def trainTestSplit(train=0.5,subArray=None):
    size =  len(subArray)
    trainIndex = int(train * size)
    trainFiles = subArray[0:trainIndex]
    testFiles  = subArray[trainIndex:size]
    return [trainFiles,testFiles]

def generateTranscript(testFiles, rawTranscription):
    testTranscription=" ".join([element[-1] for element in testFiles] )
    transcription = open(rawTranscription,'w',encoding="utf8")
    transcription.write(testTranscription + " ")
    transcription.close()

def PDATrainTestSplit(transcriptionHash):
    trainFiles = []
    testFiles =  []
    for speaker in transcriptionHash.keys():
        speakerTrainFiles, speakerTestFiles = trainTestSplit(subArray=transcriptionHash[speaker])
        trainFiles.append(speakerTrainFiles)
        testFiles.append(speakerTestFiles)
    return [sum(trainFiles,[]),sum(testFiles,[])]

#def PDAWordFrequencyPerSpeaker(transcriptionHash,words):
    #wordFrequency = {for speaker in transcriptionHash.keys() for }

    #for speaker in transcriptionHash.keys():

