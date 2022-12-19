from .. import Service

import copy
from datetime import date, datetime, timedelta
import dateutil
import json
import pandas as pd
import prometheus_client, prometheus_client.metrics
import random
import re
import threading
import time
import typing
import uuid

from kc.app.core.annotation import Logger, Singleton
from kc.app.datastream.pkg.configuration import Configuration, ConfigurationFactory
import kc.app.datastream.pkg.model.datastream.v3.service_datastream_pb2 as model
from kc.app.datastream.pkg.repository import Repository, RepositoryFactory

@Singleton
@Logger
class ServiceAlpacaCryptoV1(Service):
    __configuration: Configuration = None
    __repository: Repository = None

    __tasks: typing.Dict[str, model.Task] = None
    __locker4tasks: threading.Lock = None

    __threads_for_executor_process_task: typing.List[threading.Thread] = None

    __metric_kcde_number_of_tasks_remaining: prometheus_client.metrics.Gauge = None
    __metric_kcde_task_target_latency_seconds: prometheus_client.metrics.Gauge = None
    
    def __init__(self):
        self.__configuration = ConfigurationFactory.GetConfiguration(version=self.GetVersion())
        self.__repository = RepositoryFactory.GetRepository(version=self.GetVersion())

        self.__tasks = {}
        self.__locker4tasks = threading.Lock()

        __size_of_executor_pool: int = int(self.__configuration["service.executorpool.size"])
        self.__threads_for_executor_process_task = []
        for __executor_affinity in range(__size_of_executor_pool):
            self.__threads_for_executor_process_task.append(threading.Thread(target=self.__StartExecutor_ProcessTask,
                                                                             kwargs={'executor_affinity': __executor_affinity}))
        
        self.__metric_kcde_number_of_tasks_remaining = prometheus_client.Gauge(name="kcde_number_of_tasks_remaining",
                                                                               documentation="Number of tasks remaining in queue")
        
        self.__metric_kcde_task_target_latency_seconds = prometheus_client.Gauge(name="kcde_task_target_latency_seconds",
                                                                                 documentation="Time spent in a specific task phase",
                                                                                 labelnames=["task", "target", "executor_affinity"])

    def GetVersion(self) -> str:
        return "v1"

    def Start(self, *args, **kwargs) -> None:
        self.logger.info(f"Started service - version: { self.GetVersion() } | configuration:  { self.__configuration }")
        prometheus_client.start_wsgi_server(port=int(self.__configuration["service.ops.monitoring.api.port"]),
                                            addr=self.__configuration["service.ops.monitoring.api.host"])
        
        with self.__locker4tasks:
            self.__metric_kcde_number_of_tasks_remaining.set(0)
        
        for __thread in self.__threads_for_executor_process_task:
            __thread.start()
        
    ####################################################################
    ### CRD service - Task 
    ####################################################################

    def CreateTask(self, task: model.Task) -> model.Task:
        __task1: model.Task = self.__ValidateTask(task)
        if __task1.status.type == model.TASK_STATUS_ERROR_INVALID_ARGUMENT:
            return __task1
        
        with self.__locker4tasks:
            if __task1.metadata.id in self.__tasks.keys():
                __task1.status.type = model.TASK_STATUS_ERROR_ALREADY_EXISTS
                __task1.status.reason = f'Already exists - { __task1.metadata.id }'
                return __task1
            
            __task1.status.type = model.TASK_STATUS_CREATED
            self.__tasks[__task1.metadata.id] = __task1
            self.__metric_kcde_number_of_tasks_remaining.set(len(self.__tasks))
            return self.__tasks[__task1.metadata.id]

    def ReadTask(self, id_task: str) -> model.Task:
        with self.__locker4tasks:
            return self.__tasks[id_task]
    
    def DeleteTask(self, id_task: str) -> model.Task:
        with self.__locker4tasks:
            __task1: model.Task = self.__tasks.pop(id_task)
            self.__metric_kcde_number_of_tasks_remaining.set(len(self.__tasks))
            return __task1

    def ListTasks(self) -> model.Tasks:
        with self.__locker4tasks:
            tasks = model.Tasks()
            tasks.metadata.id = str(uuid.uuid4())
            tasks.spec.items.extend([ task for id_task, task in self.__tasks.items() ])
            tasks.spec.number_of_items = len(self.__tasks)
            return tasks

    ####################################################################
    ### (END) CRD service - Task 
    ####################################################################
    
    ####################################################################
    ### __ValidateTask 
    ####################################################################
    
    def __ValidateTask(self, task: model.Task) -> model.Task:
        __task1: model.Task = copy.deepcopy(task)
        
        if __task1.metadata.type == model.TaskType_UNKNOWN:
            __task1.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
            __task1.status.reason = 'Invalid argument - __task1.metadata.type == model.TaskType_UNKNOWN'
            return __task1
        
        if __task1.metadata.id == "":
            __task1.metadata.id = str(uuid.uuid4())
        if __task1.metadata.namespace == "":
            __task1.metadata.namespace = "datastream"

        if __task1.metadata.type == model.TASK_ALPACA_CRYPTO_TRADE_SEARCH   :
            __task1 = self.__ValidateTask_AlpacaCrypto_TradeSearch(__task1)
        elif __task1.metadata.type == model.TASK_ALPACA_CRYPTO_REPLAY_TRADE_SEARCH   :
            __task1 = self.__ValidateTask_AlpacaCrypto_Replay_TradeSearch(__task1)

        return __task1

    def __ValidateTask_AlpacaCrypto_TradeSearch(self, task: model.Task) -> model.Task:
        __spec: model.TaskAlpacaCryptoTradeSearch = task.spec.task_alpaca_crypto_trade_search

        if task.metadata.currency == model.CURRENCY_ETH_USD:
            __spec.currency = "ETH/USD"
        elif task.metadata.currency == model.CURRENCY_BTC_USD:
            __spec.currency = "BTC/USD"
        elif task.metadata.currency == model.CURRENCY_UNKNOWN:
            task.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
            task.status.reason = 'Invalid argument - Currency Unknown'
            return task
        
        if __spec.startTime != "":
            if __spec.searchDuration > 0:
                task.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
                task.status.reason = 'Invalid argument - (__spec.startTime != "") and (__spec.searchDuration > 0)'
                return task

            if __spec.endTime == "":
                __spec.endTime = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            try:
                __startTime: datetime = dateutil.parser.parse(__spec.startTime)
                __endTime: datetime = dateutil.parser.parse(__spec.endTime)
                if __startTime > __endTime:
                    task.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
                    task.status.reason = 'Invalid argument - __startTime > __endTime'
                    return task
                __spec.startTime = __startTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                __spec.endTime  = __endTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            except dateutil.parser.ParserError as e:
                task.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
                task.status.reason = f'Invalid argument - dateutil.parser.ParserError - {str(e)}'
                return task
            except Exception as e:
                task.status.type = model.TASK_STATUS_ERROR_UNKNOWN
                task.status.reason = f'Error - {str(e)}'
                return task
        
        else:
            if __spec.endTime == "":
                __spec.endTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            
            if __spec.searchDuration <= 0:
                task.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
                task.status.reason = 'Invalid argument - (__spec.startTime == "") and (__spec.searchDuration <= 0)'
                return task
            
            __endTime: datetime = dateutil.parser.parse(__spec.endTime)
            __startTime: datetime = __endTime - timedelta(seconds=__spec.searchDuration)
            __spec.startTime = __startTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            __spec.endTime  = __endTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        return task

    def __ValidateTask_AlpacaCrypto_Replay_TradeSearch(self, task: model.Task) -> model.Task:
        __spec: model.TaskAlpacaCryptoReplayTradeSearch = task.spec.task_alpacacrypto_replay_trade_search

        if __spec.searchDuration <= 0:
            task.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
            task.status.reason = 'Invalid argument - __spec.searchDuration <= 0'
            return task
        if __spec.searchDuration > 300:
            task.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
            task.status.reason = 'Invalid argument - __spec.searchDuration > 300'
            return task

        if __spec.startTime == "" or __spec.endTime == "":
            task.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
            task.status.reason = 'Invalid argument - __spec.startTime == "" or __spec.endTime == ""'
            return task

        try:
            __today: date = date.today()
            __yesterday: date = __today - timedelta(days=1)
            __last_monday: date = __today - timedelta(days=__today.weekday())
            __last_saturday: date = __last_monday + timedelta(days=5)
            
            if __spec.startTime == "START-OF-LAST-TRADING-WEEK" and __spec.endTime == "END-OF-LAST-TRADING-WEEK":
                __spec.startTime = __last_monday.strftime('%Y-%m-%d') + 'T06:00:00Z'
                __spec.endTime = __last_saturday.strftime('%Y-%m-%d') + 'T06:00:00Z'
            elif __spec.startTime == "START-OF-LAST-TRADING-DAY" and __spec.endTime == "END-OF-LAST-TRADING-DAY":
                __spec.startTime = __yesterday.strftime('%Y-%m-%d') + 'T00:00:00Z'
                __spec.endTime = __today.strftime('%Y-%m-%d') + 'T00:00:00Z' 
            else:
                pass
            
            __startTime: datetime = dateutil.parser.parse(__spec.startTime)
            __endTime: datetime = dateutil.parser.parse(__spec.endTime)
            if __startTime > __endTime:
                task.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
                task.status.reason = 'Invalid argument - __startTime > __endTime'
                return task
            __spec.startTime = __startTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            __spec.endTime  = __endTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        except dateutil.parser.ParserError as e:
            task.status.type = model.TASK_STATUS_ERROR_INVALID_ARGUMENT
            task.status.reason = f'Invalid argument - dateutil.parser.ParserError - {str(e)}'
            return task
        except Exception as e:
            task.status.type = model.TASK_STATUS_ERROR_UNKNOWN
            task.status.reason = f'Error - {str(e)}'
            return task

        return task

    ####################################################################
    ### (END) __ValidateTask
    ####################################################################

    ####################################################################
    ### Executor - ProcessTask
    ####################################################################

    def __StartExecutor_ProcessTask(self, *args, **kwargs) -> None:
        __executor_affinity: int = kwargs["executor_affinity"]
        self.logger.info(f"Starting executor { __executor_affinity } - ProcessTask")

        while True:
            try:
                self.__ExecuteTask_ProcessTask(*args, **kwargs)
            except Exception as e :
                self.logger.error(f"Restarting executor {__executor_affinity} due to exception - {str(e)}")
            
            time.sleep(1.)

        self.logger.fatal(f"Code should never reach here.")

    def __ExecuteTask_ProcessTask(self, *args, **kwargs) -> None:
        __id_task: str = None
        with self.__locker4tasks:
            if self.__tasks:
                __id_task = random.choice(list(self.__tasks.keys()))
        
        if not __id_task:
            return
        
        __task: model.Task = self.ReadTask(__id_task)

        __executor_affinity: int = kwargs["executor_affinity"]
        if __task.metadata.executor_affinity == __executor_affinity:
            if __task.metadata.type == model.TASK_ALPACA_CRYPTO_TRADE_SEARCH:
                self.__ExecuteTask_ProcessTask_AlpacaCrypto_TradeSearch(__task, *args, **kwargs)
            elif __task.metadata.type == model.TASK_ALPACA_CRYPTO_REPLAY_TRADE_SEARCH:
                self.__ExecuteTask_Replay_ProcessTask_AlpacaCrypto_TradeSearch(__task, *args, **kwargs)
            else:
                pass
        else:
            self.logger.debug(f"Executor {__executor_affinity} will not execute task {__id_task}")
            pass
    
    def __ExecuteTask_ProcessTask_AlpacaCrypto_TradeSearch(self, task: model.Task, *args, **kwargs) -> None:
        __executor_affinity: int = kwargs["executor_affinity"]
        
        __spec: model.TaskAlpacaCryptoTradeSearch = task.spec.task_alpaca_crypto_trade_search


        with self.__metric_kcde_task_target_latency_seconds.labels(task="AlpacaCrypto_TradeSearch", 
                                                                   target="extract-rest-alpaca-crypto-1", 
                                                                   executor_affinity=__executor_affinity) \
                                                           .time():
            __data: typing.List = []
            __page_counter: int = 0
            
            __data.append(self.__repository.ExtractData(target="rest-alpaca-crypto-1",
                                                                rest_request_params={
                                                                    "start": __spec.startTime,
                                                                    "end": __spec.endTime,
                                                                    "symbols": __spec.currency
                                                                }))
            self.logger.info(f"{__data[__page_counter]['spec'].json()}")
            __page_token = __data[__page_counter]['spec'].json()['next_page_token']
            while __page_token != None:
                __data.append(self.__repository.ExtractData(target="rest-alpaca-crypto-1",
                                                                rest_request_params={
                                                                    "start": __spec.startTime,
                                                                    "end": __spec.endTime,
                                                                    "symbols": __spec.currency,
                                                                    "page_token": __page_token
                                                                }))
                __page_token = __data[__page_counter]['spec'].json()['next_page_token']
                __page_counter += 1
            ###
            ### BIET-128: Shall we also measure response status-code?
            ###
        if all(page['status']['code'] == 200 for page in __data):
            with self.__metric_kcde_task_target_latency_seconds.labels(task="AlpacaCrypto_TradeSearch", 
                                                                       target="load-kafka-1", 
                                                                       executor_affinity=__executor_affinity) \
                                                               .time():
                __counter_for_fix_messages = 0
                for page in range(len(__data)):
                    self.logger.info(f"namespace: {type(task.metadata.namespace)} vendor: {type(task.metadata.vendor)} pages: {__page_counter}")

                    for __fix_message in __data[page]['spec'].json()["trades"][__spec.currency]:
                                        __counter_for_fix_messages += 1
                                        __fix_message["currency"] = __spec.currency
                                        __decorated_message: typing.Dict = {
                                            "metadata": {
                                                "namespace": task.metadata.namespace,
                                            },
                                            "spec": {
                                                "data": __fix_message,
                                            },
                                        }
                                        self.logger.info(f"Decorated Message: {__decorated_message}")
                                        self.__repository.LoadData(target="kafka-1",
                                                                message=json.dumps(__decorated_message))

                
                self.logger.info(f"Executor {__executor_affinity} published a total of { __counter_for_fix_messages }  messages to Kafka. Number of remaining tasks: { len(self.__tasks) }")

            task.status.type = model.TASK_STATUS_DONE
            self.DeleteTask(task.metadata.id)
        else:
            self.logger.error(f"Executor {__executor_affinity} failed to extract data from API. Status: {__data['status']}")
            task.status.type = model.TASK_STATUS_ERROR_TRANSIENT
            task.status.reason = f"{__data['status']['reason']}"
    
    def __ExecuteTask_Replay_ProcessTask_Ullink_LogSearch(self, task: model.Task, *args, **kwargs) -> None:
        __executor_affinity: int = kwargs["executor_affinity"]
        
        __spec: model.TaskReplayUllinkLogSearch = task.spec.task_replay_ullink_log_search

        __startTime: datetime = dateutil.parser.parse(__spec.startTime)
        __endTime: datetime = dateutil.parser.parse(__spec.endTime)
        
        __checkpoints: typing.List[str] = pd.date_range(start=__startTime, end=__endTime, freq=f"{__spec.timeDurationPerIterationInSeconds}S").strftime("%Y-%m-%dT%H:%M:%S.%fZ").to_list()
        if __checkpoints[-1] != __spec.endTime:
            __checkpoints.append(__spec.endTime)

        self.logger.info(f"Executor {__executor_affinity} will delegate replay Ullink_LogSearch tasks - spec: {__spec} | __checkpoints: {__checkpoints}")

        for __startTime1, __endTime1 in zip(__checkpoints, __checkpoints[1:]):
            __task1: model.Task = model.Task()
            __task1.metadata.type                                      = model.TASK_ULLINK_LOG_SEARCH
            __task1.metadata.namespace                                 = task.metadata.namespace
            __task1.metadata.name                                      = task.metadata.name
            __task1.metadata.environment                               = task.metadata.environment
            __task1.metadata.executor_affinity                         = task.metadata.executor_affinity
            __task1.spec.task_ullink_log_search.productKey.environment = __spec.productKey.environment
            __task1.spec.task_ullink_log_search.productKey.name        = __spec.productKey.name
            __task1.spec.task_ullink_log_search.minimumLevel           = __spec.minimumLevel
            __task1.spec.task_ullink_log_search.startTime              = __startTime1
            __task1.spec.task_ullink_log_search.endTime                = __endTime1
                    
            self.CreateTask(task=copy.deepcopy(__task1))

        task.status.type = model.TASK_STATUS_DONE
        self.DeleteTask(task.metadata.id)

    ####################################################################
    ### (END) Executor - ProcessTask
    ####################################################################
