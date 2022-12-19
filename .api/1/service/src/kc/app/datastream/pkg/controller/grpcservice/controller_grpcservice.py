import abc

class ControllerGrpcService(abc.ABC):
    @abc.abstractmethod
    def GetVersion(self) -> str:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def Start(self, *args, **kwargs) -> None:
        raise NotImplementedError()