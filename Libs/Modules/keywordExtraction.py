
__author__ = 'a.ericsson'

import os,sys
from random import randint,choice
from collections import defaultdict

def make_dict():
    return defaultdict(make_dict)

def extraction(inputtext, dictionaryFile,wordspeakerFreq=None):

    textfile = open(inputtext, "r", encoding='utf8')
    dictfile = open(dictionaryFile, "r", encoding='utf8')
    dictionary = {word.split(" ")[0]:[i.strip() for i in word.split(" ")[1:]] for word in dictfile.readlines()}
    words = defaultdict(make_dict)
    wordArray = [word.rstrip('.,:;!?').lower() for word in " ".join(textfile.readlines()).split()]
    for word in wordArray:
        if dictionary.get(word) != None:
            phoneIndex = str(len(dictionary[word.lower()]))
            phones = dictionary[word.lower()]
            words[phoneIndex][word]= {'freq':wordArray.count(word),'speakerFreq':wordspeakerFreq[word]}
    return words

def randomSampling(words, numwords, phones=[2,4,6,8],kws="kwsfile.txt"):
    kwsfile = open(kws, 'w', encoding='utf8')
    keywords = []
    for nphone in phones:
        for word in range(0, numwords):
            keyword = choice(list(words[str(nphone)].keys()))
            keywords.append(keyword)
            words[str(nphone)].pop(keyword)
            kwsfile.write(keyword+"\n")
    kwsfile.close()
    return keywords

def targetSampling(words,phones=[5,6],kws="kwsfile.txt"):
    kwsfile = open(kws, 'w', encoding='utf8')
    keywords = []

    for nphone in phones:
        for word in words[str(nphone)]:
            freq = words[str(nphone)][word]['freq']
            speakerFreq = words[str(nphone)][word]['speakerFreq']
            print(words[str(nphone)][word])
            if freq >= 6 and  speakerFreq >= 6:
                keywords.append(word)
                kwsfile.write(word + "\n")

    kwsfile.close()
    return keywords

def reference(keyhash=None,inputtext="",refsfile=""):
    textfile = open(inputtext, "r", encoding='utf8')
    outputfile = open(refsfile, 'w', encoding='utf8')
    refs = []
    for w in " ".join(textfile.readlines()).split():
        word = w.rstrip('.,:;!?').lower()
        if word in keyhash:
            refs.append(word)
            outputfile.write(word + "\n")
    outputfile.close()
    return refs

