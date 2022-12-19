from .. import Configuration

from environs import Env
import flatdict
from pathlib import Path
import typing
import yaml

from kc.app.core.annotation import Logger, Singleton
import kc.app.datastream as kcx

@Singleton
@Logger
class ConfigurationV1(Configuration):
    __configuration: flatdict.FlatDict = None

    def __init__(self):
        self.__configuration = flatdict.FlatDict(yaml.safe_load(Path(kcx.APP_RESOURCE_PATH, 'config/application.yml').read_text()),
                                                 delimiter='.')
        self.logger.debug(f"Loaded default configuration from config/application.yml - {self.__configuration}")

        env = Env(expand_vars=True)
        with env.prefixed("KCDE_API_1_SERVICE_"):
            for configuration_key in self.__configuration.keys():
                self.__configuration[configuration_key] = env(configuration_key.upper().replace('.','_'), 
                                                              self.__configuration[configuration_key])
        self.logger.debug(f"Overrided configuration from environment variables - {self.__configuration}")

    def GetVersion(self) -> str:
        return "v1"

    def __getitem__(self, key: str) -> typing.Any:
        return self.__configuration[key]

    def __str__(self) -> str:
        return f"{self.__configuration}"
