import abc
import typing

class Repository(abc.ABC):
    @abc.abstractmethod
    def GetVersion(self) -> str:
        raise NotImplementedError()
    
    @property
    @abc.abstractmethod
    def repository_rest_alpaca_crypto_1(self) -> typing.Any:
        raise NotImplementedError()
    @property
    @abc.abstractmethod
    def repository_kafka_1(self) -> typing.Any:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def ExtractData(self, *args, **kwargs) -> typing.Dict:
        raise NotImplementedError()
    
    @abc.abstractmethod
    def LoadData(self, *args, **kwargs) -> typing.Dict:
        raise NotImplementedError()  
