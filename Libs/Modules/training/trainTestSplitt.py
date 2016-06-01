__author__ = 'a.ericsson'

## method to create train test split, input train,test portion
### read the file ide file, create an int split
### cut original file and pass to test folder, read and merge all subs into one file.
### adjust fileid file and transcription file

def trainTestSplit(train=0.6,test=0.4,fileIds=None,subArray=None):
    size =  len(subArray)
    trainIndex = int(train * size)
    trainFiles = subArray[0:trainIndex]
    testFiles  = subArray[trainIndex:size]
    return [trainFiles,testFiles]

def generateTranscript(testFiles, rawTranscription):
    testTranscription=" ".join([element[2] for element in testFiles] )
    transcription = open(rawTranscription,'w',encoding="utf8")
    transcription.write(testTranscription + " ")
    transcription.close()

