__author__ = 'a.ericsson'

Root = "C:\\Users\\a.ericsson\\PycharmProjects\\SpeechAnalytics\\Voice_Python\\Libs"
import sys,os
os.chdir(Root)
sys.path.append(Root+'\\Modules')
from word_align import *
from Calibration import *
from speech import keyword_spotting, detectionconfig, defaultconfig, speechanalytics
from keywordExtraction import *
if __name__ == "__main__":

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
    