import grpc
import os
from security import idm_pb2, idm_pb2_grpc

class IDMClient:
    def __init__(self, host=None, port=None):
        host = host or os.getenv("IDM_HOST", "localhost")
        port = port or int(os.getenv("IDM_PORT", "50051"))
        channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = idm_pb2_grpc.IDMServiceStub(channel)

    def validate_token(self, token: str):
        return self.stub.ValidateToken(
            idm_pb2.TokenRequest(token=token)
        )
