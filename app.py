from flask import Flask, request, jsonify,render_template
from  DeliveryPathFinder import process_optimize 
from Grpc_API.app.client import send_to_grpc
from Data.createTableDataOrder import fetch_order,clear_csv_file
import os
from pathlib import Path
from multiprocessing import Process


app = Flask("Vehicle Routing Problem")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', os.getenv("FRONTEND_SERVER"))  ## NHỚ CHỈNH LẠI 
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
# Route xử lý yêu cầu GET
@app.route('/api1/process/data', methods=['GET'])
def get_data():
    fetch_order()
    total_distance, package_list_result, truck_path,coordinates_path = process_optimize()
    print(package_list_result)
    grpc_result = send_to_grpc(package_list_result)
    print(grpc_result)
    data = {
        "total_distance": total_distance,
        "package_list_result": package_list_result,
        "truck_path": truck_path,
        "coordinates_path" : coordinates_path
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.getenv("PORT"))