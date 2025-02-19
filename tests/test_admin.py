import sys
sys.path.append("..")
import src.admin as admin
def test_download():
    admin.download(5,6)
    assert False
