from pocketsphinx.pocketsphinx import Decoder

class Config:

    languageModel = ''
    languageDictionary = ''
    audioFile = ''
    config = None
    kwsfile = ''

    def __init__(self, languagemodel, languagedictionary, audiofile, kwsfile):
        self.languageModel = languagemodel
        self.languageDictionary = languagedictionary
        self.audioFile = audiofile
        self.config = Decoder.default_config()
        self.kwsfile = kwsfile
        self.config.set_string('-logfn','nul')
    def update(self, typeParams):

        self.config.set_string('-hmm', self.languageModel)
        self.config.set_string('-dict', self.languageDictionary)


        for i in range(0, len(typeParams)):
            if list(typeParams.keys())[i] == "oog":
                self.config.set_string('-kws', self.kwsfile)
                self.config.set_float('-kws_threshold', typeParams['oog'])

            elif list(typeParams.keys())[i] == "wip":
                self.config.set_float('-wip', typeParams['wip'])

            elif list(typeParams.keys())[i] == "beam":
                self.config.set_float('-beam', typeParams['beam'])
                self.config.set_float('-pbeam', typeParams['beam'])

            elif list(typeParams.keys())[i] == "kws-delay":
                self.config.set_float('-kws_delay', typeParams['kws-delay'])

            elif list(typeParams.keys())[i] == "wbeam":
                self.config.set_float('-wbeam', typeParams['wbeam'])

            elif list(typeParams.keys())[i] == "kws":
                self.config.set_string('-kws', self.kwsfile)

            elif list(typeParams.keys())[i] == "keyphrase":
                self.config.set_string('-keyphrase', typeParams['keyphrase'])

            elif list(typeParams.keys())[i] == "lm":
                self.config.set_string('-lm', typeParams['lm'])

    def getSphinxConfig(self):
        return self.config

    def get_string(self, key):
        return self.config.get_string(key)

    def getAudioFile(self):
        return self.audioFile
