__author__ = 'a.ericsson'

from subprocess import call
import shutil
import os
from distutils.dir_util import copy_tree

class pocketsphinx_batch():

    filedirectory = ''
    fileids = ''
    kwsfile = ''
    acousticModel = ''
    dictionary = ''
    result = None

    def __init__(self,rootDirectory, dataSet, model, result):
        self.filedirectory = dataSet.trainingSet.folder
        self.fileids = dataSet.trainingSet.fileIdsFile
        self.kwsfile = dataSet.metaData.optkwsFile
        self.acousticModel = model.acousticModel
        self.dictionary = model.dictionaryFile
        self.result = result
        self.sphinxBinPath = rootDirectory + "\\SphinxTrain\\bin\\Release\\x64"

    def applyconfig(self):
        return [self.sphinxBinPath + "\\pocketsphinx_batch",
                "-adcin", "yes",
                "-cepdir", self.filedirectory,
                "-cepext", ".wav",
                "-ctl", self.fileids,
                "-kws", self.kwsfile,
                "-hmm", self.acousticModel,
                "-dict", self.dictionary,
                "-hyp", self.result.serialHypsFile,
                #"-kws_plp", str(1e+5),
                #"-kws_threshold", str(10000),
                #"-verbose", "true",
                #"-pbeam", "1e-48",
                #"-pl_beam", "1e-100",
                #"-pl_pbeam", "1e-100",
                #"-pl_pip", "100.0"
                #"-kws_delay",
                #"-mllr", self.acousticModel + "\\mllr_matrix"
                ]

    def run(self):
        command = self.applyconfig()
        print("command")
        print(command)
        call(command)
