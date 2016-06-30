__author__ = 'a.ericsson'

from Modules.speechAnalytics.speech import *

from Modules.wordAlign import *
import numpy as np

def calhelper(config, parRange, refs, parameter):
    hyps = {}
    alignments = []
    for par in parRange:
        print("updating config for par ")
        config.update({parameter: par})
        hyp = speechanalytics(config)
        alignment = align(refs, [word[0] for word in hyp])
        hyps[str(par)] = hyp
        if parameter == 'oog':
            alignments.append([par,alignment])
        else:
            alignments.append(alignment)
    return [alignments, hyps]

def calibration(refkeywords, config, parameter, optkws = None):

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

    elif parameter == "oog":
        outfile = open(optkws,"w")
        parRange = np.logspace(-50,50,5)
        oogwords = { word:[] for word in refs }
        alignments, hyps = calhelper(config, parRange, refs, parameter)

        for (oog,alignment) in alignments:
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
        return alignments, hyps

    alignments, hyps = calhelper(config, parRange, refs, parameter)
    return [alignments, hyps]

def compare (refs,hyp):
    """
    Takes a reference file with keywords and compares this with a detected keyword sequence
    """

    infile = open(refs, "r")
    refs = [word for word in " ".join(infile.readlines()).split()]
    alignment = align(refs,[word[0] for word in hyp])
    return alignment
