from . import Application
from .v1 import ApplicationV1

import types
import typing

class ApplicationFactory:
    __lambda_implementations: typing.Dict[str, types.MethodType] = {
        "v0": Application,
        "v1": ApplicationV1,
    }

    __implementations: typing.Dict[str, Application] = {
        "v1": None
    }
    
    @classmethod
    def GetApplication(cls, *args, **kwargs) -> Application:
        client: cls.__lambda_implementations["v0"] = None
        try:
            if cls.__implementations[kwargs["version"]] is None:
                cls.__implementations[kwargs["version"]] = cls.__lambda_implementations[kwargs["version"]]()
            client = cls.__implementations[kwargs["version"]]
        except KeyError:
            client = cls.__lambda_implementations["v0"]()
        return client