__author__ = 'a.ericsson'

os.path.join(modeldir, 'en-us/en-us'
os.path.join(modeldir, 'en-us/cmudict-en-us.dict')


class config()
def createConfig(self, languagemodel, languagedictionary, audiofile, params={} ):

    config = Decoder.default_config()
    config.set_string('-hmm', languagemodel)
    config.set_string('-dict', languagedictionary)
    stream = open(audiofile, "rb")

    for i in range(0,len(params)):
        if list(params.keys())[i] == "oog":
            config.set_float('-kws_threshold', params['oog'])

        elif list(params.keys())[i] == "wip":
            config.set_float('-wip', params['wip'])

        elif list(params.keys())[i] == "beam":
            config.set_float('-beam', params['beam'])
            config.set_float('-pbeam', params['beam'])

        elif list(params.keys())[i] == "kws-delay":
            config.set_float('-kws-delay', params['kws-delay'])

        elif list(params.keys())[i] == "wbeam":
            config.set_float('-wbeam', params['wbeam'])

        elif list(params.keys())[i] == "kws":
            config.set_string('-kws', params['kws'])

        elif list(params.keys())[i] == "kws":
            config.set_string('-keyphrase', params['kws'])

        elif list(params.keys())[i] == "lm":
            config.set_string('-lm',params['lm'])

    return config