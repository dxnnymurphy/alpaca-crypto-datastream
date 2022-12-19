from elasticsearch import Elasticsearch
import json
import pandas as pd
import typing

from kc.app.core.annotation import Logger

@Logger
class ConnectivityElasticsearch:
    __configuration: typing.Dict = {}
    @property
    def configuration(self) -> typing.Dict:
        return self.__configuration
    
    def __init__(self, *args, **kwargs):
        try:
            self.__configuration = kwargs["configuration"]
            ### configuration.hosts
            if not "hosts" in self.__configuration:
                raise KeyError(f"Missing required configuration: hosts")
            else:
                self.__configuration["hosts"] = self.__configuration["hosts"].split(",")
            ### configuration.credential
            if not "credential" in self.__configuration:
                self.__configuration["credential"] = None
        except KeyError as e:
            self.logger.error(f"[ConnectivityElasticsearch::__init__] Error: { str(e) }")
    
    def __call__(self, Clazz) -> typing.Any:
        @Logger
        class __Clazz_AnnotatedBy_ConnectivityElasticsearch(Clazz):
            __configuration: typing.Dict = self.configuration
            __elasticsearch: Elasticsearch = None
            
            @property
            def configuration(self) -> typing.Dict:
                return self.__configuration
            @property
            def elasticsearch(self) -> Elasticsearch:
                return self.__elasticsearch
            
            def __init__(self, *args, **kwargs):
                __elasticsearch_basic_auth: typing.Tuple = None
                if self.__configuration["credential"]:
                    with open(self.__configuration["credential"]) as __f:
                        __credential: typing.Dict = json.load(__f)
                        __elasticsearch_basic_auth = (__credential["username"],
                                                      __credential["password"])
                self.__elasticsearch = Elasticsearch(hosts=self.__configuration["hosts"],
                                                     basic_auth=__elasticsearch_basic_auth,
                                                     verify_certs=False,
                                                     request_timeout=300)
                super().__init__(*args,**kwargs)
            
            def ExtractDataFrame(self, *args, **kwargs) -> pd.DataFrame:
                self.logger.info(f"ExtractDataFrame - Elasticsearch SQL Query:\n{kwargs['elasticsearch_sql_query']}")
                __data = []
                try:
                    __cursor: str = ''
                    while True:
                        if not __cursor:
                            response = self.__elasticsearch.sql.query(body={
                                "query": kwargs["elasticsearch_sql_query"]
                            })
                            __columns = response["columns"]
                        else:
                            response = self.__elasticsearch.sql.query(body={
                                "cursor": __cursor
                            })
                        __data.extend(response["rows"])
                        __cursor = response["cursor"]
                except KeyError as e:
                    pass
                __df = pd.DataFrame(data=__data, 
                                    columns=[column["name"] for column in __columns])
                __df["@timestamp"] = __df["@timestamp"].apply(pd.to_datetime)
                __df.set_index(keys="@timestamp", 
                               inplace=True)
                del __data
                del __columns
                return __df
                
        return __Clazz_AnnotatedBy_ConnectivityElasticsearch
