import json
import pandas as pd
import requests
import string
import typing

from kc.app.core.annotation import Logger

@Logger
class ConnectivityRest:
    __configuration: typing.Dict = {}
    @property
    def configuration(self) -> typing.Dict:
        return self.__configuration
    
    def __init__(self, *args, **kwargs):
        try:
            self.__configuration = kwargs["configuration"]
            ### configuration.url
            if not "url" in self.__configuration:
                raise KeyError(f"Missing required configuration: url")
            ### configuration.method
            if not "method" in self.__configuration:
                self.__configuration["method"] = "GET"
            ### configuration.credential
            if not "credential" in self.__configuration:
                self.__configuration["credential"] = None
            ### configuration.headers
            if not "headers" in self.__configuration:
                self.__configuration["headers"] = None
            ### configuration.params
            if not "params" in self.__configuration:
                self.__configuration["params"] = None
            ### configuration.body
            if not "body" in self.__configuration:
               self.__configuration["body"] = None
            ### configuration.bodytemplate
            if not "bodytemplate" in self.__configuration:
               self.__configuration["bodytemplate"] = None
            ### configuration.paramstemplate
            if not "paramstemplate" in self.__configuration:
               self.__configuration["paramstemplate"] = None
            ### configuration.proxies
            if not "proxies" in self.__configuration:
                self.__configuration["proxies"] = None
        except KeyError as e:
            self.logger.error(f"[ConnectivityRest::__init__] Error: { str(e) }")
    
    def __call__(self, Clazz) -> typing.Any:
        @Logger
        class __Clazz_AnnotatedBy_ConnectivityRest(Clazz):
            __configuration: typing.Dict = self.configuration
            
            @property
            def configuration(self) -> typing.Dict:
                return self.__configuration
            
            def __init__(self, *args, **kwargs):
                super().__init__(*args,**kwargs)
            
            def ExtractData(self, *args, **kwargs) -> typing.Dict:
                __requests_http_basic_auth: requests.auth.HTTPBasicAuth = None
                if self.__configuration["credential"]:
                    with open(self.__configuration["credential"]) as __f:
                        __credential: typing.Dict = json.load(__f)
                        __requests_http_basic_auth = requests.auth.HTTPBasicAuth(__credential["username"],
                                                                                 __credential["password"])
                
                __requests_params = self.configuration["params"]
                if "rest_request_params" in kwargs.keys():
                    __requests_params = kwargs["rest_request_params"]

                if "rest_request_params_format" in kwargs.keys():
                    __requests_paramstemplate = self.configuration["paramstemplate"]
                    __requests_paramsformat = kwargs["rest_request_params_format"]

                    if __requests_paramstemplate != None:
                        with open(__requests_paramstemplate) as __f:
                            __requests_params = json.loads(string.Template(__f.read()).substitute(**__requests_paramsformat))
                
                    
                __requests_body = self.configuration["body"]
                if "rest_request_body" in kwargs.keys():
                    __requests_body = kwargs["rest_request_body"]
                
                if __requests_body == None:
                    __requests_bodytemplate: str = self.configuration["bodytemplate"]
                    __requests_bodyformat: typing.Dict = {}
                    if "rest_request_body_format" in kwargs.keys():
                        __requests_bodyformat = kwargs["rest_request_body_format"]

                    if __requests_bodytemplate != None:
                        with open(__requests_bodytemplate) as __f:
                            __requests_body = json.loads(string.Template(__f.read()).substitute(**__requests_bodyformat))

                self.logger.info(f'Starting - REST call - URL: {self.configuration["url"]} | Method: {self.__configuration["method"]} | RequestBody: {__requests_body} | Params: {__requests_params}')
                
                __response: requests.models.Response = None
                if self.__configuration["method"] == "GET":
                    __response = requests.get(self.configuration["url"],
                                              auth=__requests_http_basic_auth,
                                              params=__requests_params,
                                              headers=self.configuration["headers"],
                                              proxies=self.configuration["proxies"],
                                              verify=False,
                                              timeout=60)
                elif self.__configuration["method"] == "POST":
                    __response = requests.post(self.configuration["url"],
                                               auth=__requests_http_basic_auth,
                                               params=__requests_params,
                                               headers=self.configuration["headers"],
                                               json=__requests_body,
                                               proxies=self.configuration["proxies"],
                                               verify=False,
                                               stream=True,
                                               timeout=60)
                elif self.__configuration["method"] == "PUT":
                    __response = requests.put(self.configuration["url"],
                                              auth=__requests_http_basic_auth,
                                              params=__requests_params,
                                              headers=self.configuration["headers"],
                                              json=__requests_body,
                                              proxies=self.configuration["proxies"],
                                              verify=False,
                                              timeout=60)
                elif self.__configuration["method"] == "DELETE":
                    __response = requests.delete(self.configuration["url"],
                                                 auth=__requests_http_basic_auth,
                                                 params=__requests_params,
                                                 headers=self.configuration["headers"],
                                                 json=__requests_body,
                                                 proxies=self.configuration["proxies"],
                                                 verify=False,
                                                 timeout=60)
                else:
                    raise KeyError("Invalid configuration: method. Reason: Must be one of GET, POST, PUT, DELETE.")
                
                response: typing.Dict = {
                    "metadata": self.configuration,
                    "spec": __response,
                    "status": {
                        "code":   __response.status_code,
                        "reason": __response.reason,
                    },
                }

                self.logger.info(f'Completed - REST call - URL: {self.configuration["url"]} | Method: {self.__configuration["method"]} | Response: {__response} | Response Headers: {__response.headers} | Params: {__requests_params}')
                                
                return response
            
            def ExtractDataFrame(self, *args, **kwargs) -> pd.DataFrame:
                json2df: typing.Callable[[typing.Dict], pd.DataFrame] = kwargs["json2df"]
                
                response: typing.Dict = self.ExtractData(*args, **kwargs)
                if response["status"]["code"] != 200:
                    return None
                
                return json2df(response["spec"].json())

            def LoadData(self, *args, **kwargs) -> typing.Dict:
                ### Note: For ConnectivityRest, LoadData = ExtractData
                return self.ExtractData(*args, **kwargs)
            
        return __Clazz_AnnotatedBy_ConnectivityRest