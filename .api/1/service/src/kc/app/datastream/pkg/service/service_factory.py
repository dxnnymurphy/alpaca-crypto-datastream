from . import Service
from .alpacacryptov1 import ServiceAlpacaCryptoV1

import types
import typing

class ServiceFactory:
    __lambda_implementations: typing.Dict[str, types.MethodType] = {
        "v0": Service,
        "AlpacaCryptov1": ServiceAlpacaCryptoV1,
    }

    __implementations: typing.Dict[str, Service] = {
        "AlpacaCryptov1": None
    }
    
    @classmethod
    def GetService(cls, *args, **kwargs) -> Service:
        client: cls.__lambda_implementations["v0"] = None
        try:
            if cls.__implementations[kwargs["version"]] is None:
                cls.__implementations[kwargs["version"]] = cls.__lambda_implementations[kwargs["version"]]()
            client = cls.__implementations[kwargs["version"]]
        except KeyError:
            client = cls.__lambda_implementations["v0"]()
        return client