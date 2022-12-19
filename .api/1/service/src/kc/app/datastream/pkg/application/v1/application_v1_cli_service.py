import click

from kc.app.datastream.pkg.configuration import Configuration, ConfigurationFactory
from kc.app.datastream.pkg.controller.grpcservice import ControllerGrpcService, ControllerGrpcServiceFactory

class ApplicationV1_CLI_Service:
    @staticmethod
    @click.command(name="service-start")
    @click.option("--controller_grpcservice_host", type=str, 
                  help="set gRPC service host")
    @click.option("--controller_grpcservice_port", type=int,
                  help="set gRPC service port")
    def RunCLIServiceStart(controller_grpcservice_host: str, controller_grpcservice_port: int) -> None:
        configuration: Configuration = ConfigurationFactory.GetConfiguration(version="v1")
        
        if controller_grpcservice_host != None:
            configuration['controller']['grpcservice']['host'] = controller_grpcservice_host
        if controller_grpcservice_port != None:
            configuration['controller']['grpcservice']['port'] = controller_grpcservice_port
        
        grpcservice: ControllerGrpcService = ControllerGrpcServiceFactory.GetControllerGrpcService(version="v1")
        grpcservice.Start()
