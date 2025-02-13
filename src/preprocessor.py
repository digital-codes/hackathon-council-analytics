import os
import tomllib
from typing import Optional
"""
This Module provides classes for preprocessing

Classes:
- 'Preprocessor': provide preprocessing functions

Example usage:

    >>> import preprocessoor
    >>> pp = preprocessor(configfile)
    >>> pp.show_config()
    Key: Value:
    filestore: nextcloud
    ....
    
    
"""


# Defaults
filestorage = 'nextcloud'


class Preprocessor:

    def __init__(self, configfile: Optional[str] = None) -> None:
        if not configfile:
            configfile = os.path.expanduser(os.path.join('~','.config','hca','config.toml'))
         
        #breakpoint()
        try:
            with open(configfile, "rb") as f:
                config = tomllib.load(f)
        except FileNotFoundError:
            raise Exception(f"missing configfile at {configfile}")
        
        self.filestorage = config.get('preprocessor',{}).get('filestorage') or filestorage

    def show_config(self) -> str:
        print(f"filestorage: {self.filestorage}")
