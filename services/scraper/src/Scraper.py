import sys
import json
import os
import kafka_helpers
from kafka_helpers.kafkaproducer import KafkaProducer
from kafka_helpers.kafkaconsumer import KafkaConsumer
from seleniumbase import SB
from jsonschema import validate, ValidationError


from tasks.amazon_search_results import amazon_search_results


class Scraper:
    def __init__(self, topics):
        # initialize kafka consumer and producer
        self.consumer = KafkaConsumer(self.handleMsg)
        self.producer = KafkaProducer()
        self.topics = topics

    def __enter__(self):
        # Create the SB context manager
        self._sb_cm = SB(
            uc=True,
            headed=True,
            ad_block=True,
            page_load_strategy="eager",
            skip_js_waits=True,
        )
        # Enter it and store the real sb object
        self.sb = self._sb_cm.__enter__()
        self.sb.activate_cdp_mode()
        return self

    def __exit__(self, exc_type, exc, tb):
        # Propagate errors to SB's __exit__
        if self._sb_cm:
            self._sb_cm.__exit__(exc_type, exc, tb)

        print("Scraper service exited.")

    def handleMsg(self, msg):
        try:
            # decode message
            valStr = msg.value().decode("utf-8")

            # convert to json object
            valJson = json.loads(valStr)

            # validate against new page schema
            validate(instance=valJson, schema=kafka_helpers.targetPageScehma)

            # do action
            self.doTask(valJson.get("task"), valJson.get("url"))

        except ValidationError as ve:
            print(f"JSON schema validation failed: {ve}")
        except Exception as e:
            print(f"Failed to handle message:\n\t {e}")

    def doTask(self, task, url):
        print(f"doTask key: {task}")
        print(f"doTask url: {url}")

        # run task from message
        try:
            resultData = None

            if task == "amazon_search_results":
                resultData = amazon_search_results(self.sb, url)

            # send data to topic
            if resultData != None:
                validate(instance=resultData, schema=self.scrapeResultSchema)
                self.producer.produce_message(
                    "scrape_results", "my key.", json.dumps(resultData)
                )

        except ValidationError as ve:
            print(f"JSON schema validation failed: {ve}")
        except Exception as e:
            print(f"Task {task} failed: {e}")

    def start(self):
        # begin processing events from topics
        self.consumer.consumeLoop(self.topics)


if __name__ == "__main__":
    with Scraper(["target_pages"]) as d:
        d.start()