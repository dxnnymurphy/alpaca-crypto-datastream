import abc
import kc.app.datastream.pkg.model.datastream.v3.service_datastream_pb2 as model

class Service(abc.ABC):
    @abc.abstractmethod
    def GetVersion(self) -> str:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def Start(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def CreateTask(self, query: model.Task) -> model.Task:
        raise NotImplementedError()

    @abc.abstractmethod
    def ReadTask(self, id_query: str) -> model.Task:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def DeleteTask(self, id_query: str) -> model.Task:
        raise NotImplementedError()

    @abc.abstractmethod
    def ListTasks(self) -> model.Tasks:
        raise NotImplementedError()
    