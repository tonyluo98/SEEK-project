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
        self.related_work_tab = None
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
        self.tab_title_names_list =[]
        self.project_tab_title_names_list =[]


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
            if type == 'Project' :
                self.display_project()
            else:
                self.display_people_relations()

            self.display_work_relations()

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
        tab_title_names_list =[]

        if self.settings_dict.get('display_creators') == 'Yes':
            creator_relationship_people_container = self.createRelationContainer('Creator','No')
            container_list.append(creator_relationship_people_container)
            tab_title_names_list.append('Creator')

        if self.settings_dict.get('display_submitter') == 'Yes':
            submitter_relationship_people_container = self.createRelationContainer('Submitter','No')
            container_list.append(submitter_relationship_people_container)
            tab_title_names_list.append('Submitter')

        if self.settings_dict.get('display_related_people') == 'Yes':
            people_relationship_people_container = self.createRelationContainer('People','No')
            container_list.append(people_relationship_people_container)
            tab_title_names_list.append('Related People')

        #If items are to be displayed, a tab is created for each item
        if container_list:
            related_work_tab = widgets.Tab()
            related_work_tab.children = container_list
            for index in range(len(tab_title_names_list)):
                related_work_tab.set_title(index, tab_title_names_list[index])
            display(related_work_tab)
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
        self.tab_title_names_list =[]

        if self.settings_dict.get('display_related_projects') == 'Yes':
            project_relationship_container = self.createRelationContainer('Project','Yes')
            container_list.append(project_relationship_container)
            self.tab_title_names_list.append('Related Projects')

        if self.settings_dict.get('display_related_investigations') == 'Yes':
            investigation_relationship_container = self.createRelationContainer('Investigation','Yes')
            container_list.append(investigation_relationship_container)
            self.tab_title_names_list.append('Related Investigations')

        if self.settings_dict.get('display_related_studies') == 'Yes':
            study_relationship_people_container = self.createRelationContainer('Study','Yes')
            container_list.append(study_relationship_people_container)
            self.tab_title_names_list.append('Related Studies')


        if self.settings_dict.get('display_related_assays') == 'Yes':
            assay_relationship_people_container = self.createRelationContainer('Assay','Yes')
            container_list.append(assay_relationship_people_container)
            self.tab_title_names_list.append('Related Assays')


        #If items are to be displayed, a tab is created for each item
        if container_list:
            self.related_work_tab = widgets.Tab()
            self.related_work_tab.children = container_list
            for index in range(len(self.tab_title_names_list)):
                self.related_work_tab.set_title(index, self.tab_title_names_list[index])
            display(self.related_work_tab)

    def display_project(self):
        container_list =[]
        #name of items to display
        self.project_tab_title_names_list =[]
        if self.settings_dict.get('display_project_members') == 'Yes':
            project_members_container = self.createRelationContainer('Project Member','Yes')
            container_list.append(project_members_container)
            self.project_tab_title_names_list.append('Project Members')

        if self.settings_dict.get('display_project_administrators') == 'Yes':
            project_admin_container = self.createRelationContainer('Project Admin','Yes')
            container_list.append(project_admin_container)
            self.project_tab_title_names_list.append('Project Admins')

        if self.settings_dict.get('display_project_asset_housekeepers') == 'Yes':
            project_asset_HK_container = self.createRelationContainer('Asset HK','Yes')
            container_list.append(project_asset_HK_container)
            self.project_tab_title_names_list.append('Project Asset HK')

        if self.settings_dict.get('display_project_asset_gatekeepers') == 'Yes':
            project_asset_GK_container = self.createRelationContainer('Asset GK','Yes')
            container_list.append(project_asset_GK_container)
            self.project_tab_title_names_list.append('Project Asset GK')

        if self.settings_dict.get('display_related_people') == 'Yes':
            people_relationship_people_container = self.createRelationContainer('People','No')
            container_list.append(people_relationship_people_container)
            self.project_tab_title_names_list.append('Related People')

        if self.settings_dict.get('display_project_organisms') == 'Yes':
            project_organisms_container = self.createRelationContainer('Project Organisms','Yes')
            container_list.append(project_organisms_container)
            self.project_tab_title_names_list.append('Project Organisms')

        if self.settings_dict.get('display_project_institutions') == 'Yes':
            project_institute_container = self.createRelationContainer('Project Institute','Yes')
            container_list.append(project_institute_container)
            self.project_tab_title_names_list.append('Project Institutions')

        if self.settings_dict.get('display_project_programmes') == 'Yes':
            project_programmes_container = self.createRelationContainer('Project Program','Yes')
            container_list.append(project_programmes_container)
            self.project_tab_title_names_list.append('Project Programmes')
        #If items are to be displayed, a tab is created for each item
        if container_list:
            self.project_tab = widgets.Tab()
            self.project_tab.children = container_list
            for index in range(len(self.project_tab_title_names_list)):
                self.project_tab.set_title(index, self.project_tab_title_names_list[index])
            display(self.project_tab)

    def createRelationContainer(self,type,increased_width):
        '''
        Creates the container for each item to be displayed

        Each item contains a dropbox of the titles of related documents and a#
        search button

        type            : document type
        increased_width : binary option for increased_width
                          if value is Yes then this makes the dropbox width
                          longer
        '''

        #Get a dictionary of data that contains ID amnd type
        #Iterate over dictionary to get the names from IDs
        desc = ''

        if type =='Creator':
            dict  = self.json_handler.get_relationship_creators(self.json)
            names = self.getListOfNamesFromDict(dict)
            desc = 'Name :'
            increased_width = 'No'

        elif type =='Submitter':
            dict  = self.json_handler.get_relationship_submitters(self.json)
            names = self.getListOfNamesFromDict(dict)
            desc = 'Name :'
            increased_width = 'No'

        elif type =='People':
            dict  = self.json_handler.get_relationship_people(self.json)
            names = self.getListOfNamesFromDict(dict)
            desc = 'Name :'
            increased_width = 'No'

        elif type == 'Project':
            dict  = self.json_handler.get_relationship_projects(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.project_names = self.getValuesOfDict(dictIDAndName)
            # print(self.project_names)
            names = self.project_names
            self.project_ids =self.getKeysOfDict(dictIDAndName)
            # print(self.project_ids)

            desc = 'Title :'
        elif type == 'Investigation':
            dict  = self.json_handler.get_relationship_investigations(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.investigation_names = self.getValuesOfDict(dictIDAndName)
            names = self.investigation_names

            self.investigation_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'

        elif type == 'Study':
            dict  = self.json_handler.get_relationship_studies(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.study_names = self.getValuesOfDict(dictIDAndName)
            names = self.study_names

            self.study_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'

        elif type == 'Assay':
            dict  = self.json_handler.get_relationship_assays(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.assay_names = self.getValuesOfDict(dictIDAndName)
            names = self.assay_names

            self.assay_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'

        elif type =='Project Member':
            print()

        elif type =='Project Admin':
            dict  = self.json_handler.get_project_admins(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.assay_names = self.getValuesOfDict(dictIDAndName)
            names = self.assay_names

            self.assay_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 'No'

        elif type =='Asset HK':
            dict  = self.json_handler.get_asset_HK(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.assay_names = self.getValuesOfDict(dictIDAndName)
            names = self.assay_names

            self.assay_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 'No'

        elif type =='Asset GK':
            dict  = self.json_handler.get_asset_GK(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.assay_names = self.getValuesOfDict(dictIDAndName)
            names = self.assay_names

            self.assay_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 'No'

        elif type =='Project Organisms':
            dict  = self.json_handler.get_organisms(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.assay_names = self.getValuesOfDict(dictIDAndName)
            names = self.assay_names

            self.assay_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 'No'

        elif type =='Project Institute':
            dict  = self.json_handler.get_project_institutions(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.assay_names = self.getValuesOfDict(dictIDAndName)
            names = self.assay_names

            self.assay_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 'No'

        elif type =='Project Program':
            dict  = self.json_handler.get_project_programmes(self.json)
            dictIDAndName = self.getDictOfIDandNames(dict,type)
            self.assay_names = self.getValuesOfDict(dictIDAndName)
            names = self.assay_names

            self.assay_ids =self.getKeysOfDict(dictIDAndName)
            desc = 'Title :'
            increased_width = 'No'

        relation = self.relationship_drop_box(names,increased_width,desc)
        relation_search_button = self.createRelationSearchWidget(relation.value)
        if type == 'Project' or type =='Investigation' or type == 'Study' or type == 'Assay':
            relation_search_button.on_click(self.on_click_search)


        relationship_widget_list  = [
            relation,
            relation_search_button
                        ]
        #Sorts positioning of container
        #dropbox above a search button
        relationship_people_container = widgets.VBox([relationship_widget_list[0], relationship_widget_list[1]])

        return relationship_people_container


    def on_click_search(self,button):

        tab_index = self.related_work_tab.selected_index
        item_index = self.related_work_tab.children[tab_index].children[0].index[0]
        if self.tab_title_names_list[tab_index] == 'Related Projects':
            topic = 'Document query'
            type = 'Project'
            id = self.project_ids[item_index]
        elif self.tab_title_names_list[tab_index] == 'Related Investigations':
            topic = 'Document query'
            type = 'Investigation'
            id = self.investigation_ids[item_index]
        elif self.tab_title_names_list[tab_index] == 'Related Studies':
            topic = 'Document query'
            type = 'Study'
            id = self.study_ids[item_index]
        elif self.tab_title_names_list[tab_index] == 'Related Assays':
            topic = 'Document query'
            type = 'Assay'
            id = self.assay_ids[item_index]

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

    def getKeysOfDict(self,dict):
        keys = dict.keys()
        return keys

    def getValuesOfDict(self,dict):
        values = dict.values()
        return values


    def getDictOfIDandNames(self,dict,sessionType):
        ids = []
        ids = self.iterate_over_json_list(dict,ids)
        # self.temp_list_of_ids = ids
        dictIDAndNames = {}

        dictIDAndNames = self.multiprocess_search(ids,sessionType)
        return dictIDAndNames

    def relationship_drop_box(self,list_of_names,increased_width,desc):
        x =list_of_names
        default_value =[]
        number_of_rows = 1
        if list_of_names:
            default_value.append(x[0])
            if len(list_of_names) > 4:
                number_of_rows = 4
            else :
                number_of_rows = len(list_of_names)
        if increased_width == 'Yes':
            layout = {'width': '725px'}
        else :
            layout = {'width': '300px'}
        relationship_dropdown_widget = widgets.SelectMultiple(
            layout = layout,
            options=x,
            value=default_value,
            rows=number_of_rows,
            description=desc,
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


    def retrieve_person_name(self,idNumber,dictData,pnumber):
        personMetaData = self.json_handler.get_JSON('people',idNumber,'None')
        if not personMetaData:
            # return personMetaData
            dictData[idNumber]=personMetaData
        else:
        # return self.json_handler.get_title(personMetaData)
            dictData[idNumber]=self.json_handler.get_title(personMetaData)


    def retrieve_project_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Project',idNumber,'None')
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)


    def retrieve_investigation_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Investigation',idNumber,'None')
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)


    def retrieve_study_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Study',idNumber,'None')
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)


    def retrieve_assay_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Assay',idNumber,'None')
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)

    def retrieve_organism_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Project Organisms',idNumber,'None')
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)
    def retrieve_institute_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Project Institute',idNumber,'None')
        if not metaData:
            dictData[idNumber]=metaData
            # return metaData
        else:
        # return self.json_handler.get_title(metaData)
            dictData[idNumber]=self.json_handler.get_title(metaData)
    def retrieve_program_name(self,idNumber,dictData,pnumber):
        metaData = self.json_handler.get_JSON('Project Program',idNumber,'None')
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
            self.display_doc()
        elif self.topic == 'Person query':
            pass
        elif self.topic ==  'To be implemented':
            pass
