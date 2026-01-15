from confluent_kafka import Producer
import socket

class KafkaProducer:    
    def __init__(self):
        conf = {"bootstrap.servers": "localhost:29092", "client.id": socket.gethostname()}
        self.producer = Producer(conf)
        
    def produce_message(self,topic,key,value):
        self.producer.produce(topic, key=key, value=value)
        self.producer.flush()
        