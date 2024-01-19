import psycopg2
from psycopg2 import sql

def connect_to_postgresql(dbname, user, password, host, port):
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Kết nối đến PostgreSQL thành công!")
        return connection
    except psycopg2.Error as e:
        print(f"Lỗi kết nối đến cơ sở dữ liệu: {e}")
        return None
def create_order_plan_table(connection):
    try:
        # Tạo đối tượng cursor để thực thi các truy vấn SQL
        cursor = connection.cursor()

        # Truy vấn SQL để tạo bảng order_plan
        create_table_query = """
            CREATE TABLE IF NOT EXISTS order_plan (
                id SERIAL PRIMARY KEY,
                receiver_address VARCHAR(255) NOT NULL,
                weight SERIAL NOT NULL,
                note TEXT,
                process BOOLEAN
            );
        """

        # Thực thi truy vấn để tạo bảng
        cursor.execute(create_table_query)
        connection.commit()

        print("Bảng 'order_plan' đã được tạo thành công!")

    except psycopg2.Error as e:
        print(f"Lỗi khi tạo bảng: {e}")

    finally:
        # Đóng cursor
        if cursor:
            cursor.close()

# if __name__ == '__main__':
#     connection = connect_to_postgresql("scem_database","postgres","","localhost",5432)
#     create_order_plan_table(connection)