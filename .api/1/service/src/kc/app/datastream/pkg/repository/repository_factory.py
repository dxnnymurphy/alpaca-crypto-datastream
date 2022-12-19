from . import Repository
from .v1 import RepositoryV1

import types
import typing

class RepositoryFactory:
    __lambda_implementations: typing.Dict[str, types.MethodType] = {
        "v0": Repository,
        "v1": RepositoryV1,
    }

    __implementations: typing.Dict[str, Repository] = {
        "v1": None
    }
    
    @classmethod
    def GetRepository(cls, *args, **kwargs) -> Repository:
        client: cls.__lambda_implementations["v0"] = None
        try:
            if cls.__implementations[kwargs["version"]] is None:
                cls.__implementations[kwargs["version"]] = cls.__lambda_implementations[kwargs["version"]]()
            client = cls.__implementations[kwargs["version"]]
        except KeyError:
            client = cls.__lambda_implementations["v0"]()
        return client