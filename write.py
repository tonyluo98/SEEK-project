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
from query import Query
from search import Search
from json_methods import JSON_methods

from pandas.io.json import json_normalize

from multiprocessing import Pool
from IPython.display import display
from IPython.display import HTML
from IPython.display import clear_output

# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all"
display_In_Widgets = 0;


'''
To run
x= s.SEEK()
'''
class Write():
    def __init__(self):
        pass    
    def write(self):
        pass
