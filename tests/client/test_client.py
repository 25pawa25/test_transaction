from grpc.aio import insecure_channel

from clients.grpc.proto.transaction.transaction_pb2_grpc import TransactionStub
from core.config import settings


class GRPCClient:
    def __init__(self):
        self.channel = insecure_channel(f"{settings.grpc_server.host}:{settings.grpc_server.port}")
        self.stub = TransactionStub(self.channel)
        self.auth_token = f"Bearer {settings.grpc_server.auth_token}"
        self.metadata = [("authorization", self.auth_token)]

    async def create_user_balance(self, request):
        return await self.stub.CreateUserBalance(request, metadata=self.metadata)


grpc_client = GRPCClient()
