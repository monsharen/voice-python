from subprocess import call
import shutil
import os
from distutils.dir_util import copy_tree


# current = sys.path[0]
# root = os.path.realpath('..\\..\\..')


def run(rootDirectory, originalModel, originalModelFolder, trainingSet="PDAm1", sampleRate=16000):
    sphinxBinPath = rootDirectory + "\\SphinxTrain\\bin\\Release\\x64"
    trainingFolder = rootDirectory + "\\Datasets\\" + trainingSet + "\\TrainingSet\\"
    modelFolder = rootDirectory + "\\Model\\"
    newLanguangeModel = createFolder(originalModelFolder, "_Adapt_" + trainingSet,originalModelFolder)
    newAcousticModel = newLanguangeModel + "\\" + originalModel
    datasetAdaptionFolder = createFolder(trainingFolder, "\\" + "AdaptionFolder",)
    print(get_sphinx_fe_command(newAcousticModel, trainingFolder, datasetAdaptionFolder, sphinxBinPath, sampleRate))
    call(get_sphinx_fe_command(newAcousticModel, trainingFolder, datasetAdaptionFolder, sphinxBinPath, sampleRate))

    print(get_mdef_convert_command(sphinxBinPath, newAcousticModel))
    call(get_mdef_convert_command(sphinxBinPath, newAcousticModel))
    call(get_bw_command(sphinxBinPath, newAcousticModel, newLanguangeModel, trainingFolder, datasetAdaptionFolder))
    call(get_mllr_solve_command(sphinxBinPath, newAcousticModel, datasetAdaptionFolder))
    mapAdaptionFolder = createFolder(newLanguangeModel + "\\" + originalModel, "_MAP", copyFolder=newAcousticModel)
    call(get_map_adapt_command(sphinxBinPath, newAcousticModel, datasetAdaptionFolder, mapAdaptionFolder))

def createFolder(inputFolder,outputFolder,copyFolder=None):
    newFolder = inputFolder + outputFolder
    print(newFolder)
    if os.path.exists(newFolder):
        shutil.rmtree(newFolder, ignore_errors=True)
    os.makedirs(newFolder)
    if copyFolder != None:
        copy_tree(copyFolder, newFolder)
    return newFolder

def get_sphinx_fe_command(newAcousticModel, trainingFolder, datasetAdaptionFolder , sphinxBinPath, sampleRate=16000):
    return [sphinxBinPath + "\\sphinx_fe",
            "-argfile", newAcousticModel + "\\feat.params",
            "-samprate", str(sampleRate),
            "-c", trainingFolder + "\\fileids.txt",
            "-di", trainingFolder,
            "-do", datasetAdaptionFolder,
            "-ei", "wav",
            "-eo", "mfc",
            "-mswav", "yes"]

def get_mdef_convert_command(sphinxBinPath, newAcousticModel):
    return [
        sphinxBinPath + "\\pocketsphinx_mdef_convert",
        "-text", newAcousticModel + "\\mdef",
        newAcousticModel + "\\mdef.txt"
    ]

def get_bw_command(sphinxBinPath, newAcousticModel, newLanguangeModel, trainingFolder, datasetAdaptionFolder):
    return [
        sphinxBinPath + "\\bw",
        "-hmmdir", newAcousticModel,
        "-moddeffn", newAcousticModel +"\\mdef.txt",
        "-ts2cbfn", ".ptm.",
         "-feat", "1s_c_d_dd",
         "-svspec", "0-12/13-25/26-38",
        #"-lda", newAcousticModel + "\\feature_transform",
        "-cmn", "current",
        "-agc", "none",
        "-dictfn", newLanguangeModel +  "\\cmudict-en-us.dict",
        "-ctlfn", trainingFolder + "\\fileids.txt",
        "-lsnfn", trainingFolder + "\\transcription.txt",
        "-accumdir",datasetAdaptionFolder ,
        "-cepdir", datasetAdaptionFolder
    ]

def get_mllr_solve_command(sphinxBinPath, newAcousticModel, datasetAdaptionFolder):
    return [
        sphinxBinPath + "\\mllr_solve",
        "-meanfn", newAcousticModel + "\\means",
        "-varfn", newAcousticModel + "\\variances",
        "-outmllrfn", newAcousticModel+ "\\mllr_matrix",
        "-accumdir", datasetAdaptionFolder
    ]

def get_map_adapt_command(sphinxBinPath, newAcousticModel, trainingFolder, mapAdaptionFolder):
    return [
        sphinxBinPath + "\\" + "map_adapt",
        "-moddeffn", newAcousticModel + "\\" + "mdef.txt",
        "-ts2cbfn", ".ptm.",
        "-meanfn", newAcousticModel + "\\means",
        "-varfn", newAcousticModel + "\\variances",
        "-mixwfn", newAcousticModel + "\\mixture_weights",
        "-tmatfn", newAcousticModel+ "\\transition_matrices",
        "-accumdir", trainingFolder,
        "-mapmeanfn", mapAdaptionFolder  + "\\means",
        "-mapvarfn",  mapAdaptionFolder  + "\\variances",
        "-mapmixwfn", mapAdaptionFolder  + "\\mixture_weights",
        "-maptmatfn", mapAdaptionFolder  + "\\transition_matrices"
    ]