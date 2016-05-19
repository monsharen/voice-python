
__author__ = 'a.ericsson'

import os,sys
from random import randint,choice


def extraction(inputtext, dictionaryFile):
    textfile = open(inputtext, "r", encoding='utf8')
    dictfile = open(dictionaryFile, "r", encoding='utf8')
    dictionary = {word.split(" ")[0]:[i.strip() for i in word.split(" ")[1:]] for word in dictfile.readlines()}
    words = {str(i): {} for i in range(0, 15)}
    for w in " ".join(textfile.readlines()).split():
        word = w.rstrip('.,:;!?').lower()
        try:
            dictionary[word.lower()]
        except:
            next
        else:
            index = str(len(dictionary[word.lower()]))
            phones = dictionary[word.lower()]
            words[index][word] = phones
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

