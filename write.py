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
        self.option_button = None
        self.write()
    def write(self):
        desc = 'Method :'
        val = 'Create'
        options = ['Create','Update']
        self.option_button = self.widget.toggle_button(desc,val,options)
        

        title = 'test: 1 via api'
        desc = 'test 1 via api at making a investigation'
        id = 3
        id = self.investigation_hash(title,desc,id)
        title = 'test: 1 via api'
        desc = 'test 1 via api at making a study'
        id = self.study_hash(title,desc,id)
        title = 'test: 1 via api'
        desc = 'test 1 via api at making a assay'
        id = self.assay_hash(title,desc,id)

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
