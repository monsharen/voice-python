from subprocess import call
import shutil
import os
import sys
from distutils.dir_util import copy_tree

current = sys.path[0]
root = os.path.realpath('..\\..\\..')
modelFolder = root + "\\Model\\"


trainingSet = "The Obama Deception"
trainingFolder = root + "\\Datasets\\trainingSet\\" + trainingSet


def createAdaption():
    adaptFolder = modelFolder + "\\" + originalModel + "_Adapt_" + trainingSet
    if os.path.exists(adaptFolder):
        shutil.rmtree(adaptFolder, ignore_errors=True)
    os.makedirs(adaptFolder)
    copy_tree(originalModelFolder,adaptFolder)
    return adaptFolder

newLanguangeModel = createAdaption() + "\\"
newAcousticModel = newLanguangeModel + "\\" + originalModel
outputFolder = trainingFolder

def get_sphinx_fe_command():
    return [sphinxBinPath + "\\sphinx_fe",
            "-argfile", newAcousticModel + "\\feat.params",
            "-samprate", str(sampleRate),
            "-c", trainingFolder + "\\" + trainingSet + ".fileids.txt",
            "-di", trainingFolder,
            "-do", outputFolder,
            "-ei", "wav",
            "-eo", "mfc",
            "-mswav", "yes"]

def get_mdef_convert_command():
    return [
        sphinxBinPath + "\\pocketsphinx_mdef_convert",
        "-text", newAcousticModel + "\\mdef",
        newAcousticModel + "\\mdef.txt"
    ]

def get_bw_command():
    return [
        sphinxBinPath + "\\bw",
        "-hmmdir", newAcousticModel,
        "-moddeffn", newAcousticModel +"\\mdef.txt",
        "-ts2cbfn", ".cont.",
         "-feat", "1s_c_d_dd",
        #"-svspec", "0-12/13-25/26-38",
        "-lda", newAcousticModel + "\\feature_transform",
        "-cmn", "current",
        "-agc", "none",
        "-dictfn", newLanguangeModel +  "\\cmudict-en-us.dict",
        "-ctlfn", trainingFolder + "\\" + trainingSet + ".fileids.txt",
        "-lsnfn", trainingFolder + "\\" + trainingSet + ".transcription.txt",
        "-accumdir", trainingFolder,
        "-cepdir", trainingFolder
    ]

def get_mllr_solve_command():
    return [
        sphinxBinPath + "\\mllr_solve",
        "-meanfn", newAcousticModel + "\\means",
        "-varfn", newAcousticModel + "\\variances",
        "-outmllrfn", "mllr_matrix",
        "-accumdir", trainingFolder
    ]

def get_map_adapt_command():
    return [
        sphinxBinPath + "\\" + "map_adapt",
        "-moddeffn", newAcousticModel + "\\" + "mdef.txt",
        "-ts2cbfn", ".ptm.",
        "-meanfn", newAcousticModel + "\\means",
        "-varfn", newAcousticModel + "\\variances",
        "-mixwfn", newAcousticModel + "\\mixture_weights",
        "-tmatfn", newAcousticModel+ "\\transition_matrices",
        "-accumdir", trainingFolder,
        "-mapmeanfn", newLanguangeModel + "\\final" + "\\means",
        "-mapvarfn",  newLanguangeModel + "\\final" + "\\variances",
        "-mapmixwfn", newLanguangeModel + "\\final" + "\\mixture_weights",
        "-maptmatfn", newLanguangeModel + "\\final" + "\\transition_matrices"
    ]

def create_newModel():
    final = newLanguangeModel + "\\final"
    if os.path.exists(final):
        shutil.rmtree(final, ignore_errors=True)
    os.makedirs(final)
