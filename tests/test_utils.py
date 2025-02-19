import sys

sys.path.append("../src")

from utils import vprint
def test_vprint():
    config = {'verbose': 1}
    vprint("test print", config)  # should print
    config['verbose'] = 0
    vprint("test no print", config) # should not print
    assert True
