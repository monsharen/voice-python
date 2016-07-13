import wave
from shutil import copy

def subtitleGeneration(subsFile):
    subsArray = []
    start = ""
    end = ""
    text = ''
    numbers = {i: 'number' for i in range(0, 100000)}
    totalSeconds = [60*60, 60, 1]
    with open(subsFile, 'r') as f:
        for line in f:
            if len(line.split('-->')) == 2:
                if len(start) >= 1:
                    subsArray.append([startS, endS, text.strip()])
                    text = ""
                start, end = [i.strip() for i in line.split('-->')]
                startS = sum([float(value.replace(',', '.')) * totalSeconds[index] for (index, value) in enumerate(start.split(':'))])
                endS = sum([float(value.replace(',', '.')) * totalSeconds[index] for (index, value) in enumerate(end.split(':'))])
            else:
                try:
                    int(line)
                except:
                    clean = " ".join([w.strip('.,:;!?"[]-').lower()for w in line.split()])
                    text = text + " " + clean
                    text.strip()
    return subsArray

def sent2transcription(sent):

    transcriptionHash = {}
    speakerFreq = {}
    wordSpeakerFreq = {}
    sentArray=[]

    with open(sent,"r") as f :
        for line in f :
            text, fileid = line.split('(')
            words = [w.strip('.,:;!?"[]-').lower()for w in text.split()]
            clean = " ".join(words)
            clean = clean.strip()
            fileid = fileid.split(")")[0]
            speaker, transcriptId = fileid.split('_')

            for word in words:
                if wordSpeakerFreq.get(word) != None:
                    wordSpeakerFreq[word].add(speaker)
                else:
                    wordSpeakerFreq[word]=set()
                    wordSpeakerFreq[word].add(speaker)

            sentArray.append([fileid,clean])
            if transcriptionHash.get(speaker) is not None:
                transcriptionHash[speaker].append([fileid,clean])
                speakerFreq[speaker].append([w for w in clean.split(" ")])
            else:
                transcriptionHash[speaker]=[[fileid,clean]]
                speakerFreq[speaker]=[[w for w in clean.split(" ")]]

    wordSpeakerFreq = {word:len(wordSpeakerFreq[word]) for word in wordSpeakerFreq.keys()}
    return [transcriptionHash,sentArray,wordSpeakerFreq]

def concatenateAudioFiles(fileArray,testFolder, outputFile):

    outputFile = wave.open(outputFile,"w")
    outputFile.setnchannels(1)
    outputFile.setsampwidth(2)
    outputFile.setframerate(16000)

    for element in fileArray:

        file = element[0]
        inputAudioFile = testFolder + file + ".wav"
        origAudio = wave.open(inputAudioFile,"r")
        frameRate = origAudio.getframerate()
        nChannels = origAudio.getnchannels()
        sampWidth = origAudio.getsampwidth()
        frames = origAudio.getnframes()
        data = origAudio.readframes(frames)
        outputFile.writeframesraw(data)

    outputFile.close()

def generateAudioFiles(trainingSetFolder, origAudio, start, end, fileid):
    frameRate = origAudio.getframerate()
    nChannels = origAudio.getnchannels()
    sampWidth = origAudio.getsampwidth()
    startFrames = start * frameRate
    endFrames = end * frameRate
    origAudio.setpos(int(startFrames))

    chunkData = origAudio.readframes(int(endFrames - startFrames))
    outputFile = trainingSetFolder + fileid + ".wav"
    chunkAudio = wave.open(outputFile, "w")
    chunkAudio.setnchannels(nChannels)
    chunkAudio.setsampwidth(sampWidth)
    chunkAudio.setframerate(frameRate)
    chunkAudio.writeframes(chunkData)
    chunkAudio.close()


def generateTrainingTranscription(transcriptionFile, text, fileid):
    transcript = "<s> " + text + " </s>" + " (" + fileid + ")"
    transcriptionFile.write(transcript + "\n")


def generateFileIds(fileidsFile, fileid):
    fileidsFile.write(fileid + "\n")

def kwsReferenceFile(transcriptionfile,kwshash,referenceOutputFile):
    output = open(referenceOutputFile,"w")
    print(kwshash)
    with open(transcriptionfile, 'r') as f:
        for line in f:
            linekws = []
            text, fileId = line.split('(')
            for word in text.split(" "):
                word = word.strip('.,:;!?"[]-').lower()
                if kwshash.get(word) != None:
                    linekws.append(word.strip())
                    print(linekws)
            output.write(" ".join(w for w in linekws) + "(" + fileId)
    output.close()
