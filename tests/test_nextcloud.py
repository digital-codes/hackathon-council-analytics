import pytest
import os
from importlib import import_module

def test_module(my_sample_config):
    config = my_sample_config
    filestorage = config['preprocessor']['filestorage']
    fsm = import_module(f"src.storage.{filestorage}")
    assert type(fsm).__name__ == 'module'

def test_class(my_sample_config):
    config = my_sample_config
    filestorage = config['preprocessor']['filestorage']
    fsm = import_module(f"src.storage.{filestorage}")
    fs = fsm.FileStorage(config)
    assert type(fs).__name__ == 'FileStorage'
def test_file_storage(my_sammple_config):
    configparser = my_sammple_config
    assert False
