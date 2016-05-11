from subprocess import call
import shutil
import os
from distutils.dir_util import copy_tree

sphinxBinPath = "C:\\Users\\monsharen\\Dropbox\\projects\\voice-java\\sphinx\\sphinxtrain\\bin\\Release\\x64"
sourceFolder = "C:\\Users\\monsharen\\Dropbox\\projects\\voice-java\\sphinx\\en-us"
sampleRate = 16000
inputFolder = "C:\\Users\\monsharen\\Dropbox\\projects\\voice-java\\sphinx\\en-us"
outputFolder = "C:\\Users\\monsharen\\Dropbox\\projects\\voice-java\\sphinx\\en-us"


def get_sphinx_fe_command():
    return ["sphinx_fe", sphinxBinPath,
            "sphinx_fe",
            "-argfile", sourceFolder + "en_us\\feat.params",
            "-samprate", str(sampleRate),
            "-c", sourceFolder + "\\artic20.fileids",
            "-di", inputFolder,
            "-do", outputFolder,
            "-ei", "wav",
            "-eo", "mfc",
            "-mswav", "yes"]


def get_mdef_convert_command():
    return [
        sphinxBinPath + "\\pocketsphinx_mdef_convert",
        "-text", inputFolder + "\\en_us\\mdef",
        inputFolder + "\\en_us\\mdef.txt"
    ]


def get_bw_command():
    return [
        sphinxBinPath + "\\bw",
        "-hmmdir", sourceFolder + "\\en_us",
        "-moddeffn", inputFolder + "\\en_us\\mdef.txt",
        "-ts2cbfn", ".ptm",
        "-feat", "1s_c_d_dd",
        "-svspec", "0-12/13-25/26-38",
        "-cmn", "current",
        "-agc", "none",
        "-dictfn", inputFolder + "\\en_us\\cmudict-en-us.dict",
        "-ctlfn", sourceFolder + "\\arctic20.fileids",
        "-lsnfn", sourceFolder + "\\arctic20.transcription",
        "-accumdir", outputFolder,
        "-cepdir", sourceFolder
    ]


def get_mllr_solve_command():
    return [
        sphinxBinPath + "\\mllr_solve",
        "-meanfn", sourceFolder + "\\en_us\\means",
        "-varfn", sourceFolder + "\\en_us\\variances",
        "-outmllrfn", "mllr_matrix",
        "-accumdir", outputFolder
    ]


def get_map_adapt_command():
    return [
        sphinxBinPath + "\\" + "map_adapt",
        "-moddeffn", sourceFolder + "\\" + "en_us" + "\\" + "mdef.txt",
        "-ts2cbfn", ".ptm.",
        "-meanfn", sourceFolder + "\\" + "en_us" + "\\" + "means",
        "-varfn", sourceFolder + "\\" + "en_us" + "\\" + "variances",
        "-mixwfn", sourceFolder + "\\" + "en_us" + "\\" + "mixture_weights",
        "-tmatfn", sourceFolder + "\\" + "en_us" + "\\" + "transition_matrices",
        "-accumdir", outputFolder,
        "-mapmeanfn", sourceFolder + "\\" + "en_us_adapt" + "\\" + "means",
        "-mapvarfn", sourceFolder + "\\" + "en_us_adapt" + "\\" + "variances",
        "-mapmixwfn", sourceFolder + "\\" + "en_us_adapt" + "\\" + "mixture_weights",
        "-maptmatfn", sourceFolder + "\\" + "en_us_adapt" + "\\" + "transition_matrices"
    ]


def create_output_folder():
    languageFolder = sourceFolder + "\\en_us"
    adaptFolder = sourceFolder + "\\en_us_adapt"
    if os.path.exists(adaptFolder):
        shutil.rmtree(adaptFolder, ignore_errors=True)
    os.makedirs(adaptFolder)
    copy_tree(languageFolder, adaptFolder)


call(get_sphinx_fe_command())
call(get_mdef_convert_command())
call(get_bw_command())
call(get_mllr_solve_command())
create_output_folder()
call(get_map_adapt_command())
