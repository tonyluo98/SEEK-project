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
class Call_Search():
    def __init__(self):
        self.SEEK_search = Search()

    def search(self,names,ids,search_topic,settings,search_id,search_type):
        valid = True
        list_of_names = names
        list_of_ids = ids
        topic = search_topic
        if topic == 'Document query' or topic == 'Person query':
            settings_dict = settings
            settings_dict = dict(settings_dict)
            id = search_id
            if id == '':
                print('ID is needed')
                valid = False
            type = search_type
            if valid == True :
                self.SEEK_search.search_parameters(topic,id,type,settings_dict,list_of_names,list_of_ids)
                self.SEEK_search.search()
