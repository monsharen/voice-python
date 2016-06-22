import wave

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
    transcriptionArray = []
    with open(sent,"r") as f :
        for line in f :
            text, fileid = line.split('(')
            clean = " ".join([w.strip('.,:;!?"[]-').lower()for w in text.split()])
            clean = clean.strip()
            fileid = fileid.split(")")[0]
            transcriptionArray.append([fileid,clean])
    return transcriptionArray

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
        print(frameRate)
        print(nChannels)
        print(sampWidth)
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

