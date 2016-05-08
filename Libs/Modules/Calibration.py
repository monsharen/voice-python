__author__ = 'a.ericsson'

import sys, os

Root = "C:\\Users\\a.ericsson\\PycharmProjects\\SpeechAnalytics\\Voice_Python\\Libs"
os.chdir(Root)
sys.path.append(Root+'\\Modules')
from speech import keyword_spotting, detectionconfig, defaultconfig, speechanalytics
from word_align import *
import numpy as np

def calibration(refkeywords,adjustkwsfile,keywordsfile,recording):
    """
    Takes and inputfile with keywords outputs a keywords file with adjusted Out of Grammat Thresholds
    """


    kwsOog = np.logspace(-20,50,15)
    beam  = np.logspace(-80,-40,5)
    wbeam =np.logspace(-30,-5,6)
    kwsdelay = np.arange(10,0,-1)
    lw = np.arange(0,5.5,0.5)
    wip = np.arange(0.0,0.5,0.05)




    hyps = {}
    infile = open(refkeywords, "r")
    outfile = open(adjustkwsfile,"w")
    refs = [ word for word in " ".join(infile.readlines()).split()]
    oogwords = { word:[] for word in refs }

    for oog in kwsOog:
        hyp = speechanalytics(OOG=oog,kwsfile=keywordsfile,audiofile=recording)

        alignment = align(refs,[word[0] for word in hyp])
        hyps[str(oog)] = hyp
        for (ref, hyp) in alignment['alignment']:
            if ref==hyp:
                oogwords[ref].append(oog)

    for keyword in oogwords.keys():
        try: max(oogwords[keyword])
        except:
            outfile.write(keyword+"\n")
        else:
            outfile.write(keyword + "/" + str(max(oogwords[keyword])) + "/\n" )
    outfile.close()
    return hyps

def compare(refs,hyp):
    """
    Takes a reference file with keywords and compares this with a detected keyword sequence
    """

    infile = open(refs, "r")
    refs = [word for word in " ".join(infile.readlines()).split()]
    alignment = align(refs,[word[0] for word in hyp])
    return alignment