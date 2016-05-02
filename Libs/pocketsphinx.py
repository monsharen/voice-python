__author__ = 'a.ericsson'

import sys, os
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

Root = "C:\\Users\\a.ericsson\\PycharmProjects\\SpeechAnalytics\\Voice_Python\\Libs"
os.chdir(Root)
modeldir = "..\\Model"
datadir = "..\\Datasets\\TestSet"

def speechanalytics(type,OOG=1e+1):
    stream = stream = open(os.path.join(datadir, "Test.12.wav"), "rb")
    config = detectionconfig(type,OOG)

    if type == "kws" or "keyphrase":
        result = keyword_spotting(config,stream)

    elif type == "lm":
        result = transcribe(config,stream)

    return  result

# Create a decoder with certain model
def defaultconfig():
    config = Decoder.default_config()
    config.set_string('-hmm', os.path.join(modeldir, 'en-us/en-us'))
    config.set_string('-dict', os.path.join(modeldir, 'en-us/cmudict-en-us.dict'))
    return config

def detectionconfig(type,OOG):
    config = defaultconfig()

    if type == "kws":
        config.set_string('-kws', os.path.join(Root, 'kws.txt'))
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
    kwsOog = [1e-50,1e-40,1e-30,1e-20,1e-10,1e+1,1e+10,1e+20,1e+30,1e+30,1e+40,1e+50]

    for i in kwsOog:
        result = speechanalytics("kws",i)
        results.append(result)
    for i in results:
        print(i)
