import sys
import os

#  sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Modules.Calibration import *
from Modules.speech import keyword_spotting, detectionconfig, defaultconfig, speechanalytics
from Modules.keywordExtraction import *

if __name__ == "__main__":

    Root = sys.path[0]  # "C:\\Users\\a.ericsson\\PycharmProjects\\SpeechAnalytics\\Voice_Python\\Libs"
    os.chdir(Root)
    sys.path.append(Root + '\\Modules')

    transcription ="newyork6.txt"
    recording = "newyork6.wav"
    kwsfile = "kwsfile.txt"
    optkws="optkws.txt"

    words = extraction(transcription)
    keywords = randomSampling(words,5, phones = [4,6,8], kws=kwsfile)
    refs = reference(keywords,transcription)


    hyps = calibration(refkeywords="refs.txt",adjustkwsfile=optkws,keywordsfile=kwsfile,recording=recording)
    adjustedhyp = speechanalytics(kwsfile=optkws,audiofile=recording)

    results = compare(kwsfile,adjustedhyp)
