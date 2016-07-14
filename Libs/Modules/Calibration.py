__author__ = 'a.ericsson'
from  collections import defaultdict
from Modules.speechAnalytics.speech import *
from Modules.wordAlign import *
from Modules.util.DiskUtil import *

import numpy as np


class SpeechAnalyticsWrapper:

    def parameterOptimization(self, config, parameterRange, parameter):
        hypsForPar = {}
        for par in parameterRange:
            print("updating config for par")
            config.update({parameter: par})
            hyp = speechanalytics(config)
            hypsForPar[str(par)] = hyp

        return hypsForPar


class ParameterOptimizationStatistics:
    hypsForPar = ''

    def __init__(self, hypsForPar):
        self.hypsForPar = hypsForPar

    def getPerformanceStatistics(self, refs):
        performanceStats = {word: {str(par): {'TP': 0, 'FP': 0, 'FN': 0, 'WER': 0, 'freq': refs.count(word)} for par in self.hypsForPar.keys()} for word in refs}

        for par in self.hypsForPar.keys():
            hyp = self.hypsForPar[str(par)]
            alignment = align(refs, [word[0] for word in hyp])

            for (ref, hyp) in alignment['alignment']:
                if ref != hyp:
                    if ref == '-':
                        w = performanceStats.get(hyp.lower())
                        if w is not None:
                            performanceStats[hyp.lower()][str(par)]['FP'] +=1
                    elif hyp == '-':
                        performanceStats[ref.lower()][str(par)]['FN'] +=1
                    else:
                        w = performanceStats.get(hyp.lower())
                        if w is not None:
                            performanceStats[hyp.lower()][str(par)]['FP'] +=1
                        w = performanceStats.get(ref.lower())
                        if w is not None:
                            performanceStats[ref.lower()][str(par)]['FN'] +=1
                elif ref == hyp:
                    performanceStats[ref.lower()][str(par)]['TP'] +=1

        return performanceStats

    def getBestParForWords(self, performanceStats, parameterRange):
        bestParWord = {}
        for word in performanceStats.keys():
            bestWer = None
            bestPar = len(performanceStats)

            for par in parameterRange:
                performanceStats[word][par]['WER'] = float(((performanceStats[word][par]['FP'] +  performanceStats[word][par]['FN']) /performanceStats[word][par]['freq']))
                wer = performanceStats[word][par]['WER']

                if bestWer == None:
                    bestWer = wer
                    bestPar = par

                if wer < bestWer:
                    bestWer = wer
                    bestPar = par

                print("word: " + str(word) + " wer: " + str(wer) + " bestWer: " + str(bestWer) +" bestPar: " + str(bestPar))

            bestParWord[word]=bestPar

        return bestParWord

    def writeStatisticsToFile(self, bestParWord, fileName):
        lines = ""
        for word in bestParWord.keys():
            bestPar = bestParWord[word]
            lines += word + "/" + str(bestPar) + "/\n"
        saveToDisk(fileName, lines)


def OogCalibaration(refs, hyps, outputFile):
    stats = ParameterOptimizationStatistics(hyps)
    performanceStats = stats.getPerformanceStatistics(refs)
    bestOog = stats.getBestParForWords(performanceStats, hyps.keys())
    stats.writeStatisticsToFile(bestOog, outputFile)
    return [performanceStats, bestOog]

def calibration(refkeywords, parameter, outputFile, result):

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

        hyps = readJsonFromDisk(result.serialHypsFile)
        performanceStats, bestOog = OogCalibaration(refs, hyps, outputFile)

        return bestOog

    # alignments, hyps = calhelper(config, parRange, refs, parameter)
    # return [alignments, hyps]
    return []

def compare (refs,hyp):
    """
    Takes a reference file with keywords and compares this with a detected keyword sequence
    """
    infile = open(refs, "r")
    refs = [word for word in " ".join(infile.readlines()).split()]
    alignment = align(refs,[word[0] for word in hyp])
    return alignment

def compare_transcription(refsFile,hypsFile):
    refs = open(refsFile,"r")
    hyps = open(hypsFile,"r")
    refsHash = {}
    hypsHash = {}
    results = {'alignments':[],'total':{'Ins':[],'Del':[],'Subs':[],'totalC':0}}
    totalRefs= 0


    for line in refs.readlines():
        text, fileId = line.split('(')
        words = [w for w in text.split(" ")]
        fileId = fileId.strip()
        refsHash[fileId.rstrip(')')] = words
        totalRefs += len(words)
        print(totalRefs)
    results['total']['totalC']=totalRefs

    for line in hyps.readlines():
        text, fileId = line.split('(')
        text = text.strip()
        print("'" + text + "'")
        words = []
        if len(text) != 0:
            words = [w for w in text.split(" ")]
        fixedFileId = fileId.split(" ")[0].strip()
        hypsHash[fixedFileId] = words

    print(hypsHash)

    for fileId in refsHash.keys():
        # print(refsArray[index])
        print(hypsHash[fileId])
        result = align(refsHash[fileId],hypsHash[fileId])
        results['alignments'].append([fileId,hypsHash[fileId], result['Ins'], result['Del'], result['Subs']])
        results['total']['Ins'].append(result['Ins'])
        results['total']['Del'].append(result['Del'])
        results['total']['Subs'].append(result['Subs'])

    return results