from confluent_kafka import Producer
import os,json
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
from dotenv import load_dotenv
load_dotenv(dotenv_path=env_path)

def delivery_report(err, msg, success_flag):
    if err is not None:
        print(f'Gửi tin nhắn bị lỗi: {err}')
        success_flag[0] = 0
    else:
        print(f'Tin nhắn gửi thành công: {msg.value().decode("utf-8")}')
        success_flag[0] = 1
def produce_message(message):
    conf = {
        'bootstrap.servers':  os.getenv("KAFKA_BOOTSTRAP_SERVER"),
        'client.id': 'planservice-producer'
    }

    # Tạo producer
    producer = Producer(conf)

    topic = 'longship-topic' 
    


    # Serialize the dictionary to a JSON string
    serialized_message = json.dumps(message)

    # Convert the JSON string to bytes
    message_bytes = bytes(serialized_message, 'utf-8')

    success_flag = [0]
    producer.produce(topic, value=message_bytes, callback=lambda err, msg: delivery_report(err, msg, success_flag))

    # Đảm bảo tất cả các tin nhắn đã được gửi
    producer.flush()
    return success_flag[0]

if __name__ == "__main__":
    message = {222: [7538583, 4861493, 7942605, 10945942, 11205915, 5918515, 4636807, 8929782, 10670693, 2746423, 6864349, 3983349, 2077359, 10527620, 9114793, 7345328, 610617, 2766269, 6321499, 2442555, 4581062], 1338750250: [722054, 11329843, 5635662, 10855918, 6577334, 780222, 8059194, 10439478, 6688361, 2522988, 10718357, 1214262, 2698261], 567783907: 
[7153510, 10642026, 5948446, 4241861, 4202449, 196746, 10344019, 8408179, 322172, 6053281, 3271882, 9671775, 2838316, 8778909, 6603716, 3050929, 9277948, 1592171, 5926937, 9746236, 692516, 10587575, 7152995, 578944, 4464197, 11082207, 7840670, 11475047, 6358871, 2374472, 6807336], 2130855613: [5205147, 10700086, 2230790, 860768, 2971605, 8494650, 8427547, 7181201, 1523256, 7259732, 2878179, 4067340, 2155146, 7530520, 5016559]}
    print(produce_message(message))