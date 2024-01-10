import grpc
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..\generative_code"))
import calculator_pb2
import calculator_pb2_grpc
from concurrent import futures
class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        result = request.a + request.b
        return calculator_pb2.AddResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        CalculatorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
if __name__ == '__main__':
    serve()