# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import word_game_pb2 as word__game__pb2


class WordGameStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateGame = channel.unary_unary(
                '/app.WordGame/CreateGame',
                request_serializer=word__game__pb2.GameRequest.SerializeToString,
                response_deserializer=word__game__pb2.GameResponse.FromString,
                )
        self.InitGameRequest = channel.unary_unary(
                '/app.WordGame/InitGameRequest',
                request_serializer=word__game__pb2.InitRequest.SerializeToString,
                response_deserializer=word__game__pb2.InitResponse.FromString,
                )
        self.SubmitWord = channel.unary_unary(
                '/app.WordGame/SubmitWord',
                request_serializer=word__game__pb2.WordSubmissionRequest.SerializeToString,
                response_deserializer=word__game__pb2.WordSubmissionResponse.FromString,
                )


class WordGameServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateGame(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InitGameRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitWord(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WordGameServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateGame': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateGame,
                    request_deserializer=word__game__pb2.GameRequest.FromString,
                    response_serializer=word__game__pb2.GameResponse.SerializeToString,
            ),
            'InitGameRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.InitGameRequest,
                    request_deserializer=word__game__pb2.InitRequest.FromString,
                    response_serializer=word__game__pb2.InitResponse.SerializeToString,
            ),
            'SubmitWord': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitWord,
                    request_deserializer=word__game__pb2.WordSubmissionRequest.FromString,
                    response_serializer=word__game__pb2.WordSubmissionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'app.WordGame', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WordGame(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateGame(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/app.WordGame/CreateGame',
            word__game__pb2.GameRequest.SerializeToString,
            word__game__pb2.GameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InitGameRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/app.WordGame/InitGameRequest',
            word__game__pb2.InitRequest.SerializeToString,
            word__game__pb2.InitResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubmitWord(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/app.WordGame/SubmitWord',
            word__game__pb2.WordSubmissionRequest.SerializeToString,
            word__game__pb2.WordSubmissionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
