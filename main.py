import multiprocessing
import subprocess

if __name__ == "__main__":
    kafka_consumer_process = multiprocessing.Process(target=subprocess.run, args=(["python", "Kafka/consumer.py"],))
    kafka_consumer_process.start()

    flask_process = multiprocessing.Process(target=subprocess.run, args=(["python", "app.py"],))
    flask_process.start()
