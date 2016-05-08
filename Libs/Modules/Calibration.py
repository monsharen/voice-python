__author__ = 'a.ericsson'

import sys, os
from Modules.speechAnalytics.speech import *
from Modules.speechAnalytics.Config import *
from Modules.word_align import *
import numpy as np

def calhelper(parameter,parRange,keywordsfile,recording,refs):
    hyps = {}
    languagemodel, languagedictionary
    for par in parRange:
        config = createConfig(kwsfile = keywordsfile, audiofile = recording, optType = {parameter : par })
        hyp=speechanalytics(config)
        alignment = align(refs,[word[0] for word in hyp])
        hyps[str(par)]=hyp

    return hyps

def calibration(refkeywords,config):

    infile = open(refkeywords, "r")
    refs = [ word for word in " ".join(infile.readlines()).split()]

    if parameter == "beam":
        parRange = np.logspace(-80,-40,5)

    elif parameter == "kws-delay":
        parRange = np.arange(10,0,-1)

    elif parameter == "wip":
        parRange = np.arange(0.0,0.5,0.05)

    elif parameter == "lw":
        parRange = np.arange(0,5.5,0.5)

    elif parameter == "wbeam":
        parRange = np.logspace(-30,-5,6)

    elif parameter == "oog":
        outfile = open(adjustkwsfile,"w")
        parRange = np.logspace(-20,50,15)
        oogwords = { word:[] for word in refs }

        hyps = calhelper(parmeter,parRange)

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

    hyps = calhelper(parameter, parRange, keywordsfile, recording,refs)
    return hyps

def compare(refs,hyp):
    """
    Takes a reference file with keywords and compares this with a detected keyword sequence
    """

    infile = open(refs, "r")
    refs = [word for word in " ".join(infile.readlines()).split()]
    alignment = align(refs,[word[0] for word in hyp])
    return alignment