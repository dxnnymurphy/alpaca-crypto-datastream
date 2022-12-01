# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import service_cryptodatastream_pb2 as service__cryptodatastream__pb2


class ServiceCryptoDataStreamStub(object):
    """=========================================================================================================================
    OpenAPI/v2 - Swagger - END

    For more information, please refer to:
    1) https://blog.bullgare.com/2020/07/complete-list-of-swagger-options-to-protobuf-file/
    2) https://github.com/grpc-ecosystem/grpc-gateway/blob/master/examples/internal/proto/examplepb/a_bit_of_everything.proto
    =========================================================================================================================

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateTask = channel.unary_unary(
                '/cryptodatastream.grpc.ServiceCryptoDataStream/CreateTask',
                request_serializer=service__cryptodatastream__pb2.Task.SerializeToString,
                response_deserializer=service__cryptodatastream__pb2.Task.FromString,
                )
        self.DeleteTask = channel.unary_unary(
                '/cryptodatastream.grpc.ServiceCryptoDataStream/DeleteTask',
                request_serializer=service__cryptodatastream__pb2.String.SerializeToString,
                response_deserializer=service__cryptodatastream__pb2.Task.FromString,
                )
        self.ReadTask = channel.unary_unary(
                '/cryptodatastream.grpc.ServiceCryptoDataStream/ReadTask',
                request_serializer=service__cryptodatastream__pb2.String.SerializeToString,
                response_deserializer=service__cryptodatastream__pb2.Task.FromString,
                )
        self.ListTasks = channel.unary_unary(
                '/cryptodatastream.grpc.ServiceCryptoDataStream/ListTasks',
                request_serializer=service__cryptodatastream__pb2.Void.SerializeToString,
                response_deserializer=service__cryptodatastream__pb2.Tasks.FromString,
                )


class ServiceCryptoDataStreamServicer(object):
    """=========================================================================================================================
    OpenAPI/v2 - Swagger - END

    For more information, please refer to:
    1) https://blog.bullgare.com/2020/07/complete-list-of-swagger-options-to-protobuf-file/
    2) https://github.com/grpc-ecosystem/grpc-gateway/blob/master/examples/internal/proto/examplepb/a_bit_of_everything.proto
    =========================================================================================================================

    """

    def CreateTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReadTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListTasks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServiceCryptoDataStreamServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateTask': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateTask,
                    request_deserializer=service__cryptodatastream__pb2.Task.FromString,
                    response_serializer=service__cryptodatastream__pb2.Task.SerializeToString,
            ),
            'DeleteTask': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteTask,
                    request_deserializer=service__cryptodatastream__pb2.String.FromString,
                    response_serializer=service__cryptodatastream__pb2.Task.SerializeToString,
            ),
            'ReadTask': grpc.unary_unary_rpc_method_handler(
                    servicer.ReadTask,
                    request_deserializer=service__cryptodatastream__pb2.String.FromString,
                    response_serializer=service__cryptodatastream__pb2.Task.SerializeToString,
            ),
            'ListTasks': grpc.unary_unary_rpc_method_handler(
                    servicer.ListTasks,
                    request_deserializer=service__cryptodatastream__pb2.Void.FromString,
                    response_serializer=service__cryptodatastream__pb2.Tasks.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cryptodatastream.grpc.ServiceCryptoDataStream', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ServiceCryptoDataStream(object):
    """=========================================================================================================================
    OpenAPI/v2 - Swagger - END

    For more information, please refer to:
    1) https://blog.bullgare.com/2020/07/complete-list-of-swagger-options-to-protobuf-file/
    2) https://github.com/grpc-ecosystem/grpc-gateway/blob/master/examples/internal/proto/examplepb/a_bit_of_everything.proto
    =========================================================================================================================

    """

    @staticmethod
    def CreateTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cryptodatastream.grpc.ServiceCryptoDataStream/CreateTask',
            service__cryptodatastream__pb2.Task.SerializeToString,
            service__cryptodatastream__pb2.Task.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cryptodatastream.grpc.ServiceCryptoDataStream/DeleteTask',
            service__cryptodatastream__pb2.String.SerializeToString,
            service__cryptodatastream__pb2.Task.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReadTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cryptodatastream.grpc.ServiceCryptoDataStream/ReadTask',
            service__cryptodatastream__pb2.String.SerializeToString,
            service__cryptodatastream__pb2.Task.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListTasks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cryptodatastream.grpc.ServiceCryptoDataStream/ListTasks',
            service__cryptodatastream__pb2.Void.SerializeToString,
            service__cryptodatastream__pb2.Tasks.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)