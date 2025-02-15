import argparse
import os
import tomllib
import pprint
from tqdm import tqdm
from multiprocessing import Pool
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


def download(config: dict, start_id: int, end_id: Optional[int] = None, verbose=False) -> None:
    """
    Downloads the pdfs from the website and saves them to the configures File Storage
    Parameters:
        start_id (int): The start id of the pdfs to download
        end_id (int): The end id of the pdfs to download
    """
    if verbose:
        print(f"download got called with {start_id} and {end_id}")
    pp = Preprocessor(config)
    if end_id is None:
        pp.download_pdf(start_id, verbose)
    else:
        #args_list = [(i, False) for i in range(start_id, end_id)]
        #with Pool(processes=1) as p:
        #    results = list(tqdm(p.imap(pp.download_pdf, args_list), total=len(args_list)))
        #print("Process completed.")
        for idx in tqdm(range(start_id, end_id + 1), desc="Loading documents", unit="docs"):
             pp.download_pdf(idx, verbose)
            


def preprocess(config: dict, start_id: int, end_id: Optional[int] = None, verbose=False) -> None:
    """
    Download and preprocesses the pdfs and saves them to the configures File Storage
    Parameters:
        start_id (int): The start id of the pdfs to preprocess
        end_id (int): The end id of the pdfs to preprocess 
    """
    if verbose:
        print(f"preprocess got called with {start_id} and {end_id}")
    pp = Preprocessor(config)
    if end_id is None:
        pp.process_pdf(start_id, verbose)
    else:
        for idx in tqdm(range(start_id, end_id + 1), desc="Processing documents", unit="docs"):
             pp.process_pdf(idx, verbose)        
        

def embed(config: dict, start_id: int, end_id: Optional[int] = None) -> None:
    print('embed got called')


def update(config: dict, start_id: int, end_id: Optional[int] = None) -> None:
    print('update got called')

arg_template = {
    "dest": "operands",
    "type": int,
    "nargs": '+',
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
    global_parser.add_argument('--verbose', '-v', action='store_true', help='be verbose')
    show_config_parser = subparsers.add_parser('show-config', usage='use', help='show config variables')
    show_config_parser.add_argument(dest='operands', nargs='*', help='show config variables', type=str, default=None)
    show_config_parser.set_defaults(func=show_config)
    download_parser = subparsers.add_parser('download', help='download <start_id> <end_id>')
    download_parser.add_argument(**arg_template)
    download_parser.set_defaults(func=download)
    update_parser = subparsers.add_parser('update', help='update help')
    update_parser.add_argument(**arg_template)
    update_parser.set_defaults(func=update)
    preprocess_parser = subparsers.add_parser('preprocess', help='preprocess help')
    preprocess_parser.add_argument(**arg_template)
    preprocess_parser.set_defaults(func=preprocess)
    embed_parser = subparsers.add_parser('embed', help='embed help')
    embed_parser.add_argument(**arg_template)
    embed_parser.set_defaults(func=embed)

    args = global_parser.parse_args()
    if args.config:
        config = read_config(args.config)
    else:
        config = read_config(DEFAULT_CONFIGFILE)
    #TODO: set the verbose flag in config intead of passing around as parameter
    # if args.verbose:
    #     config['verbose'] = 1 #This allows to set verbosity levels later
    args.func(config, *args.operands, verbose=args.verbose)

    # if 'operands' in args and args.operands:
    #     args.func(config, *args.operands)
    # else:
    #     args.func(config=config)


if __name__ == "__main__":
    main()
