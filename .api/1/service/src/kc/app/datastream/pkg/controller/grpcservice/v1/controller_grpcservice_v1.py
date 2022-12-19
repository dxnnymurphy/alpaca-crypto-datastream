from .. import ControllerGrpcService

from concurrent import futures
import grpc
import copy
from grpc_reflection.v1alpha import reflection
from py_grpc_prometheus.prometheus_server_interceptor import PromServerInterceptor
import threading

from kc.app.core.annotation import Logger, Singleton
from kc.app.datastream.pkg.configuration import Configuration, ConfigurationFactory
from kc.app.datastream.pkg.service import Service, ServiceFactory
import kc.app.datastream.pkg.model.datastream.v3.service_datastream_pb2 as model
import kc.app.datastream.pkg.model.datastream.v3.service_datastream_pb2_grpc as grpcservice


@Singleton
@Logger
class ControllerGrpcServiceV1(ControllerGrpcService,
                              grpcservice.ServiceDataStreamServicer):
    __configuration: Configuration = None
    __service: Service = None

    __server: grpc.Server = None
    __locker4server: threading.Lock = None

    def __init__(self):
        self.__locker4server = threading.Lock()
        self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                                    interceptors=(PromServerInterceptor(enable_handling_time_histogram=True),))
        grpcservice.add_ServiceDataStreamServicer_to_server(self, self.__server)
        reflection.enable_server_reflection((model.DESCRIPTOR.services_by_name['ServiceDataStream'].full_name,
                                             reflection.SERVICE_NAME), 
                                            self.__server)

    def GetVersion(self) -> str:
        return "v1"

    def Start(self, *args, **kwargs) -> None:
        self.__configuration = ConfigurationFactory.GetConfiguration(version=self.GetVersion())
        self.__service_alpaca_crypto = ServiceFactory.GetService(version="AlpacaCryptov1")
        self.__service_alpaca_crypto.Start(args=args, kwargs=kwargs)

        try:
            host: str = self.__configuration['controller.grpcservice.host']
            port: int = self.__configuration['controller.grpcservice.port']

            grpc_endpoint: str = f"{host}:{port}"

            with self.__locker4server:
                self.__server.add_insecure_port(grpc_endpoint)
                self.__server.start()
                self.logger.info(f"Starting gRPC service (kcde-api-service) at {grpc_endpoint} ... ")
                self.__server.wait_for_termination()
        
        except KeyError:
            self.logger.error(f"Failed - un-provided host and/or port")
        except Exception as e:
            self.logger.error(f"Failed - {str(e)}")
        finally:
            self.logger.info(f"Leaving ... ")

    def CreateTask(self, request, context):
        if request.metadata.vendor == model.VENDOR_ALPACA_CRYPTO_API:
            __task: model.Task = self.__service_alpaca_crypto.CreateTask(request)
        elif request.metadata.vendor == model.VENDOR_UNKNOWN:
            __task: model.Task = copy.deepcopy(request)
            __task.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
            __task.status.reason = 'Invalid argument - VENDOR_UNKNOWN'
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"{__task.status.reason}")
            return model.Task()
        if __task.status.type == model.TASK_STATUS_ERROR_INVALID_ARGUMENT:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"{__task.status.reason}")
            return model.Task()
        elif __task.status.type == model.TASK_STATUS_ERROR_ALREADY_EXISTS:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(f"{__task.status.reason}")
            return model.Task()
        elif __task.status.type == model.TASK_STATUS_ERROR_UNKNOWN:
            context.set_code(grpc.StatusCode.UNKNOWN)
            context.set_details(f"{__task.status.reason}")
            return model.Task()
        else:
            pass
        
        response = __task
        context.set_code(grpc.StatusCode.OK)
        return response

    def ReadTask(self, request, context):
        try:
            __task: model.Task = self.__service.ReadTask(request.value)
        
            response = __task
            context.set_code(grpc.StatusCode.OK)
            return response
        
        except KeyError as e:
            self.logger.error(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"KeyError - {str(e)}")
            return model.Task()

        context.set_code(grpc.StatusCode.UNKNOWN)
        return model_kcdatapipeline.Task()
    
    def DeleteTask(self, request, context):
        try:
            __task: model.Task = self.__service.DeleteTask(request.value)
            
            response = __task
            context.set_code(grpc.StatusCode.OK)
            return response
        
        except KeyError as e:
            self.logger.error(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"KeyError - {str(e)}")
            return model.Task()

        context.set_code(grpc.StatusCode.UNKNOWN)
        return model.Task()
    
    def ListTasks(self, request, context):
        __tasks: model.Tasks = self.__service.ListTasks()

        response = __tasks
        context.set_code(grpc.StatusCode.OK)
        return response
