import wave

def subsGeneration(subsFile):
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


def generateTranscription(transcriptionFile, text, fileid):
    transcript = "<s> " + text + " </s>" + " (" + fileid + ")"
    transcriptionFile.write(transcript + "\n")


def generateFileIds(fileidsFile, fileid):
    fileidsFile.write(fileid + "\n")

