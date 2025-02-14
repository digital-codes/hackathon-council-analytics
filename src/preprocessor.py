import os
import tomllib
import requests
import pymupdf
import pprint
#from tqdm import tqdm
from multiprocessing import Pool
from importlib import import_module
from typing import Optional
"""
This Module provides classes for preprocessing

Classes:
- 'Preprocessor': provide preprocessing functions


Functions:  
- 'show_config': show the configuration of the Preprocessor object
- 'process_pdf': process a file

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
    """
    A class to represent a Preprocessor.
    """

    def __init__(self, config: dict) -> None:
        """
        Constructs all the necessary attributes for the Preprocessor object.
        params: configfile: the configfile to read the configuration from

        """
        self.config = config
        _filestorage = config.get('preprocessor',{}).get('filestorage') or filestorage
        fsm = import_module(f"src.storage.{_filestorage}")
        self.fs = fsm.FileStorage(config=config)

    def show_config(self) -> str:
        """
        Print the configuration of the Preprocessor object.
        """
        pprint.pp(self.config)

    def download_pdf(self, idx: int, verbose=False) -> Optional[bytes]:
        """
        Download the PDF from the source.
        """
        #TODO: save on FileStorage could be optional
        pdf_content = self.request_pdf(idx)
        if pdf_content:
            if verbose:
                print(f"PDF {idx} downloaded from source.")
            filename = f"{idx}.pdf"
            self.fs.put_on_storage(filename,
                               pdf_content,
                               content_type="binary")
            return pdf_content
        else:
            return None

    def get_pdf(self, idx, verbose=False) -> str:
        """
        Try to get the PDF from storage, if not available download from source.
        params: idx: the index of the PDF to get
        verbose: if True, print messages
        returns: the PDF content
        """
        pdf_content = self.fs.get_from_storage(f"{idx}.pdf")
        if not pdf_content:
            if verbose:
                print(f"PDF {idx} not found in storage, downloading from source.")
            pdf_content = self.download_pdf(idx, verbose)
        return pdf_content


    def process_pdf(self, idx, verbose=False) -> bool:
        """
        Process the PDF by downloading from source, uploading to Storage, extracting text, and uploading the text file to Storage.
        """

        pdf_content = self.download_pdf(idx)

        if pdf_content:
            doc = pymupdf.open(stream=pdf_content, filetype="pdf")  # Extract text from the downloaded PDF
            text = self.extract_text(doc)
            text_filename = f"{idx}.txt"  # Save the extracted text to a local file
            self.fs.put_on_storage(text_filename, text, content_type="text")

            if verbose:
                print(f"Text extracted and saved for {filename} as {text_filename}")
            return True
        else:
            if verbose:
                print(f"Skipping text extraction for {idx} due to upload failure.")
            return False


    def request_pdf(self, idx, verbose=False) -> str:
        """
        Request the PDF file from the municipal council website.
        Returns the content of the file if it's a PDF, otherwise None.
        """
        url = f"https://www.gemeinderat.heidelberg.de/getfile.asp?id={idx}&type=do"
        response = requests.get(url, stream=True)

        content_type = response.headers.get('content-type')

        if 'application/pdf' in content_type:
            if verbose:
                print(f"PDF found for {idx}.")
            return response.content
        else:
            if verbose:
                print(f"Error: The file retrieved for id {idx} is not a PDF.")
            return None

    def extract_text(self, doc):
        text = ""
        for page in doc:
            text += page.get_text()
        return text

