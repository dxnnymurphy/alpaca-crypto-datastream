import typing

class Singleton:
    __Clazz: type = None
    __instance: typing.Any = None
    
    def __init__(self, Clazz):
        self.__Clazz = Clazz
       
    def __call__(self, *args, **kwargs) -> None:
        if self.__instance is None:
            self.__instance = self.__Clazz(*args, **kwargs)
        return self.__instance
        
    def __instancecheck__(self, instance: typing.Any) -> bool:
        return isinstance(instance, self.__Clazz)
