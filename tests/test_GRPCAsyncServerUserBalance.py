import asyncio

from google.protobuf.json_format import MessageToDict

from tests.client.test_client import grpc_client
from tests.client.test_request import user_request


def test_GRPCAsyncServerUserBalance():
    result = asyncio.get_event_loop().run_until_complete(grpc_client.create_user_balance(user_request))
    assert isinstance(result, object)
    print(f"Result: {MessageToDict(result)}")
