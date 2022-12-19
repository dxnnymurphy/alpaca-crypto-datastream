from .application_v1_cli_service import ApplicationV1_CLI_Service

import click
import typing

class ApplicationV1_CLI(ApplicationV1_CLI_Service):
    RunCLI: typing.Callable[[], None] = None
    
    def __init__(self):
        ApplicationV1_CLI.__RunCLI.add_command(ApplicationV1_CLI_Service.RunCLIServiceStart)
        self.RunCLI = ApplicationV1_CLI.__RunCLI

    @staticmethod
    @click.group()
    def __RunCLI() -> None:
        pass
