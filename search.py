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
from json_methods import JSON_methods


class Search():
    def __init__(self):
        self.topic = None
        self.search_id = None
        self.search_type = None
        self.settings_dict = {}
        self.json = None
        self.current_blob = None
        self.json_handler = JSON_methods()
        self.relationship_person_id =[]
        self.list_of_ids = []
        self.list_of_names = []


    def display_doc(self):
        '''
        displays the file by getting the appropriate data from the JSON tags
        '''
        #File ID to search for
        id = self.search_id
        # File type
        type = self.search_type
        self.json =self.json_handler.get_JSON(type,id,'None')
        # print(self.json)
        #title and description of file
        if self.json != []:
            if self.settings_dict.get('display_title') == 'Yes':
                self.display_title()

            if self.settings_dict.get('display_description') == 'Yes':
                self.display_description()

            if type == 'Data File':
                self.display_datafile()

            if self.settings_dict.get('display_creators') == 'Yes':
                self.display_creator()
    def display_title(self):
                # display(HTML('<h1><u>{0}</u></h1>'.format(title)))

        title = self.json_handler.get_title(self.json)
        title = ('<h1><u>{0}</u></h1>'.format(title))

        title_widget = widgets.HTML(
                       value = title
        )
        display(title_widget)

    def display_description(self):
        description = self.json_handler.get_description(self.json)
        print(description)
    def display_creator(self):
        creatorsDict  = self.json_handler.get_relationship_creators(self.json)
        creator_names = self.getListOfNamesFromDict(creatorsDict)

        creator_relation = self.relationship_drop_box(creator_names)
        creator_relation_people_search_button = self.createRelationSearchWidget(creator_relation.value)
        creator_relationship_widget_list  = [
            creator_relation,
            creator_relation_people_search_button
                        ]
        creator_relationship_people_container = widgets.VBox([creator_relationship_widget_list[0], creator_relationship_widget_list[1]])

        submittersDict  = self.json_handler.get_relationship_submitters(self.json)
        submitter_names = self.getListOfNamesFromDict(submittersDict)

        submitter_relation = self.relationship_drop_box(submitter_names)
        submitter_relation_people_search_button = self.createRelationSearchWidget(submitter_relation.value)
        submitter_relationship_widget_list  = [
            submitter_relation,
            submitter_relation_people_search_button
                        ]
        submitter_relationship_people_container = widgets.VBox([submitter_relationship_widget_list[0], submitter_relationship_widget_list[1]])

        peopleDict  = self.json_handler.get_relationship_people(self.json)
        people_names = self.getListOfNamesFromDict(submittersDict)

        people_relation = self.relationship_drop_box(people_names)
        people_relation_people_search_button = self.createRelationSearchWidget(people_relation.value)
        people_relationship_widget_list  = [
            people_relation,
            people_relation_people_search_button
                        ]
        people_relationship_people_container = widgets.VBox([people_relationship_widget_list[0], people_relationship_widget_list[1]])

        related_info_tab = widgets.Tab()
        related_info_tab.children =[creator_relationship_people_container,
                                    submitter_relationship_people_container,
                                    people_relationship_people_container]
        related_info_tab.set_title(0, 'Creators')
        related_info_tab.set_title(1, 'Submitter')
        related_info_tab.set_title(2, 'People')



        # relation_people_search_button.on_click(self.related_people_search)
        display(related_info_tab)
    def createRelationSearchWidget(self,value):
        if len(value) == 0 :
            boolean = True
        else:
            boolean = False
        search_button = widgets.Button(
            description='Search',
            disabled=boolean,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
        )
        return search_button

    def getListOfNamesFromDict(self,dict):
        ids = []
        ids = self.iterate_over_json_list(dict,ids)
        names = []
        for id in ids:
            name = self.list_of_names[self.list_of_ids.index(id)]
            names.append(name)
        return names

    def relationship_drop_box(self,list_of_names):
        x =list_of_names
        default_value =[]
        number_of_rows = 1
        if list_of_names:
            default_value.append(x[0])
            if len(list_of_names) > 3:
                number_of_rows = 3
            else :
                number_of_rows = len(list_of_names)
        relationship_dropdown_widget = widgets.SelectMultiple(
            options=x,
            value=default_value,
            rows=number_of_rows,
            description='Person ID',
            disabled=False
        )
        relationship_dropdown_widget.observe(self.change_made_search_related_person,names='value')
        return relationship_dropdown_widget


    def iterate_over_json_list(self,data,list_type):
        list_type.clear()
        for value in data:
            list_type.append(value.get('id'))
        return list_type

    def display_datafile(self):
        '''
        displays the file by getting the appropriate data from the JSON tags
        '''
        self.current_blob = self.json_handler.get_blob(self.json)
        link = self.json_handler.get_link(self.current_blob)

        if self.settings_dict.get('display_model_name') =='Yes':
            filename = self.json_handler.get_filename(self.current_blob)
            display(HTML('<h4>File Name: {0}</h4>'.format(filename)))
        # display(filename)
        if self.settings_dict.get('display_model') =='Yes':
            headers = { "Accept": "text/csv" }
            r = requests.get(link, headers=headers, params={'sheet':'1'})
            r.raise_for_status()
            #gets spreadsheet from data file
            csv = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
            display(csv)

        if self.settings_dict.get('display_download_link') == 'Yes':
            self.download_link()

    def download_link(self):
        link = self.json_handler.get_link(self.current_blob)
        filename = self.json_handler.get_filename(self.current_blob)
        download_link = link+"/download"
        print("Download link: " + download_link + "\n")
        HTML("<a href='"+ download_link + "'>Download + " + filename + "</a>")

    def multiprocess_search(self,idNumbers):

        processesBeingRun = Pool(processes = 15)
        dataRec = processesBeingRun.map(self.retrieve_person_name,idNumbers)

        processesBeingRun.close()
        return dataRec

    def retrieve_person_name(self,idNumber):
        personMetaData = self.json_handler.get_JSON('people',idNumber)
        return self.json_handler.get_title(personMetaData)

    ## needs comments
    def change_made_search_related_person(self, change):
        '''
        Checks for any updates in the select multiple
        '''
        self.search_person_list = change['new']

    def search_parameters(self,topic,id ,type ,settings_dict,list_of_names,list_of_ids):
        self.topic = topic
        self.search_id = id
        self.search_type = type
        self.settings_dict = settings_dict
        self.list_of_names = list_of_names
        self.list_of_ids = list_of_ids


    def search(self):
        '''
        Searches Fairdom for the file based on user input
        '''
        clear_output()
        # print(self.topic)
        if self.topic == 'Document query':
            self.display_doc()
        elif self.topic == 'Person query':
            pass
        elif self.topic ==  'To be implemented':
            pass
