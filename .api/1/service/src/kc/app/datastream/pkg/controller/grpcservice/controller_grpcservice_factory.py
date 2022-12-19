from . import ControllerGrpcService
from .v1 import ControllerGrpcServiceV1

import types
import typing

class ControllerGrpcServiceFactory:
    __lambda_implementations: typing.Dict[str, types.MethodType] = {
        "v0": ControllerGrpcService,
        "v1": ControllerGrpcServiceV1,
    }

    __implementations: typing.Dict[str, ControllerGrpcService] = {
        "v1": None
    }
    
    @classmethod
    def GetControllerGrpcService(cls, *args, **kwargs) -> ControllerGrpcService:
        client: cls.__lambda_implementations["v0"] = None
        try:
            if cls.__implementations[kwargs["version"]] is None:
                cls.__implementations[kwargs["version"]] = cls.__lambda_implementations[kwargs["version"]]()
            client = cls.__implementations[kwargs["version"]]
        except KeyError:
            client = cls.__lambda_implementations["v0"]()
        return client