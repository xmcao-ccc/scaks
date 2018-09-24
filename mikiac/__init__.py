import time
import sys

from .functions import *
from .errors.error import *
from .compatutil import pickle


__version__ = '1.0.0'

file_header = (
    '# This file was automatically generated by MiKiAC' +
    ' (https://github.com/PytLab/mikiac).\n' +
    '# Version %s\n# Date: %s \n#\n' +
    '# Do not make changes to this file ' +
    'unless you know what you are doing\n\n') % (__version__, time.asctime())

#-------------------------------------------------------
# Some base classes for kinetic model are defined below |
#-------------------------------------------------------


class ModelShell(object):
    """
    A non-functional parent class to be inherited by
    other tools class of kinetic model.
    """

    def __init__(self, owner):
        self._owner = owner
        self._archived_data_dict = {}

    def archive_data(self, data_name, data):
        """
        Update data dict and dump it to data file.

        :param data_name: key in data dict
        :type data_name: str

        :param data: value in data dict
        :type data: any
        """
        # Update data dict.
        if data_name in self._owner.archived_variables:
            self._archived_data_dict[data_name] = data
            # Dump data dict to data file
            if self._archived_data_dict:
                with open(self._owner.data_file, 'wb') as f:
                    pickle.dump(self._archived_data_dict, f)

    @staticmethod
    def write2file(filename, line):
        f = open(filename, 'a')
        f.write(line)
        f.close()

