import sys

sys.path.append("../src")

from preprocessor import Preprocessor


def test_preprocessor(my_config):
    pp = Preprocessor(my_config)
    assert type(pp).__name__ == 'Preprocessor'


def test_preprocessor_config(my_config):
    pp = Preprocessor(my_config)
    pp.show_config()
    assert type(pp).__name__ == 'Preprocessor'


def test_filestorage(my_config):
    pp = Preprocessor(my_config)
    fs = pp.fs
    assert type(fs).__name__ == "FileStorage"


def test_request_pdf(my_config):
    pp = Preprocessor(my_config)
    result = pp.request_pdf(367896, verbose=True)  # 36777896 is the ID of the PDF in the database
    assert result


def test_get_pdf(my_config):
    pp = Preprocessor(my_config)
    result = pp.get_pdf(367896, verbose=True)
    assert result


def test_process_pdf(my_config):
    pp = Preprocessor(my_config)
    result = pp.process_pdf(367896, verbose=True)
    assert result


