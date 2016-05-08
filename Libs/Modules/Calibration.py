__author__ = 'a.ericsson'

import sys, os

#  Root = "C:\\Users\\a.ericsson\\PycharmProjects\\SpeechAnalytics\\Voice_Python\\Libs"
#  os.chdir(Root)
#  sys.path.append(Root+'\\Modules')
from Modules.speech import keyword_spotting, detectionconfig, defaultconfig, speechanalytics
from Modules.word_align import *

def calibration(refkeywords,adjustkwsfile,keywordsfile,recording):
    """
    Takes and inputfile with keywords outputs a keywords file with adjusted Out of Grammat Thresholds
    """

    hyps = {}
    kwsOog = [1e-50,1e-40,1e-30,1e-20,1e-10,1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1e+1,1e+10,1e+20,1e+30,1e+40,1e+50]
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