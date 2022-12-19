from . import Configuration
from .v1 import ConfigurationV1

import types
import typing

class ConfigurationFactory:
    __lambda_implementations: typing.Dict[str, types.MethodType] = {
        "v0": Configuration,
        "v1": ConfigurationV1,
    }

    __implementations: typing.Dict[str, Configuration] = {
        "v1": None
    }
    
    @classmethod
    def GetConfiguration(cls, *args, **kwargs) -> Configuration:
        client: cls.__lambda_implementations["v0"] = None
        try:
            if cls.__implementations[kwargs["version"]] is None:
                cls.__implementations[kwargs["version"]] = cls.__lambda_implementations[kwargs["version"]]()
            client = cls.__implementations[kwargs["version"]]
        except KeyError:
            client = cls.__lambda_implementations["v0"]()
        return client