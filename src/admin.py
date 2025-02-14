import argparse
import os
import tomllib
import pprint
from preprocessor import Preprocessor
from typing import Optional

#Defaults
DEFAULT_CONFIGFILE = os.path.expanduser(os.path.join('~','.config','hca','config.toml'))

global_parser = argparse.ArgumentParser()

def show_config(config: dict,section: Optional[str]=None) -> None:
    if section is None:
        pprint.pprint(config)
    else:
        pprint.pprint(config[section])
def download(config: dict, start_id: int, end_id: Optional[int] = None) -> None:
    """
    Downloads the pdfs from the website and saves them to the configures File Storage
    Parameters:
        start_id (int): The start id of the pdfs to download
        end_id (int): The end id of the pdfs to download
    """
    print(f"download got called with {start_id} and {end_id}")
    pp = Preprocessor(config)
    pp.process_pdf()

def preprocess(config: dict, start_id: int, end_id: Optional[int] = None) -> None:
    """
    Download and preprocesses the pdfs and saves them to the configures File Storage
    Parameters:
        start_id (int): The start id of the pdfs to preprocess
        end_id (int): The end id of the pdfs to preprocess
    """
    pp = Preprocessor(config)
    if end_id is None:
        pp.process_pdf(start_id)

def extract(config: dict, start_id: int, end_id: Optional[int] = None) -> None:
    print('extract got called')


def update(config: dict, start_id: int, end_id: Optional[int] = None) -> None:
    print('update got called')

arg_template = {
    "dest": "operands",
    "type": int,
    "nargs": 2,
    "metavar": "OPERAND",
    "help": "a numeric value",
}

def read_config(configfile: str) -> dict:
    try:
        with open(configfile, "rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        raise Exception(f"missing configfile at {configfile}")
    return config


def main():
    """
    Commandline Interface for administrative Tasks
    """
    subparsers = global_parser.add_subparsers(required=True,
                                              title='subcommands',
                                              description='valid subcommands')
    global_parser.add_argument('--config', '-c', type=str, default=None, help='path to configfile')
    show_config_parser = subparsers.add_parser('show-config', usage='use', help='show config variables')
    show_config_parser.add_argument(dest='operands', nargs='*', help='show config variables', type=str, default=None)
    show_config_parser.set_defaults(func=show_config)
    download_parser = subparsers.add_parser('download', help='download <start_id> <end_id>')
    download_parser.add_argument(**arg_template)
    download_parser.set_defaults(func=download)
    parser_update = subparsers.add_parser('update', help='update help')
    parser_update.set_defaults(func=update)

    args = global_parser.parse_args()
    if args.config:
        config = read_config(args.config)
    else:
        config = read_config(DEFAULT_CONFIGFILE)

    args.func(config, *args.operands)

    # if 'operands' in args and args.operands:
    #     args.func(config, *args.operands)
    # else:
    #     args.func(config=config)


if __name__ == "__main__":
    main()