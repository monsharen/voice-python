import sys, os
import Modules.word_align
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

Root = os.path.realpath('.')  # "C:\\Users\\a.ericsson\\PycharmProjects\\SpeechAnalytics\\Voice_Python\\Libs"
modeldir = "..\\Model"
datadir = "..\\Datasets\\TrainingSet"


def speechanalytics(config):
    kws = config.get_string('-kws')
    keyphrase = config.get_string('-keyphrase')

    lm = config.get_string('-lm')

    stream = open(config.getAudioFile(), "rb")

    result = ''
    if (kws != None) or (keyphrase == "keyphrase"):
        print("kws: " + str(kws) + ", lm: " + str(lm))
        result = keyword_spotting(config, stream)

    elif lm == "lm":
        result = transcribe(config, stream)

    return result

def transcribe(config, stream):
    decoder = Decoder(config.getSphinxConfig())
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


def keyword_spotting(config, stream,threshold=20):
    result = []
    decoder = Decoder(config.getSphinxConfig())
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
