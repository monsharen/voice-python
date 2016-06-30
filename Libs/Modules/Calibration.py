__author__ = 'a.ericsson'

from Modules.speechAnalytics.speech import *

from Modules.wordAlign import *
import json
import numpy as np

def calhelper(config, parRange, refs, parameter):

    previous = {}
    alignments = []
    AccuracyWord = {word:{par:{'TP':0,'FP':0 ,'FN':0,'Accuracy':0,'freq':refs.count(word)}for par in parRange} for word in refs }

    bestOogForWord = {'word':'oog'}
    for par in parRange:
        print("updating config for par ")

        config.update({parameter: par})
        hyp = speechanalytics(config)
        alignment = align(refs, [word[0] for word in hyp])

        for (ref, hyp) in alignment['alignment']:

            if ref != hyp:
                if ref == '-':
                    w = AccuracyWord.get(hyp.lower())
                    if w is not None:
                        AccuracyWord[hyp.lower()][par]['FP'] +=1
                elif hyp == '-':
                    AccuracyWord[ref.lower()][par]['FN'] +=1
                else:
                    w = AccuracyWord.get(hyp.lower())
                    if w is not None:
                        AccuracyWord[hyp.lower()][par]['FP'] +=1
                    w = AccuracyWord.get(ref.lower())
                    if w is not None:
                        AccuracyWord[ref.lower()][par]['FN'] +=1

            if ref == hyp:
                AccuracyWord[ref.lower()][par]['TP'] +=1

        print(AccuracyWord)

        for word in AccuracyWord.keys():
            bestAccuracy = 0
            bestPar = 0
            for par in parRange:
                AccuracyWord[word][par]['Accuracy'] = float(1) - float(AccuracyWord[word][par]['FP'] + AccuracyWord[word][par]['FN'] / AccuracyWord[word][par]['freq'])
                Accuracy = AccuracyWord[word][par]['Accuracy']
                if Accuracy > bestAccuracy:
                    bestAccuracy = Accuracy
                    bestPar = par
            bestOogForWord[word]=bestPar

    return [AccuracyWord,bestOogForWord]

def saveHypsToDisk(config, parRange, refs, parameter):
    outfile = open("filnamn", "w")   # <--- change filename
    hypsForPar = {}
    for par in parRange:
        print("updating config for par ")

        config.update({parameter: par})
        hyp = speechanalytics(config)
        hypsForPar[par] = hyp

    outfile.write(str(hypsForPar))
    outfile.close()

def readHypsFromDisk():
    file = open("filnamn", "r")  # <--- change filename
    jsonData = file.readline()
    return json.loads(jsonData)


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
        parRange = np.logspace(-15,15,3)
        #parRange = [1e+1,1e+25]
        AccuracyWord,bestOogForWord = calhelper(config, parRange, refs, parameter)

        for keyword in bestOogForWord.keys():
            bestOog = bestOogForWord[keyword]
            # allInfo = AccuracyWord[keyword]

            if bestOog == 0:
                outfile.write(keyword+"\n")
            else:
                outfile.write(keyword + "/" + str(bestOog) + "/\n" )

        outfile.close()
        return [AccuracyWord,bestOogForWord]

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
