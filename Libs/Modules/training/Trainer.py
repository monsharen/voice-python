from subprocess import call
import shutil
import os
from distutils.dir_util import copy_tree


# current = sys.path[0]
# root = os.path.realpath('..\\..\\..')


def run(rootDirectory, originalModel, originalModelFolder, trainingSet="The Obama Deception"):
    sphinxBinPath = rootDirectory + "\\SphinxTrain\\bin\\Release\\x64"
    trainingFolder = rootDirectory + "\\Datasets\\trainingSet\\" + trainingSet
    modelFolder = rootDirectory + "\\Model\\"
    newLanguangeModel = createAdaption(modelFolder, originalModel, trainingSet, originalModelFolder) + "\\"
    newAcousticModel = newLanguangeModel + "\\" + originalModel
    outputFolder = trainingFolder
    call(get_sphinx_fe_command(newAcousticModel, trainingFolder, trainingSet, outputFolder, sphinxBinPath))
    call(get_mdef_convert_command(sphinxBinPath, newAcousticModel))
    call(get_bw_command(sphinxBinPath, newAcousticModel, newLanguangeModel, trainingFolder, trainingSet))
    call(get_mllr_solve_command(sphinxBinPath, newAcousticModel, trainingFolder))
    create_newModel(newLanguangeModel)
    call(get_map_adapt_command(sphinxBinPath, newAcousticModel, trainingFolder, newLanguangeModel))


def createAdaption(modelFolder, originalModel, trainingSet, originalModelFolder):
    adaptFolder = modelFolder + "\\" + originalModel + "_Adapt_" + trainingSet
    if os.path.exists(adaptFolder):
        shutil.rmtree(adaptFolder, ignore_errors=True)
    os.makedirs(adaptFolder)
    copy_tree(originalModelFolder, adaptFolder)
    return adaptFolder

def get_sphinx_fe_command(newAcousticModel, trainingFolder, trainingSet, outputFolder, sphinxBinPath, sampleRate=16000):
    return [sphinxBinPath + "\\sphinx_fe",
            "-argfile", newAcousticModel + "\\feat.params",
            "-samprate", str(sampleRate),
            "-c", trainingFolder + "\\" + trainingSet + ".fileids.txt",
            "-di", trainingFolder,
            "-do", outputFolder,
            "-ei", "wav",
            "-eo", "mfc",
            "-mswav", "yes"]

def get_mdef_convert_command(sphinxBinPath, newAcousticModel):
    return [
        sphinxBinPath + "\\pocketsphinx_mdef_convert",
        "-text", newAcousticModel + "\\mdef",
        newAcousticModel + "\\mdef.txt"
    ]


def get_bw_command(sphinxBinPath, newAcousticModel, newLanguangeModel, trainingFolder, trainingSet):
    return [
        sphinxBinPath + "\\bw",
        "-hmmdir", newAcousticModel,
        "-moddeffn", newAcousticModel +"\\mdef.txt",
        "-ts2cbfn", ".cont.",
         "-feat", "1s_c_d_dd",
        # "-svspec", "0-12/13-25/26-38",
        "-lda", newAcousticModel + "\\feature_transform",
        "-cmn", "current",
        "-agc", "none",
        "-dictfn", newLanguangeModel +  "\\cmudict-en-us.dict",
        "-ctlfn", trainingFolder + "\\" + trainingSet + ".fileids.txt",
        "-lsnfn", trainingFolder + "\\" + trainingSet + ".transcription.txt",
        "-accumdir", trainingFolder,
        "-cepdir", trainingFolder
    ]

def get_mllr_solve_command(sphinxBinPath, newAcousticModel, trainingFolder):
    return [
        sphinxBinPath + "\\mllr_solve",
        "-meanfn", newAcousticModel + "\\means",
        "-varfn", newAcousticModel + "\\variances",
        "-outmllrfn", "mllr_matrix",
        "-accumdir", trainingFolder
    ]

def get_map_adapt_command(sphinxBinPath, newAcousticModel, trainingFolder, newLanguangeModel):
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

def create_newModel(newLanguangeModel):
    final = newLanguangeModel + "\\final"
    if os.path.exists(final):
        shutil.rmtree(final, ignore_errors=True)
    os.makedirs(final)
