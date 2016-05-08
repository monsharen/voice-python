__author__ = 'a.ericsson'

import sys, os
from Modules.speechAnalytics.speech import *
from Modules.speechAnalytics.Config import *

from Modules.word_align import *
import numpy as np

def calhelper(config, parRange, refs):
    hyps = {}
    alignments = []
    for par in parRange:
        print("updating config for par ")
        config.update({'beam': par, 'kws': 'asd'})
        hyp = speechanalytics(config)
        alignment = align(refs, [word[0] for word in hyp])
        hyps[str(par)] = hyp
        alignments.append(alignment)

    return [alignments, hyps]

def calibration(refkeywords, config, parameter):

    infile = open(refkeywords, "r")
    refs = [word for word in " ".join(infile.readlines()).split()]

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

        #  elif parameter == "oog":
        #  outfile = open(adjustkwsfile,"w")
        #  parRange = np.logspace(-20,50,15)
        #  oogwords = { word:[] for word in refs }

        #  hyps = calhelper(parmeter,parRange)

        #  for (ref, hyp) in alignment['alignment']:
        #     if ref==hyp:
        #          oogwords[ref].append(oog)

        #  for keyword in oogwords.keys():
        #      try: max(oogwords[keyword])
        #      except:
        #          outfile.write(keyword+"\n")
        #      else:
        #          outfile.write(keyword + "/" + str(max(oogwords[keyword])) + "/\n" )

        #  outfile.close()
    #  return hyps

    alignments, hyps = calhelper(config, parRange, refs)
    return [alignments, hyps]

def compare (refs,hyp):
    """
    Takes a reference file with keywords and compares this with a detected keyword sequence
    """

    infile = open(refs, "r")
    refs = [word for word in " ".join(infile.readlines()).split()]
    alignment = align(refs,[word[0] for word in hyp])
    return alignment