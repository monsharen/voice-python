__author__ = 'a.ericsson'

sentimentFile = path.join("C:/Users/a.ericsson/PycharmProjects/SpeechAnalytics", "Sentiments.csv")

def sentiment_analysis(text,sentiment):

    sentimentScore = {'neg':[],'negRF': int(0),'pos':[], 'posRF':int(0), 'total':len(text)}
    for word in text:
        try:
            sentiment[word]
        except:
            next
        else:
            if sentiment[word] > 0:
                sentimentScore['pos'].append(sentiment[word])
            else:
                sentimentScore['neg'].append(sentiment[word])
    sentimentScore['negRF']= float( len(sentimentScore['neg']) / sentimentScore['total'] )
    sentimentScore['posRF']= float( len(sentimentScore['pos']) / sentimentScore['total'] )
    return sentimentScore


def sentiment_read(fp):
    sentiment = {}
    with open(sentimentFile) as file:
        sentiment = {lines.split(',')[0].strip() : int(lines.split(',')[1].strip()) for lines in file}
    return sentiment
