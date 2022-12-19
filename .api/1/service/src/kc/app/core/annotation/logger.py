import logging
import typing

class Logger:
    __Clazz: type = None
    
    def __init__(self, Clazz):
        self.__Clazz = Clazz

    def __call__(self, *args, **kwargs) -> typing.Any:
        ### ClazzMitLoggerEnabled is a proxy class of the underlying with logger enabled
        class ClazzMitLoggerEnabled(self.__Clazz):
            logger: logging.Logger = None
            
            def __init__(self1, *args, **kwargs):
                logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(funcName)s - %(message)s',
                                    datefmt="%Y-%m-%dT%H:%M:%S%z",
                                    level=logging.INFO)
                self1.logger = logging.getLogger(self1.__class__.__bases__[0].__name__)
                super().__init__(*args, **kwargs)
        
        return ClazzMitLoggerEnabled(*args, **kwargs)

    def __instancecheck__(self, instance: typing.Any) -> bool:
        return isinstance(instance, self.__Clazz)
