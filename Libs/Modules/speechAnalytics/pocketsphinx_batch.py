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

    def __init__(self,rootDirectory,filedirectory,fileids,kwsfile,acousticModel,dictionary,results):
        self.filedirectory = filedirectory
        self.fileids = fileids
        self.kwsfile = kwsfile
        self.acousticModel = acousticModel
        self.dictionary = dictionary
        self.sphinxBinPath = rootDirectory + "\\SphinxTrain\\bin\\Release\\x64"
        self.results = results

    def applyconfig(self):
        return [self.sphinxBinPath + "\\pocketsphinx_batch",
                "-adcin", "yes",
                "-cepdir", self.filedirectory,
                "-cepext", ".wav",
                "-ctl", self.fileids,
                "-kws", self.kwsfile,
                "-hmm", self.acousticModel,
                "-dict", self.dictionary,
                "-hyp", self.results,
                #"-kws_plp",str(1e-3),
                "-kws_threshold",str(100),
                #"-kws_delay",
                #"-mllr", self.acousticModel + "\\mllr_matrix"
                ]

    def run(self):
        call(self.applyconfig())
