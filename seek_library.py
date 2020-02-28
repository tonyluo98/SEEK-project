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
from write import Write
from json_methods import JSON_methods
from requester import Requester


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
class SEEK():
    def __init__(self):
        self.json_handler = JSON_methods()
        self.SEEK_query = None
        self.SEEK_search = None
        self.SEEK_write = None

    def query(self):
        self.SEEK_query = Query(self.json_handler)
        self.SEEK_query.query()

    def post(self):
        if self.SEEK_write == None :
            self.SEEK_write = Write(self.json_handler)
        self.SEEK_write.post_choice()

    def search(self):
        self.SEEK_search = Search(self.json_handler)

        valid = True
        list_of_names = self.SEEK_query.get_list_of_user_names()
        list_of_ids = self.SEEK_query.get_list_of_user_ids()
        topic = self.SEEK_query.get_topic()
        if topic == 'Document query' or topic == 'Person query':
            settings_dict = self.SEEK_query.get_setting_options_dict()
            settings_dict = dict(settings_dict)
            id = self.SEEK_query.get_id_to_search()
            if id == '':
                print('ID is needed')
                valid = False
            type = self.SEEK_query.get_type_to_search()
            if valid == True :
                self.SEEK_search.search_parameters(topic,id,type,settings_dict,list_of_names,list_of_ids)
                self.SEEK_search.search()
        else :
            print('Select Document/Person query tab to search')

    def change_url(self):
        print('1: https://www.fairdomhub.org')
        print('2: https://sandbox3.fairdomhub.org')
        choice = input("Please choose url 1 or 2:\n")
        print('You entered {0}'.format(choice))
        self.json_handler.change_url(choice)
        if self.SEEK_query != None:
            self.SEEK_query.set_json_handler(self.json_handler)
        if self.SEEK_search != None:
            self.SEEK_search.set_json_handler(self.json_handler)

    def auth(self):
        self.json_handler.auth_request()
        # self.SEEK_query.set_json_handler(self.json_handler)
        if self.SEEK_query != None:
            self.SEEK_query.set_json_handler(self.json_handler)
        if self.SEEK_search != None:
            self.SEEK_search.set_json_handler(self.json_handler)
        if self.SEEK_write != None:
            self.SEEK_write.set_json_handler(self.json_handler)
