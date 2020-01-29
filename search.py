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
        creatorsDict  = self.json_handler.get_relationship_creators(self.json)
        creator_names = self.getListOfNamesFromDict(creatorsDict)

        creator_relation = self.relationship_drop_box(creator_names,'No')
        creator_relation_people_search_button = self.createRelationSearchWidget(creator_relation.value)
        creator_relationship_widget_list  = [
            creator_relation,
            creator_relation_people_search_button
                        ]
        creator_relationship_people_container = widgets.VBox([creator_relationship_widget_list[0], creator_relationship_widget_list[1]])

        submittersDict  = self.json_handler.get_relationship_submitters(self.json)
        submitter_names = self.getListOfNamesFromDict(submittersDict)

        submitter_relation = self.relationship_drop_box(submitter_names,'No')
        submitter_relation_people_search_button = self.createRelationSearchWidget(submitter_relation.value)
        submitter_relationship_widget_list  = [
            submitter_relation,
            submitter_relation_people_search_button
                        ]
        submitter_relationship_people_container = widgets.VBox([submitter_relationship_widget_list[0], submitter_relationship_widget_list[1]])

        peopleDict  = self.json_handler.get_relationship_people(self.json)
        people_names = self.getListOfNamesFromDict(submittersDict)

        people_relation = self.relationship_drop_box(people_names,'No')
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

    def display_work_relations(self):
        container_list =[]
        tab_title_names_list =[]
        if self.settings_dict.get('display_related_projects') == 'Yes':
            projectsDict  = self.json_handler.get_relationship_projects(self.json)
            project_names = self.getListOfNamesFromDictSearch(projectsDict,'Project')
            project_relation = self.relationship_drop_box(project_names,'Yes')
            project_relation_people_search_button = self.createRelationSearchWidget(project_relation.value)
            project_relationship_widget_list  = [
                project_relation,
                project_relation_people_search_button
                            ]
            project_relationship_container = widgets.VBox([project_relationship_widget_list[0], project_relationship_widget_list[1]])
            container_list.append(project_relationship_container)
            tab_title_names_list.append('Related Projects')

        # if self.settings_dict.get('display_related_investigations') == 'Yes':
        #     investigationsDict  = self.json_handler.get_relationship_investigations(self.json)
        #     investigation_names = self.getListOfNamesFromDictSearch(investigationsDict,'Investigation')
        #
        #     investigation_relation = self.relationship_drop_box(investigation_names,'Yes')
        #     investigation_relation_people_search_button = self.createRelationSearchWidget(investigation_relation.value)
        #     investigaiton_relationship_widget_list  = [
        #         investigation_relation,
        #         investigation_relation_people_search_button
        #                     ]
        #     investigation_relationship_people_container = widgets.VBox([investigaiton_relationship_widget_list[0], investigaiton_relationship_widget_list[1]])
        #     container_list.append(investigation_relationship_people_container)
        #     tab_title_names_list.append('Related Investigations')


        if self.settings_dict.get('display_related_studies') == 'Yes':
            studiesDict  = self.json_handler.get_relationship_studies(self.json)
            study_names = self.getListOfNamesFromDictSearch(studiesDict,'Study')

            study_relation = self.relationship_drop_box(study_names,'Yes')
            study_relation_people_search_button = self.createRelationSearchWidget(study_relation.value)
            study_relationship_widget_list  = [
                study_relation,
                study_relation_people_search_button
                            ]
            study_relationship_people_container = widgets.VBox([study_relationship_widget_list[0], study_relationship_widget_list[1]])
            container_list.append(study_relationship_people_container)
            tab_title_names_list.append('Related Studies')


        if self.settings_dict.get('display_related_assays') == 'Yes':
            assaysDict  = self.json_handler.get_relationship_assays(self.json)
            assay_names = self.getListOfNamesFromDictSearch(assaysDict,'Assay')

            assay_relation = self.relationship_drop_box(assay_names,'Yes')
            assay_relation_people_search_button = self.createRelationSearchWidget(assay_relation.value)
            assay_relationship_widget_list  = [
                assay_relation,
                assay_relation_people_search_button
                            ]
            assay_relationship_people_container = widgets.VBox([assay_relationship_widget_list[0], assay_relationship_widget_list[1]])
            container_list.append(assay_relationship_people_container)
            tab_title_names_list.append('Related Assays')



        if container_list:
            related_work_tab = widgets.Tab()
            related_work_tab.children = container_list
            for index in range(len(tab_title_names_list)):
                related_work_tab.set_title(index, tab_title_names_list[index])
            display(related_work_tab)



    def display_doc_relations(self):
        projectsDict  = self.json_handler.get_relationship_projects(self.json)



        creator_names = self.getListOfNamesFromDict(creatorsDict)

        creator_relation = self.relationship_drop_box(creator_names,'No')
        creator_relation_people_search_button = self.createRelationSearchWidget(creator_relation.value)
        creator_relationship_widget_list  = [
            creator_relation,
            creator_relation_people_search_button
                        ]
        creator_relationship_people_container = widgets.VBox([creator_relationship_widget_list[0], creator_relationship_widget_list[1]])

        submittersDict  = self.json_handler.get_relationship_submitters(self.json)
        submitter_names = self.getListOfNamesFromDict(submittersDict)

        submitter_relation = self.relationship_drop_box(submitter_names,'No')
        submitter_relation_people_search_button = self.createRelationSearchWidget(submitter_relation.value)
        submitter_relationship_widget_list  = [
            submitter_relation,
            submitter_relation_people_search_button
                        ]
        submitter_relationship_people_container = widgets.VBox([submitter_relationship_widget_list[0], submitter_relationship_widget_list[1]])

        peopleDict  = self.json_handler.get_relationship_people(self.json)
        people_names = self.getListOfNamesFromDict(submittersDict)

        people_relation = self.relationship_drop_box(people_names,'No')
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

    def getListOfNamesFromDictSearch(self,dict,sessionType):
        ids = []
        ids = self.iterate_over_json_list(dict,ids)
        names = []

        names = self.multiprocess_search(ids,sessionType)
        return names
    def relationship_drop_box(self,list_of_names,increased_width):
        x =list_of_names
        default_value =[]
        number_of_rows = 1
        if list_of_names:
            default_value.append(x[0])
            if len(list_of_names) > 3:
                number_of_rows = 3
            else :
                number_of_rows = len(list_of_names)
        if increased_width == 'Yes':
            layout = {'width': '600px'}
        else :
            layout = {'width': '300px'}
        relationship_dropdown_widget = widgets.SelectMultiple(
            layout = layout,
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

    def multiprocess_search(self,idNumbers,sessionType):

        processesBeingRun = Pool(processes = 15)
        if sessionType == 'people':
            dataRec = processesBeingRun.map(self.retrieve_person_name,idNumbers)
        elif sessionType == 'Project':
            dataRec = processesBeingRun.map(self.retrieve_project_name,idNumbers)
        elif sessionType == 'Investigation':
            dataRec = processesBeingRun.map(self.retrieve_investigation_name,idNumbers)
        elif sessionType == 'Study':
            dataRec = processesBeingRun.map(self.retrieve_study_name,idNumbers)
        elif sessionType == 'Assay':
            dataRec = processesBeingRun.map(self.retrieve_assay_name,idNumbers)

        processesBeingRun.close()
        return dataRec

    def retrieve_person_name(self,idNumber):
        personMetaData = self.json_handler.get_JSON('people',idNumber,'None')
        if not personMetaData:
            return personMetaData
        return self.json_handler.get_title(personMetaData)

    def retrieve_project_name(self,idNumber):
        metaData = self.json_handler.get_JSON('Project',idNumber,'None')
        if not metaData:
            return metaData
        return self.json_handler.get_title(metaData)

    def retrieve_investigation_name(self,idNumber):
        metaData = self.json_handler.get_JSON('Investigation',idNumber,'None')
        if not metaData:
            return metaData
        return self.json_handler.get_title(metaData)

    def retrieve_study_name(self,idNumber):
        metaData = self.json_handler.get_JSON('Study',idNumber,'None')
        if not metaData:
            return metaData
        return self.json_handler.get_title(metaData)

    def retrieve_assay_name(self,idNumber):
        metaData = self.json_handler.get_JSON('Assay',idNumber,'None')
        if not metaData:
            return metaData
        return self.json_handler.get_title(metaData)


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
