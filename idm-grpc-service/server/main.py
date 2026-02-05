from concurrent import futures
import grpc

from server import idm_pb2_grpc
from server.service import IDMService


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    idm_pb2_grpc.add_IDMServiceServicer_to_server(IDMService(), server)

    server.add_insecure_port("[::]:50051")
    server.start()

    print("IDM gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
