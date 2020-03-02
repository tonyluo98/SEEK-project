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
        self.json = None
        self.widget = Widget()
        self.create_tab = None
        self.user_id = None

        self.parent_id = None
        self.post_query_container = None
        self.doc_write_compulsory_tab = None
        self.doc_write_optional_tab = None

        self.post_accordion = None
        # self.json
        self.choice_button = None
        self.choice_confirm_button = None
        self.choice = None
    def post_choice(self):
        options = ['Create','Update']
        desc = 'Type'
        val = options[0]
        self.choice_button = self.widget.toggle_with_options_button(desc,val,options)
        display(self.choice_button)
        desc = 'Select'
        self.choice_confirm_button = self.widget.button(desc)
        self.choice_confirm_button.on_click(self.on_click_select)
        display(self.choice_confirm_button)


    def on_click_select(self,button):
        self.choice = self.choice_button.value
        clear_output()
        if self.choice == 'Create':
            self.create()
        else :
            self.update()

    def create(self):
        # self.get_user_id()

        self.user_id =0
        if self.user_id != None:
            desc = 'Create :'
            type = 'Create'

            self.post_tab_creation(desc,type)
            self.doc_write(type)

    def update(self):
        # self.get_user_id()

        self.user_id =0
        if self.user_id != None:
            desc = 'Update :'
            type = 'Update'
            self.post_tab_creation(desc,type)

            self.doc_write(type)

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
    def post_tab_creation(self,desc,type):
        tab_list = []
        title_list =[]
        post_query_widget_list= []
        desc = desc
        options = ['Project', 'Investigation', 'Study', 'Assay', 'Data File']
        val = options[0]
        create_options_dropdown = self.widget.dropdown_widget(
                                                 options,val,desc)
        post_query_widget_list.append(create_options_dropdown)

        if type == 'Create':
            desc = 'Parent ID :'
        else :
            desc = 'ID :'
        bool = False
        min=1
        max = sys.maxsize
        val = min
        parent_id_widget = self.widget.bounded_int_text_widget(val,desc,bool,
                                                             min ,max)
        post_query_widget_list.append(parent_id_widget)
        if type == 'Create':
            self.post_query_container = widgets.VBox([post_query_widget_list[0],
                                                      post_query_widget_list[1]])
        else :
            desc = 'Load details'
            load_button = self.widget.button(desc)
            load_button.on_click(self.on_click_load_update)
            post_query_widget_list.append(load_button)
            #Formats the widgets into a column
            self.post_query_container = widgets.VBox([post_query_widget_list[0],
                                                      post_query_widget_list[1],
                                                      post_query_widget_list[2]])
        tab_list.append(self.post_query_container)
        title_list.append('Post details')
        self.create_tab = self.widget.tab(tab_list,title_list)
        display(self.create_tab)

    def doc_write(self,type):
        tab_list = []
        title_list =[]
        accordion_widget_list = []
        vbox_widget_list = []
        self.doc_write_compulsory_tab = self.compulsory_fields()
        accordion_widget_list.append(self.doc_write_compulsory_tab)

        if type == 'Update':
            self.doc_write_optional_tab = self.optional_fields()
            accordion_widget_list.append(self.doc_write_optional_tab)

        self.post_accordion = self.widget.accordion(accordion_widget_list,3)

        self.post_accordion.set_title(0, 'Compulsory')
        self.post_accordion.selected_index = 0
        vbox_widget_list.append(self.post_accordion)

        if type == 'Create':
            desc = 'Create'
        else :
            desc = 'Update'
            self.post_accordion.set_title(1, 'Optional')


        post_button = self.widget.button(desc)
        post_button.on_click(self.on_click_post)

        vbox_widget_list.append(post_button)
        doc_container= widgets.VBox([vbox_widget_list[0],
                                     vbox_widget_list[1]])
        tab_list.append(doc_container)
        title_list.append('Document Details')
        self.doc_write_tab = self.widget.tab(tab_list,title_list)
        display(self.doc_write_tab)

    def compulsory_fields(self):
        doc_write_widget_list= []

        desc = 'Title :'
        val = ''
        title_input = self.widget.text_widget(val,desc,2)
        doc_write_widget_list.append(title_input)

        desc = 'Description :'
        val = ''
        desc_input = self.widget.text_area_widget(val,desc,2)
        doc_write_widget_list.append(desc_input)

        # desc = 'Post'
        # post_button = self.widget.button(desc)
        # post_button.on_click(self.on_click_post)
        # doc_write_widget_list.append(post_button)

        compulsory_container = widgets.VBox([doc_write_widget_list[0],
                                             doc_write_widget_list[1]])
        return compulsory_container

    def optional_fields(self):
        doc_write_widget_list= []

        ver = ''
        version = ('<h1><u>Version : {0}</u></h1>'.format(ver))
        version_widget = widgets.HTML(
                       value = version
        )
        doc_write_widget_list.append(version_widget)

        optional_container = widgets.VBox([doc_write_widget_list[0]])
        return optional_container

    def on_click_load_update(self,button):
        type =self.post_query_container.children[0].value
        id =self.post_query_container.children[1].value
        self.json  = self.json_handler.get_JSON(type,id)

        if self.json :
            self.fill_form()

    def fill_form(self):
        self.doc_write_compulsory_tab.children[0].value =\
                                        self.json_handler.get_title(self.json)
        self.doc_write_compulsory_tab.children[1].value =\
                                        self.json_handler.get_description(self.json)
        self.doc_write_optional_tab.children[0].value =\
                                        self.json_handler.get_version(self.json)
    def on_click_post(self,button):
        create_doc = self.create_tab.children[0].children[0].value
        id = self.create_tab.children[0].children[1].value
        title = self.doc_write_tab.children[0].children[0].children[0].children[0].value
        desc = self.doc_write_tab.children[0].children[0].children[0].children[1].value

        if self.choice == 'Update':
            current_id = str(id)
            id = self.get_parent_id()
        if title == '':
            print('Title can not be left empty')
        else:
            if create_doc == 'Project':
                pass
            elif create_doc == 'Investigation':
                hash = self.investigation_hash(title,desc,id)
                type = 'Investigation'
            elif create_doc == 'Study':
                type = 'Study'
                hash = self.study_hash(title,desc,id)
            elif create_doc == 'Assay':
                type = 'Assay'
                hash = self.assay_hash(title,desc,id)
            if self.choice == 'Update':
                id_returned = self.json_handler.post_json(type,hash,self.choice,current_id)
            else :
                id_returned = self.json_handler.post_json(type,hash,self.choice)



        # print(id)
    def get_parent_id(self):
        doc_type = self.json_handler.get_type(self.json)
        if doc_type == 'investigations':
            parent_dict = self.json_handler.get_relationship_projects(self.json)
        elif doc_type == 'studies':
            parent_dict = self.json_handler.get_relationship_investigations(self.json)
        elif doc_type == 'assays':
            parent_dict = self.json_handler.get_relationship_studies(self.json)
        id = self.iterate_over_json_list(parent_dict)
        return id

    def iterate_over_json_list(self,data):
        for value in data:
            id = value.get('id')
        return id

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
        # id = self.json_handler.post_json(type,investigation)
        return investigation

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
        # id = self.json_handler.post_json(type,study)
        return study

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
        # id = self.json_handler.post_json(type,assay)
        return assay
