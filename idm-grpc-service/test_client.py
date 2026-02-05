import grpc

from server import idm_pb2
from server import idm_pb2_grpc


def test_login():
    channel = grpc.insecure_channel("localhost:50051")
    stub = idm_pb2_grpc.IDMServiceStub(channel)

    response = stub.Login(
        idm_pb2.LoginRequest(
            email="admin@test.com",
            password="admin123"
        )
    )

    print("TOKEN:")
    print(response.token)

    validation = stub.ValidateToken(
    idm_pb2.TokenRequest(token=response.token)
)
    print(validation)


if __name__ == "__main__":
    test_login()
