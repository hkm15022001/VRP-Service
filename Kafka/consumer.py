from confluent_kafka import Consumer, KafkaError
import os
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
from dotenv import load_dotenv
load_dotenv(dotenv_path=env_path)
consumer = None

def connect_consumer(conf):
    global consumer
    consumer = Consumer(conf)
    return consumer

def close_consumer():
    if consumer is not None:
        consumer.close()

def consume_messages(topic):
    if consumer is None:
        print("Consumer is not connected.")
        return

    consumer.subscribe([topic])

    running = True
    while running:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Consumer error: {msg.error()}")
                break

        print(f"Received message: {msg.value().decode('utf-8')}")

def start_kafka_consumer():
    print("Bootstrap server: ",os.getenv("KAFKA_BOOTSTRAP_SERVER"))
    conf = {'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVER"), 'group.id': 'python-consumer-group', 'auto.offset.reset': 'earliest'}
    topic = 'order-topic'
    connect_consumer(conf)
    consume_messages(topic)
    close_consumer()

if __name__ == "__main__":
    start_kafka_consumer()
