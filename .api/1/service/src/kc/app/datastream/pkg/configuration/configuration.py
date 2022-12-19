import abc
import typing

class Configuration(abc.ABC):
    def GetVersion(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def __getitem__(self, key: str) -> typing.Any:
        raise NotImplementedError()
