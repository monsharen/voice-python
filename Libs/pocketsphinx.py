__author__ = 'a.ericsson'

import sys, os
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

Root = "C:\\Users\\a.ericsson\\PycharmProjects\\SpeechAnalytics\\Voice_Python\\Libs"
os.chdir(Root)
modeldir = "..\\Model"
datadir = "..\\Datasets\\TestSet"

def freetext():
    config = lm()
    stream = open(os.path.join(datadir, "Test.12.wav"), "rb")
    text = transcribe(config,stream)
    return  text

def keywords(oog):
    config=kws(oog)
    stream = stream = open(os.path.join(datadir, "Test.1.wav"), "rb")
    result = keyword_spotting(config,stream)
    return  result

# Create a decoder with certain model
def defaultconfig():
    config = Decoder.default_config()
    config.set_string('-hmm', os.path.join(modeldir, 'en-us/en-us'))
    config.set_string('-dict', os.path.join(modeldir, 'en-us/cmudict-en-us.dict'))
    return config

def lm():
    config = defaultconfig()
    config.set_string('-lm', os.path.join(modeldir, 'en-us/en-us.lm.bin'))
    return config

def kws(OOG):
    config = defaultconfig()
    config.set_string('-kws', os.path.join(Root, 'kws.txt'))
    config.set_float('-kws_threshold', OOG)
    return config

def transcribe(config,stream):
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

def keyword_spotting(config,stream):
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
            result.append([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
            decoder.end_utt()
            decoder.start_utt()
    return result

if __name__ == "__main__":
    results = []
    kwsOog = [1e+20,1e+19,1e+18,1e+17,1e+16,1e+15,1e+14,1e+14,1e+13,1e+12,1e+11,1e+10,1e+9,1e+8,1e+7,1e+6,1e+5,1e+4,1e+3,1e+2,1e+1]
    for i in kwsOog:
        result = keywords(i)
        results.append(result)
    for i in results:
        print(i)
