from .. import Application
from .application_v1_cli import ApplicationV1_CLI

from kc.app.core.annotation import Logger, Singleton

@Singleton
@Logger
class ApplicationV1(Application,
                    ApplicationV1_CLI):
    def GetVersion(self) -> str:
        return "v1"

    def Run(self, *args, **kwargs) -> None:
        self.RunCLI()
