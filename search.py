import requests
import json
import string
import getpass
import sys
import io
import ipywidgets as widgets
import functools as ft


import time
# Importing the libraries we need to format the data in a more readable way.
import pandas as pd
import query
from pandas.io.json import json_normalize

import multiprocessing as mp
from IPython.display import display
from IPython.display import HTML
from IPython.display import clear_output
from json_methods import JSON_methods
from widget import Widget


class Search():
    def __init__(self,json_handler):
        self.topic = None
        self.search_id = None
        self.search_type = None
        self.settings_dict = {}
        self.json = None
        self.current_blob = None
        self.json_handler = json_handler
        self.relationship_person_id =[]
        self.list_of_ids = []
        self.list_of_names = []
        self.related_work_tab = None
        self.related_people_tab = None

        self.project_meta_data = None
        self.project_tab = None
        self.temp_list_of_ids = []
        self.project_names = []
        self.project_ids = []
        self.investigation_names = []
        self.investigation_ids = []
        self.study_names = []
        self.study_ids = []
        self.assay_names = []
        self.assay_ids = []
        self.data_file_names = []
        self.data_file_ids = []
        self.creator_names = []
        self.creator_ids = []
        self.submitter_names = []
        self.submitter_ids = []
        self.people_names = []
        self.people_ids = []
        self.project_members_names = []
        self.project_members_ids = []
        self.project_admins_names = []
        self.project_admins_ids = []
        self.project_asset_HK_names = []
        self.project_asset_HK_ids = []
        self.project_asset_GK_names = []
        self.project_asset_GK_ids = []
        self.project_people_names = []
        self.project_people_ids = []
        self.tab_title_names_list_doc =[]
        self.tab_title_names_list_people =[]
        self.project_tab_title_names_list =[]
        self.widget = Widget()
        self.list_of_top_level_widgets = []
        self.title = None
        self.desc = None
        self.model_name = None
        self.csv = None
        self.download_link_text = None
    def set_json_handler(self,json_handler):
        self.json_handler = json_handler
    def display(self):
        '''
        displays the file by getting the appropriate data from the JSON tags
        '''
        #File ID to search for
        id = self.search_id
        # File type
        type = self.search_type
        self.json =self.json_handler.get_JSON(type,id)
        # print(self.json)
        #title and description of file
        if self.json != []:
            self.display_basic_info()
            if type == 'Person':
                self.display_institution()
            if type == 'Data File':
                self.display_datafile()
            if type == 'Project' :
                self.display_project()
            else:
                if type != 'Person':
                    self.display_people_relations()

            self.display_work_relations()
    def display_basic_info(self):
        if self.settings_dict.get('display_title') == 'True':
            self.display_title()
        if self.settings_dict.get('display_description') == 'True':
            self.display_description()
    def display_title(self):
                # display(HTML('<h1><u>{0}</u></h1>'.format(title)))

        title = self.json_handler.get_title(self.json)
        self.title = title + '\n'
        title = ('<h1><u>{0}</u></h1>'.format(title))

        title_widget = widgets.HTML(
                       value = title
        )
        display(title_widget)

    def display_description(self):
        description = self.json_handler.get_description(self.json)
        print(description)
        self.desc = description
    def display_institution(self):
        #list of items to display
        container_list =[]
        #name of items to display
        tab_title_names_list =[]

        if self.settings_dict.get('display_project_institutions') == 'True':
            instituion_container = self.createRelationContainer('Project Institute')
            container_list.append(instituion_container)
            tab_title_names_list.append('Institution')

        #If items are to be displayed, a tab is created for each item
        if container_list:
            related_work_tab = widgets.Tab()
            related_work_tab.children = container_list
            for index in range(len(tab_title_names_list)):
                related_work_tab.set_title(index, tab_title_names_list[index])
            display(related_work_tab)
    def display_people_relations(self):
        '''
        Shows all the related Projects / Studies / Assays related to current
        working document.

        Checks settings list to see which to display, then for each item, a
        container is created with the name of each related item

        Can be optimised by using multiprocessing
        '''
        #list of items to display
        container_list =[]
        #name of items to display
        self.tab_title_names_list_people =[]

        if self.settings_dict.get('display_creators') == 'True':
            creator_relationship_people_container = self.createRelationContainer('Creator')
            container_list.append(creator_relationship_people_container)
            self.tab_title_names_list_people.append('Creator')

        if self.settings_dict.get('display_submitter') == 'True':
            submitter_relationship_people_container = self.createRelationContainer('Submitter')
            container_list.append(submitter_relationship_people_container)
            self.tab_title_names_list_people.append('Submitter')

        if self.settings_dict.get('display_related_people') == 'True':
            people_relationship_people_container = self.createRelationContainer('People')
            container_list.append(people_relationship_people_container)
            self.tab_title_names_list_people.append('Related People')

        #If items are to be displayed, a tab is created for each item
        if container_list:
            self.related_people_tab = widgets.Tab()
            self.related_people_tab.children = container_list
            for index in range(len(self.tab_title_names_list_people)):
                self.related_people_tab.set_title(index, self.tab_title_names_list_people[index])
            display(self.related_people_tab)
            self.list_of_top_level_widgets.append(self.related_people_tab)
    def display_work_relations(self):
        '''
        Shows all the related Projects / Studies / Assays related to current
        working document.

        Checks settings list to see which to display, then for each item, a
        container is created with the name of each related item

        Can be optimised by using multiprocessing
        '''
        #list of items to display
        container_list =[]
        #name of items to display
        self.tab_title_names_list_doc =[]

        if self.settings_dict.get('display_related_projects') == 'True':
            project_relationship_container = self.createRelationContainer('Project')
            container_list.append(project_relationship_container)
            self.tab_title_names_list_doc.append('Related Projects')

        if self.settings_dict.get('display_related_investigations') == 'True':
            investigation_relationship_container = self.createRelationContainer('Investigation')
            container_list.append(investigation_relationship_container)
            self.tab_title_names_list_doc.append('Related Investigations')

        if self.settings_dict.get('display_related_studies') == 'True':
            study_relationship_container = self.createRelationContainer('Study')
            container_list.append(study_relationship_container)
            self.tab_title_names_list_doc.append('Related Studies')


        if self.settings_dict.get('display_related_assays') == 'True':
            assay_relationship_container = self.createRelationContainer('Assay')
            container_list.append(assay_relationship_container)
            self.tab_title_names_list_doc.append('Related Assays')

        if self.settings_dict.get('display_related_data_files') == 'True':
            data_file_relationship_container = self.createRelationContainer('Data File')
            container_list.append(data_file_relationship_container)
            self.tab_title_names_list_doc.append('Related Data Files')

        #If items are to be displayed, a tab is created for each item
        if container_list:
            self.related_work_tab = self.widget.tab(container_list,self.tab_title_names_list_doc)
            display(self.related_work_tab)
            self.list_of_top_level_widgets.append(self.related_work_tab)
    def display_project(self):
        container_list =[]
        #name of items to display
        self.project_tab_title_names_list =[]
        if self.settings_dict.get('display_project_members') == 'True':
            project_members_container = self.createRelationContainer('Project Member')
            container_list.append(project_members_container)
            self.project_tab_title_names_list.append('Project Members')

        if self.settings_dict.get('display_project_administrators') == 'True':
            project_admin_container = self.createRelationContainer('Project Admin')
            container_list.append(project_admin_container)
            self.project_tab_title_names_list.append('Project Admins')

        if self.settings_dict.get('display_project_asset_housekeepers') == 'True':
            project_asset_HK_container = self.createRelationContainer('Asset HK')
            container_list.append(project_asset_HK_container)
            self.project_tab_title_names_list.append('Project Asset HK')

        if self.settings_dict.get('display_project_asset_gatekeepers') == 'True':
            project_asset_GK_container = self.createRelationContainer('Asset GK')
            container_list.append(project_asset_GK_container)
            self.project_tab_title_names_list.append('Project Asset GK')

        if self.settings_dict.get('display_related_people') == 'True':
            people_relationship_people_container = self.createRelationContainer('Project People')
            container_list.append(people_relationship_people_container)
            self.project_tab_title_names_list.append('Related People')

        if self.settings_dict.get('display_project_organisms') == 'True':
            project_organisms_container = self.createRelationContainer('Project Organisms')
            container_list.append(project_organisms_container)
            self.project_tab_title_names_list.append('Project Organisms')

        if self.settings_dict.get('display_project_institutions') == 'True':
            project_institute_container = self.createRelationContainer('Project Institute')
            container_list.append(project_institute_container)
            self.project_tab_title_names_list.append('Project Institutions')

        if self.settings_dict.get('display_project_programmes') == 'True':
            project_programmes_container = self.createRelationContainer('Project Program')
            container_list.append(project_programmes_container)
            self.project_tab_title_names_list.append('Project Programmes')
        #If items are to be displayed, a tab is created for each item
        if container_list:
            self.project_tab = self.widget.tab(container_list,self.project_tab_title_names_list)
            display(self.project_tab)
            self.list_of_top_level_widgets.append(self.project_tab)

    def createRelationContainer(self,type):
        '''
        Creates the container for each item to be displayed

        Each item contains a dropbox of the titles of related documents and a#
        search button

        type            : document type
        increased_width : option for increased_width
                          0 = small
                          1 = medium
                          2 = large
        '''

        #Get a dictionary of data that contains ID amnd type
        #Iterate over dictionary to get the names from IDs
        desc = ''
        increased_width = 1
        if type =='Creator':
            dict  = self.json_handler.get_relationship_creators(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.creator_names = self.getValuesOfDict(dictIDAndName)
            names = self.creator_names
            self.creator_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Name :'
            increased_width = 0
        elif type =='Submitter':
            dict  = self.json_handler.get_relationship_submitters(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.submitter_names = self.getValuesOfDict(dictIDAndName)
            names = self.submitter_names
            self.submitter_ids =self.getKeysOfDict(dictIDAndName)

            desc = 'Name :'
            increased_width = 0

        elif type =='People':
            dict  = self.json_handler.get_relationship_people(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.people_names = self.getValuesOfDict(dictIDAndName)
            names = self.people_names
            self.people_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Name :'
            increased_width = 0
        elif type == 'Project':
            dict  = self.json_handler.get_relationship_projects(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.project_names = self.getValuesOfDict(dictIDAndName)
            # print(self.project_names)
            names = self.project_names
            self.project_ids =self.getKeysOfDict(dictIDAndName)
            # print(self.project_ids)

            desc = 'Title :'
            increased_width = 2
        elif type == 'Investigation':
            dict  = self.json_handler.get_relationship_investigations(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.investigation_names = self.getValuesOfDict(dictIDAndName)
            names = self.investigation_names
            self.investigation_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 2
        elif type == 'Study':
            dict  = self.json_handler.get_relationship_studies(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.study_names = self.getValuesOfDict(dictIDAndName)
            names = self.study_names

            self.study_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 2
        elif type == 'Assay':
            dict  = self.json_handler.get_relationship_assays(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.assay_names = self.getValuesOfDict(dictIDAndName)
            names = self.assay_names

            self.assay_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 2

        elif type == 'Data File':
            dict  = self.json_handler.get_relationship_data_files(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.data_file_names = self.getValuesOfDict(dictIDAndName)
            names = self.data_file_names

            self.data_file_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 2
        elif type =='Project Member':
            dict  = self.json_handler.get_project_members(self.json)

            dictIDAndName = self.getDictOfIDandNamesPerson(dict,type)
            self.project_members_names = self.getValuesOfDict(dictIDAndName)
            names = self.project_members_names

            self.project_members_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Name :'
            increased_width = 0
        elif type =='Project Admin':
            dict  = self.json_handler.get_project_admins(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.project_admins_names = self.getValuesOfDict(dictIDAndName)
            names = self.project_admins_names

            self.project_admins_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Name :'
            increased_width = 0
        elif type =='Asset HK':
            dict  = self.json_handler.get_asset_HK(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.project_asset_HK_names = self.getValuesOfDict(dictIDAndName)
            names = self.project_asset_HK_names

            self.project_asset_HK_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Name :'
            increased_width = 0
        elif type =='Asset GK':
            dict  = self.json_handler.get_asset_GK(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.project_asset_GK_names = self.getValuesOfDict(dictIDAndName)
            names = self.project_asset_GK_names

            self.project_asset_GK_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Name :'
            increased_width = 0
        elif type =='Project Organisms':
            dict  = self.json_handler.get_organisms(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            names = self.getValuesOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 0
        elif type =='Project Institute':
            dict  = self.json_handler.get_project_institutions(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            names = self.getValuesOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 0
        elif type =='Project Program':
            dict  = self.json_handler.get_project_programmes(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            names = self.getValuesOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 0
        elif type =='Project People':
            dict  = self.json_handler.get_relationship_people(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.project_people_names = self.getValuesOfDict(dictIDAndName)
            names = self.project_people_names

            self.project_people_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Name :'
            increased_width = 0
        relationship_widget_list = []
        relationship_people_container =[]
        relation = self.relationship_drop_box(names,increased_width,desc)
        relationship_widget_list.append(relation)
        desc = 'Search'
        relation_search_button = self.widget.button_optional(desc,relation.value)
        if type == 'Project' or type =='Investigation' or type == 'Study' or type == 'Assay' or type == 'Data File':
            relation_search_button.on_click(self.on_click_search_doc)
        elif type == 'Creator' or type == 'Submitter' or type == 'People':
            relation_search_button.on_click(self.on_click_search_person)
        else:
            relation_search_button.on_click(self.on_click_search_project_meta_data)

        relationship_widget_list.append(relation_search_button)

        if type == 'Project Organisms' or type =='Project Institute' or type == 'Project Program':
            relationship_people_container = widgets.VBox([relationship_widget_list[0]])
        else :
        #Sorts positioning of container
        #dropbox above a search button

            relationship_people_container = widgets.VBox([relationship_widget_list[0], relationship_widget_list[1]])

        return relationship_people_container
    def on_click_search_doc(self,button):

        tab_index = self.related_work_tab.selected_index
        item_index = self.related_work_tab.children[tab_index].children[0].index[0]
        if self.tab_title_names_list_doc[tab_index] == 'Related Projects':
            topic = 'Document query'
            type = 'Project'
            id = self.project_ids[item_index]
        elif self.tab_title_names_list_doc[tab_index] == 'Related Investigations':
            topic = 'Document query'
            type = 'Investigation'
            id = self.investigation_ids[item_index]
        elif self.tab_title_names_list_doc[tab_index] == 'Related Studies':
            topic = 'Document query'
            type = 'Study'
            id = self.study_ids[item_index]
        elif self.tab_title_names_list_doc[tab_index] == 'Related Assays':
            topic = 'Document query'
            type = 'Assay'
            id = self.assay_ids[item_index]
        elif self.tab_title_names_list_doc[tab_index] == 'Related Data Files':
            topic = 'Document query'
            type = 'Data File'
            id = self.data_file_ids[item_index]

        # topic =
        # type =
        settings_dict = self.settings_dict
        list_of_names = self.list_of_names
        list_of_ids = self.list_of_ids
        self.search_parameters(topic,id,type,settings_dict,list_of_names,list_of_ids)
        # print(topic)
        # print(id)
        # print(type)
        self.search()
    def on_click_search_person(self,button):

        tab_index = self.related_people_tab.selected_index
        item_index = self.related_people_tab.children[tab_index].children[0].index[0]
        if self.tab_title_names_list_people[tab_index] == 'Creator':
            topic = 'Document query'
            type = 'Person'
            id = self.creator_ids[item_index]
        elif self.tab_title_names_list_people[tab_index] == 'Submitter':
            topic = 'Document query'
            type = 'Person'
            id = self.submitter_ids[item_index]
        elif self.tab_title_names_list_people[tab_index] == 'Related People':
            topic = 'Document query'
            type = 'Person'
            id = self.people_ids[item_index]
        # topic =
        # type =
        settings_dict = self.settings_dict
        list_of_names = self.list_of_names
        list_of_ids = self.list_of_ids
        self.search_parameters(topic,id,type,settings_dict,list_of_names,list_of_ids)
        self.search()
    def on_click_search_project_meta_data(self,button):

        tab_index = self.project_tab.selected_index
        item_index = self.project_tab.children[tab_index].children[0].index[0]

        if self.project_tab_title_names_list[tab_index] == 'Project Members':
            topic = 'Document query'
            type = 'Person'
            id = self.project_members_ids[item_index]
        elif self.project_tab_title_names_list[tab_index] == 'Project Admins':
            topic = 'Document query'
            type = 'Person'
            id = self.project_admins_ids[item_index]
        elif self.project_tab_title_names_list[tab_index] == 'Project Asset HK':
            topic = 'Document query'
            type = 'Person'
            id = self.project_asset_HK_ids[item_index]
        elif self.project_tab_title_names_list[tab_index] == 'Project Asset GK':
            topic = 'Document query'
            type = 'Person'
            id = self.project_asset_GK_ids[item_index]
        elif self.project_tab_title_names_list[tab_index] == 'Related People':
            topic = 'Document query'
            type = 'Person'
            id = self.project_people_ids[item_index]
        # topic =
        # type =
        settings_dict = self.settings_dict
        list_of_names = self.list_of_names
        list_of_ids = self.list_of_ids
        self.search_parameters(topic,id,type,settings_dict,list_of_names,list_of_ids)
        self.search()

    def on_click_convert(self, button):
        clear_output()

        if self.settings_dict.get('display_title') == 'True':
            if self.title is not None:
                print(self.title)
        if self.settings_dict.get('display_description') == 'True':
            if self.desc is not None:
                print(self.desc)
        if self.settings_dict.get('display_model_name') == 'True':
            if self.model_name is not None:
                print(self.model_name)
        if self.settings_dict.get('display_model') == 'True':
            if self.csv is not None:
                display(self.csv)
        if self.settings_dict.get('display_download_link') == 'True':
            if self.download_link_text is not None:
                print(self.download_link_text)
        # for index in len(self.list_of_top_level_widgets):
        #     tab_index = self.list_of_top_level_widgets[index].selected_index
        #     tab_title = self.list_of_top_level_widgets[index]._titles.get(str(tab_index))
        #     item_title = self.list_of_top_level_widgets[tab_index].children[0].value
        #     print('Query type       : {0}'.format(tab_title))
        #     print('Title of file    : {0}'.format(id))


    def getListOfNamesFromDict(self,dict,type):

        ids = []
        if type == 'Project Member':
            ids = self.iterate_over_json_list_person(dict,ids)
        else:
            ids = self.iterate_over_json_list(dict,ids)
        names = []
        for id in ids:
            name = self.list_of_names[self.list_of_ids.index(id)]
            names.append(name)
            if type == 'Creator':
                self.creator_ids.append(id)
            elif type == 'Submitter':
                self.submitter_ids.append(id)
            elif type == 'People':
                self.people_ids.append(id)
            elif type == 'Project Member':
                self.project_members.append(id)
            elif type == 'Project Admin':
                self.project_admins.append(id)
            elif type == 'Asset HK':
                self.project_asset_HK.append(id)
            elif type == 'Asset GK':
                self.project_asset_GK.append(id)
            elif type == 'Project People':
                self.project_people.append(id)

        return names

    def getKeysOfDict(self,dict):
        keys = dict.keys()
        return keys

    def getValuesOfDict(self,dict):
        values = dict.values()
        return values

    def getDictOfIDandNamesPerson(self,dict,sessionType):
        ids = []
        ids = self.iterate_over_json_list_person(dict,ids)
        # self.temp_list_of_ids = ids
        dictIDAndNames = {}

        dictIDAndNames = self.multiprocess_search(ids,sessionType)
        return dictIDAndNames
    def getDictOfIDandNames(self,dict,sessionType):
        ids = []
        ids = self.iterate_over_json_list(dict,ids)
        # self.temp_list_of_ids = ids
        dictIDAndNames = {}

        dictIDAndNames = self.multiprocess_search(ids,sessionType)
        return dictIDAndNames

    def relationship_drop_box(self,list_of_names,increased_width,desc):
        options =list_of_names
        default_value =[]
        number_of_rows = 1
        if list_of_names:
            default_value.append(options[0])
            if len(list_of_names) > 4:
                number_of_rows = 5
            else :
                number_of_rows = len(list_of_names)
                if number_of_rows < 2:
                    number_of_rows = 2

        relationship_dropdown_widget = self.widget.select_multiple(
                                                        increased_width,
                                                        options,
                                                        default_value,
                                                        number_of_rows,
                                                        desc)

        relationship_dropdown_widget.observe(self.change_made_search_related_person,names='value')
        return relationship_dropdown_widget

    def iterate_over_json_list(self,data,list_type):
        list_type.clear()

        for value in data:
            list_type.append(value.get('id'))
        return list_type

    def iterate_over_json_list_person(self,data,list_type):
        list_type.clear()

        for value in data:
            list_type.append(value.get('person_id'))
        return list_type

    def display_datafile(self):
        '''
        displays the file by getting the appropriate data from the JSON tags
        '''
        self.current_blob = self.json_handler.get_blob(self.json)
        link = self.json_handler.get_link(self.current_blob)

        if self.settings_dict.get('display_model_name') =='True':
            filename = self.json_handler.get_filename(self.current_blob)
            display(HTML('<h4>File Name: {0}</h4>'.format(filename)))
            self.model_name = filename
        # display(filename)
        if self.settings_dict.get('display_model') =='True':
            headers = { "Accept": "text/csv" }
            r = requests.get(link, headers=headers, params={'sheet':'1'})
            if r.status_code == 200:
                r.raise_for_status()
                #gets spreadsheet from data file
                csv = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
                display(csv)
                self.csv = csv
            else :
                print('Can not display file ')
                print('Reason could be : permission is not allowed ')
                print('                  file is not a excel sheet ')



        if self.settings_dict.get('display_download_link') == 'True':
            self.download_link()

    def download_link(self):
        link = self.json_handler.get_link(self.current_blob)
        filename = self.json_handler.get_filename(self.current_blob)
        download_link = link+"/download"
        print("Download link: " + download_link + "\n")
        HTML("<a href='"+ download_link + "'>Download + " + filename + "</a>")
        self.download_link_text = download_link

    def retrieve_person_name(self,idNumber,dictData,pnumber):
        personMetaData = self.json_handler.get_JSON('people',idNumber)
        if not personMetaData:
            # return personMetaData
            dictData[idNumber]=personMetaData
        else:
        # return self.json_handler.get_title(personMetaData)
            dictData[idNumber]=self.json_handler.get_title(personMetaData)

    def retrieve_project_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Project',idNumber)
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)

    def retrieve_investigation_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Investigation',idNumber)
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)

    def retrieve_study_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Study',idNumber)
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)

    def retrieve_assay_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Assay',idNumber)
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)

    def retrieve_data_file_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Data File',idNumber)
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)
    def retrieve_organism_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Project Organisms',idNumber)
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)
    def retrieve_institute_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Project Institute',idNumber)
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)
    def retrieve_program_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Project Program',idNumber)
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)
    def retrieve_project_people_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Project People',idNumber)
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)
    def multiprocess_search(self,idNumbers,sessionType):
        manager = mp.Manager()
        dict_return_data = manager.dict()
        processes = []
        # dataRec = []
        # processesBeingRun = Pool(processes = 8)
        if sessionType == 'Submitter' or sessionType == 'Creator' or sessionType == 'People':
            sessionType ='people'
        for counter in range(len(idNumbers)):
            if sessionType == 'people':
                process = mp.Process(target=self.retrieve_person_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
                # dataRec = processesBeingRun.map(self.retrieve_person_name,idNumbers)
            elif sessionType == 'Project':
                process = mp.Process(target=self.retrieve_project_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
                # dataRec = processesBeingRun.map(self.retrieve_project_name,idNumbers)
            elif sessionType == 'Investigation':
                process = mp.Process(target=self.retrieve_investigation_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
                # dataRec = processesBeingRun.map(self.retrieve_investigation_name,idNumbers)
            elif sessionType == 'Study':
                process = mp.Process(target=self.retrieve_study_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
                # dataRec = processesBeingRun.map(self.retrieve_study_name,idNumbers)
            elif sessionType == 'Assay':
                process = mp.Process(target=self.retrieve_assay_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
            elif sessionType == 'Data File':
                process = mp.Process(target=self.retrieve_data_file_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
            elif sessionType == 'Project Member':
                process = mp.Process(target=self.retrieve_person_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
            elif sessionType == 'Project Admin':
                process = mp.Process(target=self.retrieve_person_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
                # dataRec = processesBeingRun.map(self.retrieve_assay_name,idNumbers)
            elif sessionType == 'Asset HK':
                process = mp.Process(target=self.retrieve_person_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
            elif sessionType == 'Asset GK':
                process = mp.Process(target=self.retrieve_person_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
            elif sessionType == 'Project Organisms':
                process = mp.Process(target=self.retrieve_organism_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
            elif sessionType == 'Project Institute':
                process = mp.Process(target=self.retrieve_institute_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
            elif sessionType == 'Project Program':
                process = mp.Process(target=self.retrieve_program_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))
            elif sessionType == 'Project People':
                process = mp.Process(target=self.retrieve_project_people_name,
                                                  args=(idNumbers[counter],dict_return_data,counter))



            processes.append(process)
            process.start()

        for p in processes:
            p.join()
        # print(dict_return_data)
        # print(idNumbers)
        # time.sleep(10)
        # processesBeingRun.close()
        # yield processesBeingRun
        # processesBeingRun.terminate()

        return dict_return_data

    ## needs comments
    def change_made_search_related_person(self, change):
        '''
        Checks for any updates in the select multiple
        '''
        self.search_person_list = change['new']

    def search_parameters(self,topic,id ,type ,settings_dict,list_of_names,list_of_ids):
        self.creator_ids = []
        self.submitter_ids = []
        self.people_ids = []
        self.project_members = []
        self.project_admins = []
        self.project_asset_HK = []
        self.project_asset_GK = []
        self.project_people = []

        self.topic = topic
        self.search_id = id
        self.search_type = type
        self.settings_dict = settings_dict
        self.list_of_names = list_of_names
        self.list_of_ids = list_of_ids
        # print(self.topic)
        # print(self.search_id)
        # print(self.search_type)
        # time.sleep(5)

    def search(self):
        '''
        Searches Fairdom for the file based on user input
        '''
        clear_output()
        # print(self.topic)
        if self.topic == 'Document query':
            self.display()
        elif self.topic == 'Person query':
            self.display()
        elif self.topic ==  'To be implemented':
            pass

        desc = 'Convert widgets to text'
        widgets_to_text_button = self.widget.button(desc)
        widgets_to_text_button.on_click(self.on_click_convert)
        display(widgets_to_text_button)
