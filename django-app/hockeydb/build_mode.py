"""
Provides an easy way to tell if the program is running in a development or production environment by setting an environment variable.
"""

from os import environ
from warnings import warn
from enum import Enum

class BuildMode(Enum):
    DEV : int = 1
    PROD : int = 2
    __MODE : int = 0
    __VARNAME : str = "HOCKEYDB_BUILD_MODE"

    @staticmethod
    def __check_mode_set() -> None:
        """
        Ensures that __MODE is set by setting it if it isn't already.
        """
        if (BuildMode.__MODE == 0):
            try:
                if (environ[BuildMode.__VARNAME].upper() == "DEV"):
                    BuildMode.__MODE = BuildMode.DEV
                elif (environ[BuildMode.__VARNAME].upper() == "PROD"):
                    BuildMode.__MODE = BuildMode.PROD
            except KeyError:
                warn(f"\033[5;31m{BuildMode.__VARNAME} not set, defaulting to DEV\033[0m")
                environ[BuildMode.__VARNAME] = "DEV"
                BuildMode.__MODE = BuildMode.DEV
        return None
    
    @staticmethod
    def mode() -> Enum:
        """
        Return the current build mode.
        """
        BuildMode.__check_mode_set()
        return BuildMode.__MODE
    
    @staticmethod
    def when_dev(func : callable) -> callable:
        """
        The decorated function will only run when in development mode.
        If you are using the output of this function, your program should be able to accept a `None` return value from the decorated function.
        """
        BuildMode.__check_mode_set()
        if BuildMode.__MODE == BuildMode.DEV:
            def ret(*args):
                return func(*args)
            return ret
        else:
            return (lambda *args : None)
        
    @staticmethod
    def when_prod(func : callable) -> callable:
        """
        The decorated function will only run when in production mode.
        If you are using the output of this function, your program should be able to accept a `None` return value from the decorated function.
        """
        BuildMode.__check_mode_set()
        if BuildMode.__MODE == BuildMode.PROD:
            def ret(*args):
                return func(*args)
            return ret
        else:
            return (lambda *args : None)
        
    @staticmethod
    def is_dev() -> bool:
        """
        Returns `True` if running in development mode, and `False` if running in production.
        """
        BuildMode.__check_mode_set()
        return BuildMode.__MODE == BuildMode.DEV
    
    @staticmethod
    def is_prod() -> bool:
        """
        Returns `True` if running in production mode, and `False` if running in development.
        """
        BuildMode.__check_mode_set()
        return BuildMode.__MODE == BuildMode.PROD