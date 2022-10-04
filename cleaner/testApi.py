from flask_restful import Api, Resource 
from flask import Flask
from kafka import KafkaConsumer
import re,string ,json
import numpy as np
import pandas as pd
from textblob import TextBlob
app = Flask(__name__)
my_api=Api(app)
basePath='/api/v1'


def give_emoji_free_text(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    clean_text=emoji_pattern.sub(r'',text)
    return clean_text

#metodo che pulisce il tweet da link caratteri speciali
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

#rimuovere punteggiatura
#string.punctuation
#'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
def remove_punct(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text

def stemming(text):
    ita_stemmer = nltk.stem.snowball.ItalianStemmer()
    text = [ita_stemmer.stem(word) for word in text]
    return text

def applyClean(lista):
    print('sono qui')
    for item in lista:
        noemoji=give_emoji_free_text(item['text'])#elimino le emiji
        nolink=clean_tweet(noemoji)#elimino link e caratteri speciali
        nopunct=remove_punct(nolink)#rimuovo punteggiatura
        item['text']=nopunct
    return lista
#metodo che ti serve per avere i dati del tweet sotto forma di data frame o anche grande tabella
def tweets_to_data_frame(tweets):
        df = pd.DataFrame(data=[tweet['text'] for tweet in tweets], columns=['tweets'])
        df['len'] = np.array([len(tweet['text']) for tweet in tweets])
        df['date'] = np.array([tweet['date'] for tweet in tweets])
        df['position'] = np.array([tweet['position'] for tweet in tweets])
        df['likes'] = np.array([tweet['like'] for tweet in tweets])
        df['sentiment'] = np.array([analyze_sentiment(tweet['text']) for tweet in tweets])
        return df


#funzione che ritorna il sentimento
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 1
    else:
        return 0


class start(Resource):
    def get(self):
        print("Tweets Collected....")
        consumer = KafkaConsumer('fromTwitter', auto_offset_reset='earliest',
                            bootstrap_servers=['broker:9092'], 
                            value_deserializer=lambda m: json.loads(m.decode('ascii')),
                            api_version=(0, 10,1),
                            consumer_timeout_ms=1000)

        print('sono qui')
        tweets = []
        #consumer ora contiene tutto il testo che mi serve, devo leggerlo
        for msg in consumer:
            print('messaggio in arrivo....')
            tweets.append(msg.value)
        consumer.close()
        print('ecco la lista dei messaggi arrivati:')
        if len(tweets)>=1:
            for text in tweets:
                print(text)
            print(' ')
            print('ripulisco i tweet')
            return tweets_to_data_frame(applyClean(tweets)).to_json(),200
        return None,404


my_api.add_resource(start,f'{basePath}/data')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,  debug=True)
