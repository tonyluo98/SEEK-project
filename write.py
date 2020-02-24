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
from widget import Widget

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
    def __init__(self,json_handler):
        self.json_handler = json_handler
        self.widget = Widget()
        self.create_tab = None
        self.user_id = None

        self.parent_id = None
        self.post_query_container = None
        self.doc_write_tab = None
    def create(self):
        # self.get_user_id()

        self.user_id =0
        if self.user_id != None:
            self.create_tab_creation()
            self.doc_write()

        # title = 'test: 1 via api'
        # desc = 'test 1 via api at making a investigation'
        # id = 2
        # id = self.investigation_hash(title,desc,id)
        # title = 'test: 1 via api'
        # desc = 'test 1 via api at making a study'
        # id = self.study_hash(title,desc,id)
        # title = 'test: 1 via api'
        # desc = 'test 1 via api at making a assay'
        # id = self.assay_hash(title,desc,id)
    def create_tab_creation(self):
        tab_list = []
        title_list =[]
        post_query_widget_list= []
        desc = 'Create :'
        options = ['Project', 'Investigation', 'Study', 'Assay', 'Data File']
        val = options[0]
        create_options_dropdown = self.widget.dropdown_widget(
                                                 options,val,desc)
        post_query_widget_list.append(create_options_dropdown)

        desc = 'Parent ID :'
        bool = False
        min=1
        max = sys.maxsize
        val = min
        parent_id_widget = self.widget.bounded_int_text_widget(val,desc,bool,
                                                             min ,max)
        post_query_widget_list.append(parent_id_widget)
        desc = 'Load details'
        load_button = self.widget.button(desc)
        load_button.on_click(self.on_click_load)
        post_query_widget_list.append(load_button)
        #Formats the widgets into a column
        self.post_query_container = widgets.VBox([post_query_widget_list[0],
                                                  post_query_widget_list[1],
                                                  post_query_widget_list[2]])
        tab_list.append(self.post_query_container)
        title_list.append('Post details')
        self.create_tab = self.widget.tab(tab_list,title_list)
        display(self.create_tab)

    def doc_write(self):
        tab_list = []
        title_list =[]
        doc_write_widget_list= []

        desc = 'Title :'
        val = ''
        title_input = self.widget.text_widget(val,desc)
        doc_write_widget_list.append(title_input)

        desc = 'Description :'
        val = ''
        desc_input = self.widget.text_area_widget(val,desc)
        doc_write_widget_list.append(desc_input)

        desc = 'Post'
        post_button = self.widget.button(desc)
        post_button.on_click(self.on_click_post)
        doc_write_widget_list.append(post_button)

        self.doc_write_container = widgets.VBox([doc_write_widget_list[0],
                                                 doc_write_widget_list[1],
                                                 doc_write_widget_list[2]])
        tab_list.append(self.doc_write_container)
        title_list.append('Document Details')
        self.doc_write_tab = self.widget.tab(tab_list,title_list)
        display(self.doc_write_tab)

    def on_click_load(self,button):
        pass

    def on_click_post(self,button):
        create_doc = self.create_tab.children[0].children[0].value
        parent_id = self.create_tab.children[0].children[1].value
        title = self.doc_write_tab.children[0].children[0].value
        desc = self.doc_write_tab.children[0].children[1].value


        id = self.investigation_hash(title,desc,parent_id)
        # print(id)

    def get_user_id(self):
        self.user_id = self.json_handler.get_user_id()
        if user_id == {}:
            self.user_id = None
            print('Need Correct login details')

    def investigation_hash(self,title,desc,id):
        type = 'Investigation'
        investigation = {}
        investigation['data'] = {}
        investigation['data']['type'] = 'investigations'
        investigation['data']['attributes'] = {}
        investigation['data']['attributes']['title'] = title
        investigation['data']['attributes']['description'] = desc
        investigation['data']['relationships'] = {}
        investigation['data']['relationships']['projects'] = {}
        investigation['data']['relationships']['projects']['data'] = [{'id' : id, 'type' : 'projects'}]
        id = self.json_handler.post_json(type,investigation)
        return id

    def study_hash(self,title,desc,id):
        type = 'Study'
        study = {}
        study['data'] = {}
        study['data']['type'] = 'studies'
        study['data']['attributes'] = {}
        study['data']['attributes']['title'] = title
        study['data']['attributes']['description'] =desc
        study['data']['attributes']['policy'] = {'access':'view', 'permissions': [{'resource': {'id': '1','type': 'people'},'access': 'manage'}]}
        study['data']['relationships'] = {}
        study['data']['relationships']['investigation'] = {}
        study['data']['relationships']['investigation']['data'] = {'id' : id, 'type' : 'investigations'}
        id = self.json_handler.post_json(type,study)
        return id

    def assay_hash(self,title,desc,id):
        type = 'Assay'
        assay = {}
        assay['data'] = {}
        assay['data']['type'] = 'assays'
        assay['data']['attributes'] = {}
        assay['data']['attributes']['title'] = title
        assay['data']['attributes']['description'] =desc
        assay['data']['attributes']['policy'] = {'access':'view', 'permissions': []}
        assay['data']['attributes']['assay_class'] = {'key' : 'EXP'}
        assay['data']['attributes']['assay_type'] = {'uri' : 'http://jermontology.org/ontology/JERMOntology#Metabolomics'}
        assay['data']['attributes']['technology_type'] = {'uri' : 'http://jermontology.org/ontology/JERMOntology#Electrophoresis'}
        assay['data']['relationships'] = {}
        assay['data']['relationships']['study'] = {}
        assay['data']['relationships']['study']['data'] = {'id' : id, 'type' : 'studies'}
        id = self.json_handler.post_json(type,assay)
        return id
