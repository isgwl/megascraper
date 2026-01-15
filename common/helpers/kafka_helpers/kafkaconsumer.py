from confluent_kafka import Consumer,KafkaException

class KafkaConsumer:
    def __init__(self,handleMsg):
        conf = {
            "bootstrap.servers": "localhost:29092",
            "group.id": "foo",
            "enable.auto.commit": "false",
            "auto.offset.reset": "earliest",
        }
        self.consumer = Consumer(conf)
        self.handleMsg = handleMsg

    def consumeLoop(self,topics):
        try:
            self.consumer.subscribe(topics)

            running = True
            while running:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                elif msg.error():
                    raise KafkaException(msg.error())
                else:
                    # Do something with the message
                    self.handleMsg(msg)
                    
                    #commit value
                    self.consumer.commit(message=msg,asynchronous=False)
                    
        except Exception as e:
            print(f"Fatal error in consumeLoop: {e}")
        finally:
            self.consumer.close()
            