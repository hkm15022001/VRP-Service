import grpc
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..\generative_code"))
import longship_pb2
import longship_pb2_grpc

def send_to_grpc(package_list):
    package_list_result = longship_pb2.PackageListResult()
    for key, values in package_list.items():
        package_items = package_list_result.package_list_result[key]
        # Convert integers to strings
        str_values = [str(value) for value in values]
        # Extend the 'id' field with string values
        package_items.id.extend(str_values)

    with grpc.insecure_channel('localhost:50052') as channel:
        stub = longship_pb2_grpc.LongShipStub(channel)
        response = stub.CreateLongShipFromVRP(package_list_result)
        print("Result:", response.ok, response.response)
    return response
if __name__ == '__main__':
    send_to_grpc()