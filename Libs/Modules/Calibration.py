__author__ = 'a.ericsson'

from Modules.speechAnalytics.speech import *
from Modules.wordAlign import *
import json
import numpy as np
import demjson


def scienceToString(number):

    number,exponent = number.split('e')
    if number > 0 :
        outputkey = str([0]*number+"."+"0")
    elif number < 0 :
        outputkey = 1


class PerformanceStats():
    performanceStats = []

    def __init__(self):
        self.performanceStats=

    def update(self,par):
        self.performanceStats

    def calculate(self,alignment,par):

    def get_Stats(self):
        return self.performanceStats()



class TestClass():

    def __init__(self,refs,hyps,parameter=None,parameterRange=None):
        self.refs = refs,
        self.hyps = hyps
        self.parameter = parameter
        self.parameterRange = parameterRange
        if parameterRange != None

        else:
            self.performanceStats = {word:{'TP':0,'FP':0 ,'FN':0,'WER':0,'freq':refs.count(word)} for word in refs for par in parameterRange}

    def parameterOptimization(self,config,parameterRange,parameter):
        hypsForPar={}
        for par in parameterRange:
            print("updating config for par")
            config.update({parameter:par})
            hyp = speechanalytics(config)
            hypsForPar[str(par)]= hyp

        return hypsForPar

    def performanceStatsCalculation(self,refs,hyps):

        alignment = align(refs,hyps)

        for (ref, hyp) in alignment['alignment']:
            if ref != hyp:
                if ref == '-':
                    w = self.performanceStats.get(hyp.lower())
                    if w is not None:
                        self.performanceStats[hyp.lower()]['FP'] += 1
                elif hyp == '-':
                    self.performanceStats[ref.lower()]['FN'] += 1
                else:
                    w = self.performanceStats.get(hyp.lower())
                    if w is not None:
                        self.performanceStats[hyp.lower()]['FP'] += 1
                    w = self.performanceStats.get(ref.lower())
                    if w is not None:
                        self.performanceStats[ref.lower()]['FN'] += 1
            elif ref == hyp:
                self.performanceStats[ref.lower()]['TP'] +=1

    def performanceEvaluation(self, refs,hyps):
        performanceStatsOog = {}
        for par in self.parameterRange:
            hyp = hyps[str(par)]
            performanceStats = wordStats(refs,hyp)

        return performanceStats


    def performanceEvaluation(self, refs,hyps):

        for par in hyps['parameterRange']:
            hyp = hyps[str(par)]
            alignment = align(refs, [word[0] for word in hyp])

            for (ref, hyp) in alignment['alignment']:
                if ref != hyp:
                    if ref == '-':
                        w = performanceStats.get(hyp.lower())
                        if w is not None:
                            performanceStats[hyp.lower()][par]['FP'] +=1
                    elif hyp == '-':
                        performanceStats[ref.lower()][par]['FN'] +=1
                    else:
                        w = performanceStats.get(hyp.lower())
                        if w is not None:
                            performanceStats[hyp.lower()][par]['FP'] +=1
                        w = performanceStats.get(ref.lower())
                        if w is not None:
                            performanceStats[ref.lower()][par]['FN'] +=1
                elif ref == hyp:
                    performanceStats[ref.lower()][par]['TP'] +=1

        return performanceStats

    def bestPar(self, performanceStats,parameterRange,optkws):
        bestParWord = {}
        outfile = open(optkws,"w")
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

                print("word: " + str(word) + " " + "wer: " + str(wer) + " " +  "bestWer: " + str(bestWer) +" " + "bestPar: " + str(bestPar))

            bestParWord[word]=bestPar
            outfile.write(word + "/" + str(bestPar) + "/\n" )

        return bestParWord

def saveHypsToDisk(config, parameterRange, parameter):
    outfile = open("C:/Users/a.ericsson/PycharmProjects/SpeechAnalytics/Voice_Python/Datasets/PDAm1/MetaData/serialhyps1.txt", "w")   # <--- change filename
    hypsForPar = parameterOptimization(config,parameterRange,parameter)
    outfile.write(str(hypsForPar))
    outfile.close()

def readHypsFromDisk():
    file = open("C:/Users/a.ericsson/PycharmProjects/SpeechAnalytics/Voice_Python/Datasets/PDAm1/MetaData/serialhyps1.txt", "r")  # <--- change filename
    jsonData = file.readline()
    return demjson.decode(jsonData)

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
        #parameterRange = np.logspace(-10,50,7)
        #hyps = saveHypsToDisk(config, parameterRange, parameter)
        hyps = readHypsFromDisk()
        performanceStats= performanceEvaluation(refs, hyps)
        bestOog = bestPar(performanceStats,hyps['parameterRange'],optkws)

        return [performanceStats,bestOog]

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

def compare_transcription(refsFile,hypsFile):
    refs = open(refsFile,"r")
    hyps = open(hypsFile,"r")
    refsArray = []
    hypsArray = []
    results = {'alignments':[],'total':{'Ins':[],'Del':[],'Subs':[],'totalC':0}}
    totalRefs= 0

    for line in refs.readlines():
        text, fileId = line.split('(')
        words = [w for w in text.split(" ")]
        fileId=fileId.strip()
        refsArray.append( [fileId.rstrip(')'),words])
        totalRefs+=len(words)
        print(totalRefs)
    results['total']['totalC']=totalRefs

    for line in hyps.readlines():
        text, fileId = line.split('(')
        words = [w for w in text.split(" ")]
        fileId=fileId.strip()
        hypsArray.append( [fileId.rstrip(')'),words])

    for index in range(0,len(hypsArray)):
        print(refsArray[index])
        result = align(refsArray[index][1],hypsArray[index][1])
        results['alignments'].append([hypsArray[0],result['Ins'],result['Del'],result['Subs']])
        results['total']['Ins'].append(result['Ins'])
        results['total']['Del'].append(result['Del'])
        results['total']['Subs'].append(result['Subs'])

    return results