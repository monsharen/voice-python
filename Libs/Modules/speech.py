__author__ = 'a.ericsson'
__author__ = 'a.ericsson'

import sys, os
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

Root = "C:\\Users\\a.ericsson\\PycharmProjects\\SpeechAnalytics\\Voice_Python\\Libs"
os.chdir(Root)
sys.path.append(Root + '\\Modules')
modeldir = "..\\Model"
datadir = "..\\Datasets\\TrainingSet"
import word_align

    beam  = np.logspace(-80,-40,5)
    wbeam =np.logspace(-30,-5,6)
    kwsdelay = np.arange(10,0,-1)
    lw = np.arange(0,5.5,0.5)
    wip = np.arange(0.0,0.5,0.05)

def speechanalytics(audiofile="", type="kws", kwsfile="", OOG=None, wip=None,):
    stream = stream = open(os.path.join(datadir, audiofile), "rb")
    config = detectionconfig(type, OOG, kwsfile,WIP=wip,LW=lw,BEAM=beam,WBEAM=wbeam,KWSDELAY=kwsdelay)
    if type == "kws" or "keyphrase":
        result = keyword_spotting(config, stream, OOG)
    elif type == "lm":
        result = transcribe(config, stream)
    return result


# Create a decoder with certain model
def defaultconfig():
    config = Decoder.default_config()
    config.set_string('-hmm', os.path.join(modeldir, 'en-us/en-us'))
    config.set_string('-dict', os.path.join(modeldir, 'en-us/cmudict-en-us.dict'))
    return config


def detectionconfig(type, OOG,kwsfile):
    config = defaultconfig()

    if type == "kws":
        config.set_string('-kws', os.path.join(Root, kwsfile))
        if OOG != None:
            config.set_float('-kws_threshold', OOG)
        return config

    elif type == "keyphrase":
        config.set_string('-keyphrase', os.path.join(Root, 'keyphrase.txt'))
        config.set_float('-kws_threshold', OOG)
        return config

    elif type == "lm":
        config = defaultconfig()
        config.set_string('-lm', os.path.join(modeldir, 'en-us/en-us.lm.bin'))
        return config


def transcribe(config, stream):
    decoder = Decoder(config)
    decoder.start_utt()
    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
    decoder.end_utt()
    hypothesis = decoder.hyp()
    return hypothesis.hypstr


def keyword_spotting(config, stream, OOG,threshold=20):
    result = []
    decoder = Decoder(config)
    decoder.start_utt()

    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
        if decoder.hyp() != None:
            for seg in decoder.seg():
                if seg.prob > threshold:
                    result.append([seg.word, seg.prob, seg.start_frame, seg.end_frame])
            decoder.end_utt()
            decoder.start_utt()
    return result