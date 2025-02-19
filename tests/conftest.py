import pytest
import os
import tomllib

@pytest.fixture
def my_config(my_configfile):
    configfile = my_configfile
    with open(configfile, "rb") as f:
        config = tomllib.load(f)
    config['verbose'] = 1
    return config

@pytest.fixture
def my_configfile():
    configfile = os.path.expanduser(os.path.join('~', '.config', 'hca', 'config.toml'))
    return configfile

@pytest.fixture
def my_sample_config(my_configfile):
    with open(my_configfile, "rb") as f:
        config = tomllib.load(f)
    return config


@pytest.fixture
def my_sample_configfile():
    configfile = "../src/config_sample.toml"
    return os.path.abspath(configfile)