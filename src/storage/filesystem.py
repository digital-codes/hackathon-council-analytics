import os
"""
This module gets imported by the preprocessor when filestorage is configured as 'filesystem'

Example:
 
     >>>> set filestorage=filesystem
     >>>> set path ='folder'
     >>>> import preprocessor
     >>>> pp = preprocessor(configfile)
     >>>> pp.fs.get_from_storage('filename')
     True
"""

class FileStorage:
    """
    This class contains methods for storing and retrieving files from the file system
    """

    def __init__(self,config):
        try:
            self.path = config['filestorage']['path']
        except KeyError:
            raise Exception("A path configuration is required")

    def get_from_storage(self,filename):
        """
        This method retrieves a file from the filesystem
        """
        basename,filetype = os.path.splitext(filename)
        if filetype == '.pdf':
            readtype = 'rb'
        else:
            readtype = 'r'
        file = os.path.join(self.path,filename)
        if not os.path.isfile(file):
            return None
        else:
            with open(file, readtype) as f:
                return f.read()


    def put_on_storage(self,filename,content, content_type="binary") -> bool:
        """
        This method stores a file in the filesystem
        """
        if content_type == 'binary':
            write_type = 'wb'
        else:
            write_type = 'w'
        with open(os.path.join(self.path,filename),write_type) as f:
            f.write(content)
        return True
