import sys
import json
import os
import psycopg
import kafka_helpers
from kafka_helpers.kafkaproducer import KafkaProducer
from kafka_helpers.kafkaconsumer import KafkaConsumer

from jsonschema import validate, ValidationError
from postgres_helpers.postgres_connector import getDb

class Coordinator:
    def __init__(self, topics):
        # initialize kafka consumer and producer
        self.consumer = KafkaConsumer(self.handleMsg)
        self.producer = KafkaProducer()
        self.topics = topics
        self.dbPool = getDb()

    
    def handleMsg(self, msg):
        try:
            # decode message
            valStr = msg.value().decode("utf-8")

            # convert to json object
            valJson = json.loads(valStr)

            # validate against new page schema
            validate(instance=valJson, schema=kafka_helpers.scrapeResultSchema)

            # asynchronously update data records in db
            
            
            # Check new links against Redis cache
            
            # Produce new target urls
            
            print(valJson)

        except ValidationError as ve:
            print(f"JSON schema validation failed: {ve}")
        except Exception as e:
            print(f"Failed to handle message:\n\t {e}")

    def start(self):
        # begin processing events from topics
        self.consumer.consumeLoop(self.topics)

if __name__ == "__main__":
    Coordinator(["scrape_results"]).start()
        