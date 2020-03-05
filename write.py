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
    '''
    Class handles posting json data to the SEEK database via FAIRDOM api
    Can either post new files or update existing ones
    '''
    def __init__(self,json_handler):
        self.json_handler = json_handler
        self.json = None
        self.widget = Widget()
        self.create_tab = None
        self.user_id = None

        self.parent_id = None
        self.post_query_container = None
        self.doc_write_compulsory_tab = None
        self.doc_write_assay_tab = None
        self.doc_write_data_file_tab = None
        self.doc_write_optional_tab = None
        self.post_accordion = None
        # self.json
        self.choice_button = None
        self.choice_confirm_button = None
        self.choice = None
        self.lock = False
    def set_json_handler(self,json_handler):
        '''
        Sets the json handler so that if there exists login details, it can be used
        '''
        self.json_handler = json_handler
    def post_choice(self):
        '''
        Displays a option menu that lets the user decide to update / create a
        file
        '''
        # Choice option toggle button
        options = ['Create','Update']
        desc = 'Type'
        val = options[0]
        self.choice_button = self.widget.toggle_with_options_button(desc,val,options)
        display(self.choice_button)
        # Confirmation button
        desc = 'Select'
        self.choice_confirm_button = self.widget.button(desc)
        self.choice_confirm_button.on_click(self.on_click_select)
        display(self.choice_confirm_button)

    def on_click_select(self,button):
        '''
        Sets the choice made by user between Create / Update
        '''
        self.choice = self.choice_button.value
        clear_output()
        if self.choice == 'Create':
            self.create()
        else :
            self.update()

    def create(self):
        '''
        Sets tab for creating a json
        '''
        self.user_id =0
        if self.user_id != None:
            desc = 'Create :'
            type = 'Create'
            self.post_tab_creation(desc,type)
            self.doc_write(type)

    def update(self):
        '''
        Sets tab for updating a json
        '''
        self.user_id =0
        if self.user_id != None:
            desc = 'Update :'
            type = 'Update'
            self.post_tab_creation(desc,type)
            self.doc_write(type)
    def post_tab_creation(self,desc,type):
        '''
        Tab to get details for the file to be uploaded / created
        '''
        tab_list = []
        title_list =[]
        post_query_widget_list= []
        desc = desc
        options = ['Investigation', 'Study', 'Assay', 'Data File']
        val = options[0]
        # widget for type of doc
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
        # Input box for ID
        # ID can either be for the current file or the parent Project file
        #           ID = updating current file
        #    Parent ID = creating new file
        id_widget = self.widget.bounded_int_text_widget(val,desc,bool,
                                                             min ,max)
        post_query_widget_list.append(id_widget)
        # extra widget for updating
        # the extra widget is used to fill the form with the current file
        # details
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
        '''
        Creates a tab that allows the user to fill the details for JSON to be
        uploaded
        '''
        tab_list = []
        title_list =[]
        accordion_widget_list = []
        vbox_widget_list = []
        # Fields that are necessary for a json to be uploaded
        self.doc_write_compulsory_tab = self.compulsory_fields()
        accordion_widget_list.append(self.doc_write_compulsory_tab)
        # Fields that are necessary for a assay json to be uploaded
        self.doc_write_assay_tab = self.assay_fields()
        accordion_widget_list.append(self.doc_write_assay_tab)
        # Fields that are necessary for a data file json to be uploaded
        self.doc_write_data_file_tab = self.data_file_fields()
        accordion_widget_list.append(self.doc_write_data_file_tab)
        # Fields that are optional
        self.doc_write_optional_tab = self.optional_fields()
        accordion_widget_list.append(self.doc_write_optional_tab)

        self.post_accordion = self.widget.accordion(accordion_widget_list,3)

        self.post_accordion.set_title(0, 'Compulsory')
        self.post_accordion.set_title(1, 'Assay options')
        self.post_accordion.set_title(2, 'Data File options')
        self.post_accordion.set_title(3, 'Optional')
        self.post_accordion.selected_index = 0
        vbox_widget_list.append(self.post_accordion)


        if type == 'Create':
            desc = 'Create'
        else :
            desc = 'Update'

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
        '''
        Fields that are compulsory for JSON file
                - Title
                - Description
        '''
        doc_write_widget_list= []

        desc = 'Title :'
        val = ''
        title_input = self.widget.text_widget(val,desc,2)
        doc_write_widget_list.append(title_input)

        desc = 'Description :'
        val = ''
        desc_input = self.widget.text_area_widget(val,desc,2)
        doc_write_widget_list.append(desc_input)


        compulsory_container = widgets.VBox([doc_write_widget_list[0],
                                             doc_write_widget_list[1]])
        return compulsory_container

    def data_file_fields(self):
        '''
        Fields that are compulsory for Data file JSON file
                - URL of data file
                - Filename
                - License

        Also allows the data file to be linked to related assays
        '''
        doc_write_widget_list= []

        desc = 'URL :'
        val = ''
        url_input = self.widget.text_widget(val,desc,2)
        doc_write_widget_list.append(url_input)

        desc = 'Filename :'
        val = ''
        filename_input = self.widget.text_widget(val,desc,2)
        doc_write_widget_list.append(filename_input)

        desc = 'Licences :'
        options = ['CC0-1.0','CC-BY-4.0','CC-BY-SA-4.0','ODC-BY-1.0','ODbL-1.0',
                   'ODC-PDDL-1.0','notspecified','other-at','other-open',
                   'other-pd','AFL-3.0','Against-DRM','CC-BY-NC-4.0','DSL',
                   'FAL-1.3','GFDL-1.3-no-cover-texts-no-invariant-sections',
                   'geogratis','hesa-withrights','localauth-withrights',
                   'MirOS','NPOSL-3.0','OGL-UK-1.0','OGL-UK-2.0','OGL-UK-3.0',
                   'OGL-Canada-2.0','OSL-3.0','dli-model-use','Talis',
                   'ukclickusepsi','ukcrown-withrights','ukpsi']
        url_input = self.widget.select(desc,options,1,4)
        doc_write_widget_list.append(url_input)

        desc = 'Assay ID :'
        val = 1
        max = sys.maxsize
        min  =1
        assay_id_input = self.widget.bounded_int_text_widget(val,desc,False,min,max)
        doc_write_widget_list.append(assay_id_input)

        desc = 'Add :'
        add_button = self.widget.button(desc)
        add_button.on_click(self.on_click_add)
        doc_write_widget_list.append(add_button)

        desc = 'Assay list:'
        int_options = []
        default_value =[]
        assay_ids_select = self.widget.select_multiple(0,int_options,default_value,3,desc)
        doc_write_widget_list.append(assay_ids_select)

        desc = 'Remove :'
        remove_button = self.widget.button(desc)
        remove_button.on_click(self.on_click_remove)
        doc_write_widget_list.append(remove_button)


        data_file_info_container = widgets.VBox([doc_write_widget_list[0],
                                                 doc_write_widget_list[1],
                                                 doc_write_widget_list[2],
                                                 doc_write_widget_list[3],
                                                 doc_write_widget_list[4],
                                                 doc_write_widget_list[5],
                                                 doc_write_widget_list[6]])
        return data_file_info_container

    def optional_fields(self):
        '''
        Optional information displayed :
                - Version number
                - Public Access setting
        '''
        doc_write_widget_list= []
        ver = ''
        desc = 'Version :'
        version_widget = self.widget.text_widget(ver,desc)
        version_widget.disabled = True
        version_widget.value = '1.0'
        doc_write_widget_list.append(version_widget)

        desc = 'Access :'
        options = ['no_access','view','download','edit','manage']
        access_widget = self.widget.select(desc,options)
        doc_write_widget_list.append(access_widget)

        optional_container = widgets.VBox([doc_write_widget_list[0],
                                           doc_write_widget_list[1]])
        return optional_container

    def check_access_chosen(self):
        access = self.doc_write_optional_tab.children[1].value
        options = ['no_access','view','download','edit','manage']
        create_doc = self.create_tab.children[0].children[0].value

        if create_doc == 'Project':
            pass
        elif create_doc == 'Investigation':
            if access != 'no_access' or access != 'view':
                access = 'view'
        elif create_doc == 'Study':
            if access != 'no_access' or access != 'view':
                access = 'view'
        elif create_doc == 'Assay':
            if access != 'no_access' or access != 'view':
                access = 'view'
        elif create_doc == 'Data File':
            if access != 'no_access' or access != 'view' or access != 'download':
                access = 'download'
        return access
    def assay_fields(self):
        '''
        Fields that are compulsory for assay JSON file
                - Title
                - Description
                - Assay Class
                - Assay Type
                - Assay Tech Type
        '''
        doc_write_widget_list= []

        desc = 'Assay Class :'
        options = ['EXP','MODEL']
        class_type_button = self.widget.toggle_with_options_button(desc,
                                                                   options[0],
                                                                   options)
        doc_write_widget_list.append(class_type_button)

        desc = 'Assay Type :'
        val = ''
        JERM_type_input = self.widget.text_widget(val,desc,2)
        doc_write_widget_list.append(JERM_type_input)


        desc = 'Tech Type :'
        val = ''
        JERM_tech_type_input = self.widget.text_widget(val,desc,2)
        doc_write_widget_list.append(JERM_tech_type_input)



        compulsory_container = widgets.VBox([doc_write_widget_list[0],
                                             doc_write_widget_list[1],
                                             doc_write_widget_list[2]])

        return compulsory_container

    def on_click_load_update(self,button):
        '''
        Load data for widgets
        '''
        type =self.post_query_container.children[0].value
        id =self.post_query_container.children[1].value
        self.json  = self.json_handler.get_JSON(type,id)

        if self.json :
            self.fill_form(type)

    def on_click_add(self,button):
        '''
        Add Assay ID to a list of assays to link
        '''
        id =self.doc_write_data_file_tab.children[3].value
        options = self.doc_write_data_file_tab.children[5].options
        # remove duplicates
        options = list(options)
        options.append(id)
        options = list(dict.fromkeys(options))
        # options.remove('None')
        self.doc_write_data_file_tab.children[5].options = options

    def on_click_remove(self,button):
        '''
        Remove Assay ID from a list of assays to link
        '''
        id =self.doc_write_data_file_tab.children[5].value
        id = list(id)
        id = id[0]
        options = self.doc_write_data_file_tab.children[5].options
        options = list(options)

        options.remove(id)
        self.doc_write_data_file_tab.children[5].options = options

    def fill_form(self,type):
        '''
        Fills widget boxes with the data from JSON downloaded
        Only used for a update function call
        '''
        self.doc_write_compulsory_tab.children[0].value =\
                                        self.json_handler.get_title(self.json)
        self.doc_write_compulsory_tab.children[1].value =\
                                        self.json_handler.get_description(self.json)
        self.doc_write_optional_tab.children[0].value =\
                                        self.json_handler.get_version(self.json)
        self.doc_write_optional_tab.children[1].value =\
                                        self.json_handler.get_public_access(self.json)

        if type == 'Data File':
            blob = self.json_handler.get_blob(self.json)
            self.doc_write_data_file_tab.children[0].value =\
                                            self.json_handler.get_url(blob)
            self.doc_write_data_file_tab.children[1].value =\
                                            self.json_handler.get_filename(blob)
            self.doc_write_data_file_tab.children[2].value =\
                                            self.json_handler.get_license(self.json)
            assays_list = self.json_handler.get_relationship_assays(self.json)
            assay_ids= self.iterate_over_json_list(assays_list)

            self.doc_write_data_file_tab.children[5].options = assay_ids
        elif type == 'Assay':
            assay_class = self.json_handler.get_assay_class(self.json)
            assay_class = assay_class.get('key')
            if assay_class == 'EXP':
                index = 0
            else :
                index =1
            self.doc_write_assay_tab.children[0].value = \
                        self.doc_write_assay_tab.children[0].options[index]
            if assay_class == 'EXP':
                assay_type = self.json_handler.get_assay_type_uri(self.json)
                # print(assay_type)
                # assay_type = assay_class.get('uri')
                self.doc_write_assay_tab.children[1].value =assay_type

                technology_type = self.json_handler.get_assay_tech_type_uri(self.json)
                # technology_type = assay_class.get('uri')
                self.doc_write_assay_tab.children[2].value =technology_type

    def on_click_post(self,button):
        '''
        Post JSON to fairdom by creating necessary hash (JSON)
        '''
        create_doc = self.create_tab.children[0].children[0].value
        id = self.create_tab.children[0].children[1].value
        title = self.doc_write_tab.children[0].children[0].children[0].children[0].value
        desc = self.doc_write_tab.children[0].children[0].children[0].children[1].value
        url = self.doc_write_data_file_tab.children[0].value
        filename =self.doc_write_data_file_tab.children[1].value
        license = self.doc_write_data_file_tab.children[2].value
        access = self.doc_write_optional_tab.children[1].value
        access = self.check_access_chosen()
        if self.choice == 'Update':
            current_id = str(id)
            id = self.get_parent_id()
        valid = True
        if title == '':
            valid = False
            print('Title can not be left empty')

        # if create_doc == 'Data File':
        #     if url == '':
        #         valid = False
        #         print('URL can not be left empty')
        #     if filename == '':
        #         valid = False
        #         print('Filename can not be left empty')

        if valid == True:
            if create_doc == 'Project':
                pass
            elif create_doc == 'Investigation':
                hash = self.investigation_hash(title,desc,access,id)
                type = 'Investigation'
            elif create_doc == 'Study':
                type = 'Study'
                hash = self.study_hash(title,desc,access,id)
            elif create_doc == 'Assay':
                assay_class = self.doc_write_assay_tab.children[0].value
                assay_type = self.doc_write_assay_tab.children[1].value
                assay_tech_type = self.doc_write_assay_tab.children[2].value
                type = 'Assay'
                hash = self.assay_hash(title,desc,access,id,assay_class,
                                       assay_type,assay_tech_type)
            elif create_doc == 'Data File':
                type = 'Data File'
                hash = self.data_file_hash(title,desc,access,id,license,url,filename)
            if self.choice == 'Update':
                id_returned = self.json_handler.post_json(type,hash,self.choice,current_id)
            else :
                id_returned = self.json_handler.post_json(type,hash,self.choice)
            if id_returned != None:
                if create_doc =='Data File':
                    self.link_data_files_to_assays(id_returned)


        # print(id)
    def get_parent_id(self):
        '''
        Used in updating
        Gets the parent ID that the file is linked to
        '''
        doc_type = self.json_handler.get_type(self.json)
        if doc_type == 'investigations':
            parent_dict = self.json_handler.get_relationship_projects(self.json)
        elif doc_type == 'studies':
            parent_dict = self.json_handler.get_relationship_investigations(self.json)
        elif doc_type == 'assays':
            parent_dict = self.json_handler.get_relationship_studies(self.json)
        elif doc_type == 'data_files':
            parent_dict = self.json_handler.get_relationship_projects(self.json)
        id = self.iterate_over_json_list(parent_dict)
        return id

    def iterate_over_json_list(self,data):
        '''
        Gets list of dictionary keys
        '''
        ids = []
        for value in data:
            ids.append(value.get('id'))
        return ids

    def get_user_id(self):
        '''
        Gets user ID
        NOT IMPLEMENTED FOR CURRENT VERSION OF API
        '''
        self.user_id = self.json_handler.get_user_id()
        if user_id == {}:
            self.user_id = None
            print('Need Correct login details')

    def investigation_hash(self,title,desc,access,id):
        '''
        JSON for Investigation
        '''
        type = 'Investigation'
        investigation = {}
        investigation['data'] = {}
        investigation['data']['type'] = 'investigations'
        investigation['data']['attributes'] = {}
        investigation['data']['attributes']['title'] = title
        investigation['data']['attributes']['description'] = desc
        investigation['data']['attributes']['policy']= {}

        investigation['data']['attributes']['policy']['access'] = access
        investigation['data']['relationships'] = {}
        investigation['data']['relationships']['projects'] = {}
        investigation['data']['relationships']['projects']['data'] = [{'id' : id, 'type' : 'projects'}]
        # id = self.json_handler.post_json(type,investigation)
        return investigation

    def study_hash(self,title,desc,access,id):
        '''
        JSON for Study
        '''
        type = 'Study'
        study = {}
        study['data'] = {}
        study['data']['type'] = 'studies'
        study['data']['attributes'] = {}
        study['data']['attributes']['title'] = title
        study['data']['attributes']['description'] =desc
        study['data']['attributes']['policy']= {}

        study['data']['attributes']['policy']['access'] = access
        # study['data']['attributes']['policy'] = {'access':'view', 'permissions': [{'resource': {'id': '1','type': 'people'},'access': 'manage'}]}
        study['data']['relationships'] = {}
        study['data']['relationships']['investigation'] = {}
        study['data']['relationships']['investigation']['data'] = {'id' : id, 'type' : 'investigations'}
        # id = self.json_handler.post_json(type,study)
        return study

    def assay_hash(self,title,desc,access,id,assay_class,assay_type,assay_tech_type):
        '''
        JSON for Assay
        '''
        type = 'Assay'
        assay = {}
        assay['data'] = {}
        assay['data']['type'] = 'assays'
        assay['data']['attributes'] = {}
        assay['data']['attributes']['title'] = title
        assay['data']['attributes']['description'] =desc
        assay['data']['attributes']['policy']= {}
        assay['data']['attributes']['policy']['access'] = access
        assay['data']['attributes']['assay_class'] = {}
        assay['data']['attributes']['assay_class']['key'] = assay_class
        if assay_class == 'EXP':
            assay['data']['attributes']['assay_type'] = {}
            assay['data']['attributes']['assay_type']['uri'] = assay_type
            assay['data']['attributes']['technology_type'] = {}
            assay['data']['attributes']['technology_type']['uri'] = assay_tech_type
        assay['data']['relationships'] = {}
        assay['data']['relationships']['study'] = {}
        assay['data']['relationships']['study']['data'] = {'id' : id, 'type' : 'studies'}
        # id = self.json_handler.post_json(type,assay)
        return assay

    def data_file_hash(self,title,desc,access,id,license,url,filename):
        '''
        JSON for Data File
        '''
        data_file = {}
        data_file['data'] = {}
        data_file['data']['type'] = 'data_files'
        data_file['data']['attributes'] = {}
        data_file['data']['attributes']['title'] = title
        data_file['data']['attributes']['description'] =desc
        data_file['data']['attributes']['license'] = license
        data_file['data']['attributes']['policy']= {}
        data_file['data']['attributes']['policy']['access'] = access
        data_file['data']['relationships'] = {}
        data_file['data']['relationships']['projects'] = {}
        data_file['data']['relationships']['projects']['data'] = [{'id' : id, 'type' : 'projects'}]

        remote_blob = {'url' : url, 'original_filename':filename}
        data_file['data']['attributes']['content_blobs'] = [remote_blob]
        return(data_file)

    def link_data_files_to_assays(self,id):
        '''
        Updates the JSON for Assays to include a relation to data file uploaded
        '''
        # list of assay ids to link
        assay_ids = self.doc_write_data_file_tab.children[5].options
        # for each id , update the JSON
        for item in assay_ids:
            assay_json = self.json_handler.get_JSON('Assay',item)
            assay_data_files =  self.json_handler.get_relationship_data_files(assay_json)
            id_list = self.iterate_over_json_list(assay_data_files)
            # Create a dict so that it can check if that id already exists
            id_dict = {id_list[item_ID]: 'id' for item_ID in range(0, len(id_list))}
            assay = {}
            assay['data'] = {}
            assay['data']['type'] = 'assays'
            assay['data']['relationships'] = {}
            assay['data']['relationships']['data_files'] = {}
            if item not in id_dict:
                new_relation_data_file = {}
                new_relation_data_file = {'id' : id, 'type' : 'data_files'}
                assay_data_files.append(new_relation_data_file)
                assay['data']['relationships']['data_files']['data'] = assay_data_files
                id_returned = self.json_handler.post_json('Assay',assay,'Update',str(item))
