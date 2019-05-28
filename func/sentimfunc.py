from textblob import TextBlob
# Implementing TextBlob for sentiment analysis

class sentimfunc:
    def sentimentP(text):
        try:
            return TextBlob(text).sentiment.polarity
        except:
            return "You are bad at Coding "


    def sentimentS(text):
        try:
            return TextBlob(text).sentiment.subjectivity
        except:
            return "You are bad at Coding "


    def sentimentI(text):
        try:
            return TextBlob(text).srntiment.intensity
        except:
            return "you are bad at coding"