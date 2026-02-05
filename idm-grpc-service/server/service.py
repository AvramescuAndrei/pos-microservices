import grpc

from server import idm_pb2
from server import idm_pb2_grpc
from server.db import get_connection
from server.jwt_utils import generate_token
from server.jwt_utils import decode_token
from server import blacklist


class IDMService(idm_pb2_grpc.IDMServiceServicer):

    def Login(self, request, context):
        email = request.email
        password = request.password

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, password, role FROM users WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()
        conn.close()

        if row is None:
            context.abort(
                grpc.StatusCode.UNAUTHENTICATED,
                "Invalid credentials"
            )

        user_id, db_password, role = row

        if password != db_password:
            context.abort(
                grpc.StatusCode.UNAUTHENTICATED,
                "Invalid credentials"
            )

        token = generate_token(user_id, email, role)
        return idm_pb2.LoginResponse(token=token)

    def ValidateToken(self, request, context):
        return idm_pb2.TokenValidationResponse(
            valid=False,
            user_id=0,
            role="",
            email="",
            message="Not implemented yet"
        )

    def Logout(self, request, context):
        return idm_pb2.GenericResponse(
            success=True,
            message="Not implemented yet"
        )
    
    def ValidateToken(self, request, context):
        token = request.token

        if blacklist.contains(token):
            return idm_pb2.TokenValidationResponse(
                valid=False,
                message="Token is blacklisted"
            )

        try:
            payload = decode_token(token)
        except Exception:
            blacklist.add(token)
            return idm_pb2.TokenValidationResponse(
                valid=False,
                message="Invalid or expired token"
            )

        return idm_pb2.TokenValidationResponse(
            valid=True,
            user_id=int(payload["sub"]),
            role=payload["role"],
            email=payload["email"],
            message="Token valid"
        )

    def Logout(self, request, context):
        blacklist.add(request.token)
        return idm_pb2.GenericResponse(
            success=True,
            message="Logged out"
        )

