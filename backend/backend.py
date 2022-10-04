from twitter_producer import TwitterClient, tweets_to_data_frame
from flask import Flask,render_template,request
import requests
from kafka import KafkaProducer
import json,os,datetime
import folium
from geopy.geocoders import Nominatim
app = Flask(__name__)
base='http://frontend:5000/api/v1/data'

# Kafka settings
KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL") if os.environ.get(
    "KAFKA_BROKER_URL") else 'localhost:9092'
TOPIC_NAME = os.environ.get("TOPIC_NAME") if os.environ.get(
    "TOPIC_NAME") else 'from_twitter'


producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda x: json.dumps(x).encode('ascii'),
        api_version=(0, 10, 1)
    )


def getFromAPI():
    try:
        
        uresponse=requests.get(base)
        response=json.loads(uresponse.text)
        data=response["data"]
    except requests.ConnectionError:
        return "Connection Error"
    return data

def getTweet():
    data=getFromAPI()
    hashtag_list=data["hashtag_list"]
    numero_di_tweet= data["numero_di_tweet"]
    #Uso l apposito metodo per recuperare l api per poter effettuare le ricerche dei tweet con il cursore
    api = TwitterClient().get_twitter_client_api()
    for tag in hashtag_list:
        tweets = api.search(tag, lang = 'it', result_type='mixed', count =numero_di_tweet)
        df=tweets_to_data_frame(tweets)
        print('dati serializzati')
        for tweet in tweets:
            producer.send('fromTwitter',value={'text':tweet.text,
                                               'date':tweet.created_at.isoformat(),
                                               'position':tweet.user.location,
                                               'like':tweet.favorite_count
                                               }
                        )
       
    producer.flush()
    producer.close() 
    return df 

@app.route('/',methods=['GET'])
def filter_data():
    if request.method=='GET':
        data=getFromAPI()
        df=getTweet()
    return render_template('index.html',data=data,tables=[df.to_html(classes='data', header="true")])



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=2000,  debug=True)



