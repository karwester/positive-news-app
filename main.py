from flask import Flask
from flask import render_template
import feedparser
import pandas as pd
from flair.models import TextClassifier
from flair.data import Sentence
from hugchat import hugchat

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"



@app.route("/rssFeed")

def runApp():
    df = getRssFeed().head(5)

    df['flairSentimentTitle'] = df.title.map(lambda x : text_sentiment_flair(x))


#print(df.head())
#do not change npositive headings
    #df["posTitle"] = df.apply(lambda row: row["title"] if row["flairSentimentTitle"][0] == "POSITIVE" else getPositiveHeading(row["title"]), axis=1)
#change positive headings
    df["posTitle"] = df.apply(lambda row: getPositiveHeading(row["title"]), axis=1)
    posDf = df[["published", "posTitle"]]
    return posDf.to_html(header="true", table_id="table")

def getRssFeed():


    feed = "https://www.theguardian.com/uk/rss"
    newsFeed = feedparser.parse(feed)
    #entry = newsFeed.entries[1]

    #print (entry.keys())
    #noOfEntries = len(newsFeed.entries)
    #print ('Number of RSS posts :', len(newsFeed.entries))

    column = ['published', 'title', 'summary']
    rows_list = []

    for entry in newsFeed.entries:
        row = [entry.published, entry.title, entry.summary]
        rows_list.append(dict(zip(column, row)))

    #df = pd.DataFrame(rows_list, columns=['published', 'title', 'summary'])
    df = pd.DataFrame(rows_list, columns=['published', 'title'])
    return df
    #return df.head().to_html(header="true", table_id="table")
    #return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

def text_sentiment_flair(text):
    classifier = TextClassifier.load('en-sentiment')
    sentence = Sentence(text)
    classifier.predict(sentence)
    sent = sentence.labels[0].value
    conf =sentence.labels[0].score
    return sent, conf

def getPositiveHeading(heading):
    chatbot = hugchat.ChatBot(cookie_path = r'C:\Users\karol\OneDrive\Desktop\cookies.json')
    return(chatbot.chat("Rewrite this heading to sound very positive, keeping the original spelling of names and places. Keep it short and output ONLY the changed heading. Here is the heading to change:" + heading))
    








if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)