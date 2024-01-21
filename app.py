from flask import Flask, request, jsonify
from  DeliveryPathFinder import process_optimize 
from Event.producer import produce_message
from Model.postgres import connect_to_postgresql
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask("Vehicle Routing Problem")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', os.getenv("*"))  ## NHỚ CHỈNH LẠI 
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
# Route xử lý yêu cầu GET
@app.route('/scem-ship/api1/process/data', methods=['GET'])
def get_data():
    total_distance, package_list_result, truck_path,coordinates_path = process_optimize(connection)
    print("Package list result:",package_list_result)
    #if use grpc
    # response = send_to_grpc(package_list_result) 

    #if use kafka
    result = produce_message(package_list_result)
    data = {
        "total_distance": total_distance,
        "package_list_result": package_list_result,
        "truck_path": truck_path,
        "coordinates_path" : coordinates_path
    }

    if(result==1):
        update_query = "UPDATE order_plan SET process = true;"
        cursor = connection.cursor()
        cursor.execute(update_query)
        connection.commit()

    return jsonify(data)


if __name__ == "__main__":
    dbname = 'scem_database'
    user = 'postgres'
    password = ''
    host = os.getenv("POSTGRES_HOST")
    port = '5432'

# Kết nối đến PostgreSQL
    connection = connect_to_postgresql(dbname, user, password, host, port)
    port = os.getenv("PORT")
    print("Start in port:", port)
    app.run(debug=True, host='0.0.0.0', port=int(port))
