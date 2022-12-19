import confluent_kafka
from prometheus_kafka_producer.metrics_manager import ProducerMetricsManager as KafkaProducerMetricsManager
import threading
import typing

from kc.app.core.annotation import Logger

@Logger
class ConnectivityKafka:
    __configuration: typing.Dict = {}
    @property
    def configuration(self) -> typing.Dict:
        return self.__configuration
    
    def __init__(self, *args, **kwargs):
        try:
            self.__configuration = kwargs["configuration"]
            ### configuration - topic
            if not "topic" in self.__configuration:
                raise KeyError(f"Missing required configuration: topic")
            ### configuration - bootstrap.servers
            if not "bootstrap.servers" in self.__configuration:
                raise KeyError(f"Missing required configuration: bootstrap.servers")
            ### configuration - queue.buffering.max.messages
            if not "queue.buffering.max.messages" in self.__configuration:
                raise KeyError(f"Missing required configuration: queue.buffering.max.messages")
            ### configuration - queue.buffering.max.ms
            if not "queue.buffering.max.ms" in self.__configuration:
                raise KeyError(f"Missing required configuration: queue.buffering.max.ms")
            ### configuration - batch.size
            if not "batch.size" in self.__configuration:
                raise KeyError(f"Missing required configuration: batch.size")
            
        except KeyError as e:
            self.logger.error(f"[ConnectivityKafka::__init__] Error: { str(e) }")
    
    def __call__(self, Clazz) -> typing.Any:
        @Logger
        class __Clazz_AnnotatedBy_ConnectivityKafka(Clazz):
            __configuration: typing.Dict = self.configuration
            __kafka_producer: confluent_kafka.Producer = None
            __locker_for_kafka_producer: threading.Lock = None
            __kafka_producer_metrics_manager: KafkaProducerMetricsManager = None
            
            @property
            def configuration(self) -> typing.Dict:
                return self.__configuration
            @property
            def kafka_producer(self) -> confluent_kafka.Producer:
                return self.__kafka_producer

            def __init__(self, *args, **kwargs):
                self.__kafka_producer_metrics_manager = KafkaProducerMetricsManager()
                self.__kafka_producer = confluent_kafka.Producer({"bootstrap.servers": self.__configuration["bootstrap.servers"],
                                                                  "queue.buffering.max.messages": self.__configuration["queue.buffering.max.messages"],
                                                                  "queue.buffering.max.ms": self.__configuration["queue.buffering.max.ms"],
                                                                  "batch.size": self.__configuration["batch.size"],
                                                                  "compression.type": "lz4",
                                                                  #"statistics.interval.ms": 250,   ### BIET-128: Detected memory leak here.
                                                                  "stats_cb": self.__kafka_producer_metrics_manager.send})
                self.__locker_for_kafka_producer = threading.Lock()
            
            def PublishMessage(self, *args, **kwargs) -> None:
                def __OnDelivery(err: typing.Any, msg: typing.Any) -> None:
                    if err is not None:
                        print(f"[ConnectivityKafka] Failed to deliver message - {str(msg)} | error - {str(err)}")
                    else:
                        pass
                
                with self.__locker_for_kafka_producer:
                    self.__kafka_producer.produce(topic=self.__configuration["topic"], 
                                                  value=kwargs["message"],
                                                  on_delivery=__OnDelivery)
                    self.__kafka_producer.poll(0)

        return __Clazz_AnnotatedBy_ConnectivityKafka
