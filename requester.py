import requests
import json
import string
import getpass
import sys
import io
import ipywidgets as widgets
import functools as ft

# Importing the libraries we need to format the data in a more readable way.
import pandas as pd
import query
from pandas.io.json import json_normalize

from multiprocessing import Pool
from IPython.display import display
from IPython.display import HTML
from IPython.display import clear_output



class requester():
    '''
    Functions that associate with JSON data
    '''
    def __init__(self,auth = None):
        self.headers  = {"Accept": "application/vnd.api+json",
                         "Connection": "close",
                         "Accept-Charset": "ISO-8859-1"}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.auth = auth

    def auth_request(self):
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.auth = (input('Username:'), getpass.getpass('Password'))
