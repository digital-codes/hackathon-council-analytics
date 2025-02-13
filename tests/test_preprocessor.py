import sys
sys.path.append("..") 

from src.preprocessor import Preprocessor


def test_preprocessor():
	pp = Preprocessor()
	assert type(pp).__name__ == 'Preprocessor'
