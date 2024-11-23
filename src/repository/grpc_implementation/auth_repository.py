from functools import lru_cache

from google.protobuf.json_format import MessageToDict
from grpc.aio import AioRpcError, insecure_channel

from clients.grpc.proto.auth import auth_pb2
from clients.grpc.proto.auth.auth_pb2_grpc import AuthStub
from common.exceptions.grpc import GRPCConnectionException
from core.config import settings
from repository.interfaces.grpc.abc_auth_repository import AbstractAuthRepository


class GRPCAuthRepository(AbstractAuthRepository):
    def __init__(self):
        self.metadata = settings.auth_grpc.metadata

    @property
    def channel(self):
        return insecure_channel(settings.auth_grpc.url)

    @property
    def stub(self):
        return AuthStub(self.channel)

    async def check_if_user_exists(self, user_id: str) -> bool:
        """
        Check if user exists
        Args:
            user_id: id of the user
        Returns:
            bool
        """
        try:
            response = await self.stub.CheckUserExisting(
                auth_pb2.CheckUserExistingRequest(user_id=user_id), metadata=self.metadata
            )
            user = MessageToDict(response, preserving_proto_field_name=True)
            return user.get("id") is not None
        except AioRpcError:
            raise GRPCConnectionException("Error while checking user existing")


@lru_cache()
def get_grpc_auth_repository() -> AbstractAuthRepository:
    return GRPCAuthRepository()
