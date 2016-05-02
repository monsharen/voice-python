__author__ = 'a.ericsson'
import pocketsphinx
import speech_recognition as sr
import Evaluation as test
import keywordDetection as key
from os import path

WAV_FILE = "C:/Users/a.ericsson/PycharmProjects/SpeechAnalytics/Test_Set/Test.1.wav"
TEXTFILE = "C:/Users/a.ericsson/PycharmProjects/SpeechAnalytics/Test_Set/Test.1.txt"
sentimentFile = path.join("C:/Users/a.ericsson/PycharmProjects/SpeechAnalytics", "Sentiments.csv")

def main()
r = sr.Recognizer()
test = test
audio = readAudio(WAV_FILE)
sphinxText = sphinx(audio)

Rank = sentiment_analysis(sentiment_read(sphinxText),sentimentFile)



def readAudio(audiofile):
    with sr.WavFile(audiofile) as source:
        audio = r.record(source) # read the entire WAV file
    return audio

# recognize speech using Sphinx

def sphinx(input):
    try:
        r.recognize_sphinx(input)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    return r.recognize_sphinx(input)

# recognize speech using Google Speech Recognition

def google(input):

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        r.recognize_google(input)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return r.recognize_google(input)

# recognize speech using Wit.ai

def wit_AI(input):

    WIT_AI_KEY = "YK5SWAMMGH2A4WIOH7TMGWJ3U4DBVYNQ" # Wit.ai keys are 32-character uppercase alphanumeric strings

    try:
        print("Wit.ai results: " + r.recognize_wit(input, key=WIT_AI_KEY))
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))

# recognize speech using IBM Speech to Text

def ibm(input):

    IBM_USERNAME = "INSERT IBM SPEECH TO TEXT USERNAME HERE" # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    IBM_PASSWORD = "INSERT IBM SPEECH TO TEXT PASSWORD HERE" # IBM Speech to Text passwords are mixed-case alphanumeric strings

    try:
        print("IBM Speech to Text thinks you said " + r.recognize_ibm(input, username=IBM_USERNAME, password=IBM_PASSWORD))
    except sr.UnknownValueError:
        print("IBM Speech to Text could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from IBM Speech to Text service; {0}".format(e))

# recognize speech using api.ai Speech to Text
# Note: Use the developer access token for managing entities and intents, and use the client access token for making queries.

def apiAi(input):

    API_AI_CLIENT_ACCESS_TOKEN = "892b361f4dd14c6da7d9c202382563fe"  # api.ai access tokens are 32-character lowercase alphanumeric strings
    API_AI_SUBSCRIPTION_KEY = "786d69dd-d59f-4a74-a618-120fbb46e62c"  # api.ai subscription_keys are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX

    try:
        print("api.ai Speech to Text Results :" + r.recognize_api(input, username=API_AI_CLIENT_ACCESS_TOKEN, password=API_AI_SUBSCRIPTION_KEY))
    except sr.UnknownValueError:
        print("api.ai Speech to Text could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from api.ai Speech to Text service; {0}".format(e))



