from kafka import KafkaConsumer
import json
import time

if __name__ == '__main__':
    
    time.sleep(30)
    print("Tweets Collected....")
    consumer = KafkaConsumer('fromTwitter', auto_offset_reset='earliest',
                             bootstrap_servers=['broker:9092'], 
                             value_deserializer=lambda m: json.loads(m.decode('ascii')),
                             api_version=(0, 10,1),
                              consumer_timeout_ms=1000)
    print('sono qui')
    Lista = []
    #consumer ora contiene tutto il testo che mi serve, devo leggerlo
    for msg in consumer:
        print('messaggio in arrivo....')
        Lista.append(msg.value)
    print('ecco la lista dei messaggi arrivati:')
    for text in Lista:
        print(text)

    print('fine')