# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import word_game2_pb2 as word__game2__pb2


class WordGameStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateGame = channel.unary_unary(
                '/app.WordGame/CreateGame',
                request_serializer=word__game2__pb2.CreateGameRequest.SerializeToString,
                response_deserializer=word__game2__pb2.CreateGameResponse.FromString,
                )
        self.JoinGame = channel.unary_unary(
                '/app.WordGame/JoinGame',
                request_serializer=word__game2__pb2.JoinGameRequest.SerializeToString,
                response_deserializer=word__game2__pb2.JoinGameResponse.FromString,
                )
        self.InitGame = channel.unary_unary(
                '/app.WordGame/InitGame',
                request_serializer=word__game2__pb2.InitGameRequest.SerializeToString,
                response_deserializer=word__game2__pb2.InitGameResponse.FromString,
                )
        self.GetPangram = channel.unary_unary(
                '/app.WordGame/GetPangram',
                request_serializer=word__game2__pb2.GetPangramRequest.SerializeToString,
                response_deserializer=word__game2__pb2.GetPangramResponse.FromString,
                )
        self.SubmitWord = channel.unary_unary(
                '/app.WordGame/SubmitWord',
                request_serializer=word__game2__pb2.WordSubmissionRequest.SerializeToString,
                response_deserializer=word__game2__pb2.WordSubmissionResponse.FromString,
                )
        self.QueryGameStatus = channel.unary_unary(
                '/app.WordGame/QueryGameStatus',
                request_serializer=word__game2__pb2.GameStatusRequest.SerializeToString,
                response_deserializer=word__game2__pb2.GameStatusResponse.FromString,
                )
        self.EndGame = channel.unary_unary(
                '/app.WordGame/EndGame',
                request_serializer=word__game2__pb2.EndGameRequest.SerializeToString,
                response_deserializer=word__game2__pb2.EndGameResponse.FromString,
                )


class WordGameServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateGame(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def JoinGame(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InitGame(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPangram(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitWord(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryGameStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EndGame(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WordGameServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateGame': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateGame,
                    request_deserializer=word__game2__pb2.CreateGameRequest.FromString,
                    response_serializer=word__game2__pb2.CreateGameResponse.SerializeToString,
            ),
            'JoinGame': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinGame,
                    request_deserializer=word__game2__pb2.JoinGameRequest.FromString,
                    response_serializer=word__game2__pb2.JoinGameResponse.SerializeToString,
            ),
            'InitGame': grpc.unary_unary_rpc_method_handler(
                    servicer.InitGame,
                    request_deserializer=word__game2__pb2.InitGameRequest.FromString,
                    response_serializer=word__game2__pb2.InitGameResponse.SerializeToString,
            ),
            'GetPangram': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPangram,
                    request_deserializer=word__game2__pb2.GetPangramRequest.FromString,
                    response_serializer=word__game2__pb2.GetPangramResponse.SerializeToString,
            ),
            'SubmitWord': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitWord,
                    request_deserializer=word__game2__pb2.WordSubmissionRequest.FromString,
                    response_serializer=word__game2__pb2.WordSubmissionResponse.SerializeToString,
            ),
            'QueryGameStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.QueryGameStatus,
                    request_deserializer=word__game2__pb2.GameStatusRequest.FromString,
                    response_serializer=word__game2__pb2.GameStatusResponse.SerializeToString,
            ),
            'EndGame': grpc.unary_unary_rpc_method_handler(
                    servicer.EndGame,
                    request_deserializer=word__game2__pb2.EndGameRequest.FromString,
                    response_serializer=word__game2__pb2.EndGameResponse.SerializeToString,
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
            word__game2__pb2.CreateGameRequest.SerializeToString,
            word__game2__pb2.CreateGameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def JoinGame(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/app.WordGame/JoinGame',
            word__game2__pb2.JoinGameRequest.SerializeToString,
            word__game2__pb2.JoinGameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InitGame(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/app.WordGame/InitGame',
            word__game2__pb2.InitGameRequest.SerializeToString,
            word__game2__pb2.InitGameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPangram(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/app.WordGame/GetPangram',
            word__game2__pb2.GetPangramRequest.SerializeToString,
            word__game2__pb2.GetPangramResponse.FromString,
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
            word__game2__pb2.WordSubmissionRequest.SerializeToString,
            word__game2__pb2.WordSubmissionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryGameStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/app.WordGame/QueryGameStatus',
            word__game2__pb2.GameStatusRequest.SerializeToString,
            word__game2__pb2.GameStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EndGame(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/app.WordGame/EndGame',
            word__game2__pb2.EndGameRequest.SerializeToString,
            word__game2__pb2.EndGameResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
