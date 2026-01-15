import sys
import json
from kafka_helpers.kafkaproducer import KafkaProducer

msgs = [
    {"url": "amazon.com", "task": "amazon_search_results"},
]

prod = KafkaProducer()

for val in msgs:
    prod.produce_message("target_pages", val.get("task"), json.dumps(val))
