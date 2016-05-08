__author__ = 'a.ericsson'

Root = "C:\\Users\\a.ericsson\\PycharmProjects\\SpeechAnalytics\\Voice_Python\\Libs"
import sys,os
os.chdir(Root)
sys.path.append(Root+'\\Modules')
from word_align import *
from Calibration import *
from speech import keyword_spotting, detectionconfig, defaultconfig, speechanalytics

if __name__ == "__main__":
    hyps = calibration("kwsC.txt","Adjustedkws.txt","kwsC.txt")
    adjustedhyp = speechanalytics(kwsfile="Adjustedkws.txt")
    results = compare("kwsC.txt",adjustedhyp)
    print results