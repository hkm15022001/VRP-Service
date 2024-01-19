from confluent_kafka import Consumer, KafkaError
import psycopg2
import json,os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from Model.postgres import connect_to_postgresql
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
from dotenv import load_dotenv
load_dotenv(dotenv_path=env_path)


def consume_messages_and_save(topic):
    dbname = 'scem_database'
    user = 'postgres'
    password = ''
    host = os.getenv("POSTGRES_HOST")
    port = '5432'

    # Kết nối đến PostgreSQL
    connection = connect_to_postgresql(dbname, user, password, host, port)

    # Tạo đối tượng cursor để thực hiện truy vấn SQL
    cursor = connection.cursor()
    print("URL Kafka:",os.getenv("KAFKA_BOOTSTRAP_SERVER"))
    consumer_conf = {
        'bootstrap.servers':  os.getenv("KAFKA_BOOTSTRAP_SERVER"),
        'group.id': 'plan-group-id',
        'auto.offset.reset': 'earliest'
    }
    
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    try:
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

            # Giả sử dữ liệu nhận được từ Kafka là chuỗi JSON
            json_data = msg.value().decode('utf-8')
            data_dict = json.loads(json_data)

            # Tạo dictionary chứa dữ liệu cho bảng order_plan
            order_plan = {
                'id': data_dict.get('id', ''),
                'receiver_address': data_dict.get('receiver_address', ''),
                'weight': data_dict.get('weight', ''),
                'note': data_dict.get('note', ''),
                'process': False
            }
            print(order_plan)
            #Thực hiện truy vấn INSERT để lưu dữ liệu vào bảng order_plan
            insert_query = """
                INSERT INTO order_plan (id, receiver_address, weight, note, process)
                VALUES (%(id)s, %(receiver_address)s, %(weight)s, %(note)s,%(process)s);
            """
            cursor.execute(insert_query, order_plan)
            connection.commit()

            print("Dữ liệu đã được lưu vào bảng 'order_plan'!")

    except KeyboardInterrupt:
        print("Consumer stopped by user.")
    finally:
        # Đóng cursor và kết nối PostgreSQL khi hoàn tất
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        consumer.close()

# Thay đổi thông tin kết nối và bootstrap servers của Kafka theo cấu hình của bạn
consume_messages_and_save('order-topic')
