from .. import Repository

import typing

from kc.app.core.annotation import Logger, Singleton
from kc.app.data.connectivity.annotation import ConnectivityKafka, ConnectivityRest
from kc.app.datastream.pkg.configuration import Configuration, ConfigurationFactory

@Singleton
@Logger
class RepositoryV1(Repository):
    __configuration: Configuration = None
    
    __repository_rest_alpaca_crypto_1:   typing.Any = None
    
    __repository_kafka_1: typing.Any = None

    def __init__(self, *args, **kwargs):
        self.__configuration = ConfigurationFactory.GetConfiguration(version="v1")
        self.__InitializeRepositoryRestAlpacaCrypto1(*args, **kwargs)
        self.__InitializeRepositoryKafka1(*args, **kwargs)

    def GetVersion(self) -> str:
        return "v1"

    @property
    def repository_rest_alpaca_crypto_1(self) -> typing.Any: 
        return self.__repository_rest_alpaca_crypto_1
    @property
    def repository_kafka_1(self) -> typing.Any: 
        return self.__repository_kafka_1

    def ExtractData(self, *args, **kwargs) -> typing.Dict:
        __repository_target: str = kwargs["target"]
        
        if __repository_target == "rest-alpaca-crypto-1":
            return self.__ExtractData_RestAlpacaCrypto1(*args, **kwargs)
        else:
            pass
    
    def LoadData(self, *args, **kwargs) -> typing.Dict:
        __repository_target: str = kwargs["target"]
        
        if __repository_target == "kafka-1":
            self.__LoadData_Kafka1(*args, **kwargs)
            return None
        else:
            pass
    
    def __InitializeRepositoryRestAlpacaCrypto1(self, *args, **kwargs) -> None:
        @ConnectivityRest(configuration={
           "url": self.__configuration['repository.connectivity.rest.alpaca.crypto.1.url'],
           "method": self.__configuration['repository.connectivity.rest.alpaca.crypto.1.method'],
        })
        class __RepositoryRest:
            pass
        self.__repository_rest_alpaca_crypto_1 = __RepositoryRest()
    
    def __InitializeRepositoryKafka1(self, *args, **kwargs) -> None:
        @ConnectivityKafka(configuration={
            "bootstrap.servers": self.__configuration['repository.connectivity.kafka.1.bootstrap_servers'],
            "topic": self.__configuration['repository.connectivity.kafka.1.topic'],
            "queue.buffering.max.messages": self.__configuration['repository.connectivity.kafka.1.spec.queue_buffering_max_messages'],
            "queue.buffering.max.ms": self.__configuration['repository.connectivity.kafka.1.spec.queue_buffering_max_ms'],
            "batch.size": self.__configuration['repository.connectivity.kafka.1.spec.batch_size'],
        })
        class __RepositoryKafka:
            pass
        self.__repository_kafka_1 = __RepositoryKafka()
    
    def __ExtractData_RestAlpacaCrypto1(self, *args, **kwargs) -> typing.Dict:
        __data: typing.Dict = self.__repository_rest_alpaca_crypto_1\
                                  .ExtractData(*args, **kwargs)
        return __data

    def __LoadData_Kafka1(self, *args, **kwargs) -> None:
        self.__repository_kafka_1.PublishMessage(*args, **kwargs)