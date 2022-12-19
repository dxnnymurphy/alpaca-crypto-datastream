import abc

class Application(abc.ABC):
    @abc.abstractmethod
    def GetVersion(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def Run(self, *args, **kwargs) -> None:
        raise NotImplementedError
