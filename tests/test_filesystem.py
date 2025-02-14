import pytest
import os
from importlib import import_module

def test_module(filesytem_config):
    config = filesytem_config
    filestorage = config['preprocessor']['filestorage']
    fsm = import_module(f"src.storage.{filestorage}")
    assert type(fsm).__name__ == 'module'

def test_class(filesytem_config):
    config = filesytem_config
    filestorage = config['preprocessor']['filestorage']
    fsm = import_module(f"src.storage.{filestorage}")
    fs = fsm.FileStorage(config)
    assert type(fs).__name__ == 'FileStorage'

def test_get_from_storage(filesytem_config):
    config = filesytem_config
    filestorage = config['preprocessor']['filestorage']
    fsm = import_module(f"src.storage.{filestorage}")
    fs = fsm.FileStorage(config)
    result = fs.get_from_storage('testfile.txt')
    assert result == 'Testresultat\n'
def test_put_on_storage(filesytem_config):
    config = filesytem_config
    filestorage = config['preprocessor']['filestorage']
    fsm = import_module(f"src.storage.{filestorage}")
    fs = fsm.FileStorage(config)
    fs.put_on_storage('testfile2.txt', 'Testresultat2')
    result = fs.get_from_storage('testfile2.txt')
    assert result   == 'Testresultat2'

@pytest.fixture
def filesytem_config(my_sample_config):
    config = my_sample_config
    folder = os.path.abspath('./test_data')
    config['filestorage'] = {'path': folder}
    config['preprocessor'] = {'filestorage': 'filesystem'}
    return config

