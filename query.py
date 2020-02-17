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
from pandas.io.json import json_normalize

from multiprocessing import Pool
from IPython.display import display
from IPython.display import HTML
from IPython.display import clear_output

from json_methods import JSON_methods
from widget import Widget
from call_search import Call_Search


class Query():
    '''
    Class used to search/browse data on the FairdomHub website
    (https://www.fairdomhub.org)

    To use :
        import seek_library as s
        x= s.read()
        x.query()
        x.search()

    '''
    def __init__(self,json_handler):
        '''
        Sets up varaiables for class
        Contains details on what the search items are
        Gets all the user names and IDs of all FAIRDOM users
        '''

        '''
        Will program ability to get json of item in query so that search wont
        need to Wait
        use multithreading??

        '''
        self.widget = Widget()
        self.json = None

        self.json_handler = json_handler
        self.call_search = Call_Search(self.json_handler)

        # self.search_and_display_handler =  search_and_display()
        self.search_doc_id = None
        self.doc_option_selected = None
        self.current_blob = None

        self.settings_dict_from_file={}
        self.settings_dict = {}


        self.dict_of_users_and_ids = {}
        self.list_of_user_names=[]
        self.list_of_user_ids=[]
        self.user_list_alphabet_order= []


        self.search_person_list = []
        self.max_ID_value=0;

        self.name_search_widget = None
        self.people_search_ID_widget = None

        self.query_tab = None
        self.maxProcesses = 5;

        self.load_default_settings()
        self.get_all_FAIRDOM_user_names_and_ID()

    def set_json_handler(self,json_handler):
        self.json_handler = json_handler
        self.call_search.set_json_handler(json_handler)

    def get_all_FAIRDOM_user_names_and_ID(self):
        '''
        Gets a dictionary of all users and IDs
        as well as lists for both users and IDs
        '''
        self.dict_of_users_and_ids.clear()

        temp_list =[]
        self.dict_of_users_and_ids = self.json_handler.get_dictionary_of_user_and_id()
        temp_list = self.json_handler.get_list_of_user_ids()
        self.list_of_user_ids =temp_list
        temp_list = self.json_handler.get_list_of_user_names()
        self.list_of_user_names = temp_list

    def get_dict_of_user_names_and_ids(self):
        return self.dict_of_users_and_ids
    def get_list_of_user_names(self):
        return self.list_of_user_names
    def get_list_of_user_ids(self):
        return self.list_of_user_ids

    def read_settings_file(self):
        '''
        Get the saved settings for the search options
        '''
        fn = 'search_settings.txt'
        try:
            file = open(fn, 'r')
        except IOError:
            file = open(fn, 'w+')

        try:

            with file as f:
                for line in f:
                   (key, value) = line.split()
                   self.settings_dict_from_file[key] = value

            self.settings_dict = dict(self.settings_dict_from_file)
            file.close()
        except:
            print('Error with settings file')
            print('Delete file to fix')

    def save_settings(self):
        '''
        Save the search options to a file
        '''
        self.get_updated_setting_options()
        fn = 'search_settings.txt'
        try:
            file = open(fn, 'w')

            for key in self.settings_dict:
                k = (key)
                val = (self.settings_dict.get(key))
                to_write = k + ' ' + val + '\n'
                file.write(to_write)

            file.close()
        except:
            print('Error with settings file')
            print('Delete file to fix')

    def load_settings(self):
        '''
        Load search option settings from the file
        and display the choices on the widgets on the settings tab
        '''
        self.read_settings_file()
        self.query_tab.children[2].children[0].children[0].children[0].children[0].value = self.settings_dict_from_file.get('display_title')

        self.query_tab.children[2].children[0].children[0].children[0].children[1].value = self.settings_dict_from_file.get('display_description')

        self.query_tab.children[2].children[0].children[0].children[0].children[2].value = self.settings_dict_from_file.get('display_model_name')

        self.query_tab.children[2].children[0].children[0].children[0].children[3].value = self.settings_dict_from_file.get('display_model')

        self.query_tab.children[2].children[0].children[0].children[0].children[4].value = self.settings_dict_from_file.get('display_download_link')

        self.query_tab.children[2].children[0].children[0].children[1].children[0].value = self.settings_dict_from_file.get('display_creators')
        self.query_tab.children[2].children[0].children[0].children[1].children[1].value = self.settings_dict_from_file.get('display_submitter')
        self.query_tab.children[2].children[0].children[0].children[1].children[2].value = self.settings_dict_from_file.get('display_related_people')
        self.query_tab.children[2].children[0].children[0].children[1].children[3].value = self.settings_dict_from_file.get('display_related_projects')
        self.query_tab.children[2].children[0].children[0].children[1].children[4].value = self.settings_dict_from_file.get('display_related_investigations')
        self.query_tab.children[2].children[0].children[0].children[1].children[5].value = self.settings_dict_from_file.get('display_related_studies')
        self.query_tab.children[2].children[0].children[0].children[1].children[6].value = self.settings_dict_from_file.get('display_related_assays')
        self.query_tab.children[2].children[0].children[0].children[1].children[7].value = self.settings_dict_from_file.get('display_related_data_files')

        self.query_tab.children[2].children[0].children[0].children[1].children[8].value = self.settings_dict_from_file.get('display_related_publications')
        self.query_tab.children[2].children[0].children[0].children[1].children[9].value = self.settings_dict_from_file.get('display_related_events')
        self.query_tab.children[2].children[0].children[0].children[1].children[10].value = self.settings_dict_from_file.get('display_project_members')
        self.query_tab.children[2].children[0].children[0].children[1].children[11].value = self.settings_dict_from_file.get('display_project_administrators')
        self.query_tab.children[2].children[0].children[0].children[1].children[12].value = self.settings_dict_from_file.get('display_project_asset_housekeepers')
        self.query_tab.children[2].children[0].children[0].children[1].children[13].value = self.settings_dict_from_file.get('display_project_asset_gatekeepers')
        self.query_tab.children[2].children[0].children[0].children[1].children[14].value = self.settings_dict_from_file.get('display_project_organisms')
        self.query_tab.children[2].children[0].children[0].children[1].children[15].value = self.settings_dict_from_file.get('display_project_institutions')
        self.query_tab.children[2].children[0].children[0].children[1].children[16].value = self.settings_dict_from_file.get('display_project_programmes')

    def load_default_settings(self):
        '''
        Default settings for the search options
        '''

        self.settings_dict['display_title'] = 'True'
        self.settings_dict['display_description'] = 'True'
        self.settings_dict['display_model_name'] = 'True'
        self.settings_dict['display_model'] = 'True'
        self.settings_dict['display_download_link'] = 'True'
        self.settings_dict['display_creators'] = 'True'
        self.settings_dict['display_submitter'] = 'True'
        self.settings_dict['display_related_people'] = 'True'
        self.settings_dict['display_related_projects'] = 'True'
        self.settings_dict['display_related_investigations'] = 'True'
        self.settings_dict['display_related_studies'] = 'True'
        self.settings_dict['display_related_assays'] = 'True'
        self.settings_dict['display_related_data_files'] = 'True'

        self.settings_dict['display_related_publications'] = 'True'
        self.settings_dict['display_related_events'] = 'True'

        self.settings_dict['display_project_members'] = 'True'
        self.settings_dict['display_project_administrators'] = 'True'
        self.settings_dict['display_project_asset_housekeepers'] = 'True'
        self.settings_dict['display_project_asset_gatekeepers'] = 'True'
        self.settings_dict['display_project_organisms'] = 'True'
        self.settings_dict['display_project_institutions'] = 'True'
        self.settings_dict['display_project_programmes'] = 'True'

    def change_made_name_search(self, change):
        '''
        Deals with any updates in the combo box widget for name in person tab
        If valid name is entered, update the id combo box widget in person tab
        with the corresponding ID
        '''
        #Prevent the ID widget from automatically updating
        #as update is forced done in this method
        self.people_search_ID_widget.unobserve(self.change_made_people_search_ID)

        #Remove ID when name box is made empty
        #If name is valid, update ID box
        if (change['new'] ==''):
            self.people_search_ID_widget.value = ''
        elif change['type'] == 'change' and change['name'] == 'value':
            name_selected = change['new']
            if name_selected in self.dict_of_users_and_ids.keys():
                ID_index_list = self.dict_of_users_and_ids.get(name_selected)
                #if name has multiple IDs, ask the user to choose which ID
                if len(ID_index_list) > 1:
                    self.people_search_ID_widget.value = ''
                    self.people_search_ID_widget.placeholder = 'Choose ID'
                    self.people_search_ID_widget.options = ID_index_list
                else :
                    self.people_search_ID_widget.value = str(ID_index_list[0])
            else :
                self.people_search_ID_widget.value = ''
                self.people_search_ID_widget.placeholder = 'Enter ID'
                self.people_search_ID_widget.options = []

        self.people_search_ID_widget.observe(self.change_made_people_search_ID)

    def change_made_people_search_ID(self, change):
        '''
        Deals with any updates in the ID combo box widget in person tab
        Updates the name combo box widget in person tab with corresponding ID
        '''
        #Prevent the name widget from automatically updating
        #as update is forced done in this method
        self.name_search_widget.unobserve(self.change_made_name_search)
        if change['new'] =='':
            self.name_search_widget.value = ''
            self.name_search_widget.options = []
        elif change['type'] == 'change' and change['name'] == 'value':
            ID=str(change['new'])
            #If ID is in database, display the name associated
            if (change['new'] in self.list_of_user_ids):
                name = self.list_of_user_names[self.list_of_user_ids.index(ID)]
                self.name_search_widget.value = name
            else:
                self.name_search_widget.value = ''
                # self.name_search_widget.options = self.user_list_alphabet_order

        self.name_search_widget.observe(self.change_made_name_search)

    def change_made_doc_option(self, change):
        '''
        Deals with update in Search Type dropdown widget in the Document Tab
        Store the working document type
        '''
        option = None
        if change['type'] == 'change' and change['name'] == 'value':
            if str(change['new']) == 'Project':
                option = 'Project'
            elif str(change['new']) == 'Investigation':
                option = 'Investigation'
            elif str(change['new']) == 'Study':
                option = 'Study'
            elif str(change['new']) == 'Assay':
                option = 'Assay'
            elif str(change['new']) == 'Data File':
                option = 'Data File'

            #sets the class variable to option
            self.doc_option_selected = option

    def change_made_ID(self, change):
        '''
        Deals with update in ID number int widget in the Document Tab
        Stores the selected ID number
        '''
        if change['type'] == 'change' and change['name'] == 'value':
            #print("changed to %s" % change['new'])
            self.search_doc_id = int(change['new'])

    def on_click_setting_load_save(self, button):
        '''
        Deals with button press for both Load Settings and Save Settings button
        in the Search settings tab
        Either loads settings from file or saves the settings to file depending
        on button pressed
        '''

        if button.description == 'Load Settings':
            self.load_settings()
        elif button.description == 'Save Settings':
            self.save_settings()
    def on_click_search(self, button):
        list_of_names = self.list_of_user_names
        list_of_ids = self.list_of_user_ids
        topic = self.get_topic()
        settings_dict =self.get_setting_options_dict()
        settings_dict = dict(settings_dict)
        id = self.get_id_to_search()
        type = self.get_type_to_search()
        self.call_search.search(list_of_names,list_of_ids,topic,settings_dict,id,type)

    def on_click_convert(self, button):
        tab_index = self.query_tab.selected_index
        title = self.query_tab._titles.get(str(tab_index))
        clear_output()
        print('Query type       : {0}'.format(title))
        if tab_index == 0 :
            type = self.query_tab.children[tab_index].children[0].value
            id =  self.query_tab.children[tab_index].children[1].value
            print('File search type : {0}'.format(type))
            print('ID search        : {0}'.format(id))
        elif tab_index == 1 :
            id =  self.query_tab.children[tab_index].children[0].value
            print('ID search        : {0}'.format(id))
    def document_tab(self):
        '''
        Creates tab relating to searching for a working document
        '''

        doc_select_widget_list = []
        options=['Project','Investigation','Study', 'Assay', 'Data File']
        desc = 'Search Type:'
        doc_option_widget = self.widget.dropdown_widget(options,'default',desc)
        doc_select_widget_list.append(doc_option_widget)
        #calls a function that handles updates in the drop down menu
        doc_option_widget.observe(self.change_made_doc_option)
        self.doc_option_selected = doc_option_widget.value

        value=1
        desc='ID number:'
        bool=False
        min=1
        max = sys.maxsize
        doc_id_search_widget= self.widget.bounded_int_text_widget(value,desc,bool,min,max)
        doc_select_widget_list.append(doc_id_search_widget)

        #calls a function that handles updates in the int box
        doc_id_search_widget.observe(self.change_made_ID)

        self.search_doc_id = doc_id_search_widget.value
        desc = 'Search'
        search = self.widget.button(desc)
        search.on_click(self.on_click_search)
        doc_select_widget_list.append(search)

        #Formats the widgets into a column
        doc_select_widgets_container = widgets.VBox([doc_select_widget_list[0],
                                                     doc_select_widget_list[1],
                                                     doc_select_widget_list[2]])
        return doc_select_widgets_container

    def person_tab(self):
        '''
        Creates tab relating to searching for a person
        '''
        #Get the list of users sorted in alphbetical order and removes
        #duplicates
        self.user_list_alphabet_order = []
        self.user_list_alphabet_order = list(self.list_of_user_names)
        #removes duplicates
        self.user_list_alphabet_order = list(dict.fromkeys(self.user_list_alphabet_order))
        #sort alphabetically
        self.user_list_alphabet_order.sort()
        #add empty string for when the widget is empty
        self.user_list_alphabet_order.append('')
        people_search_widget_list = []
        ph='Enter ID'
        options=[]
        desc='ID :'
        ensure_option=False
        bool_active=False
        self.people_search_ID_widget = self.widget.combobox(ph,options,desc,ensure_option,bool_active)
        people_search_widget_list.append(self.people_search_ID_widget)
        #Handles update to ID widget
        self.people_search_ID_widget.observe(self.change_made_people_search_ID)

        ph='Enter Name'
        options=[]
        desc='Name :'
        ensure_option=False
        bool_active=False
        self.name_search_widget = self.widget.combobox(ph,options,desc,ensure_option,bool_active)
        people_search_widget_list.append(self.name_search_widget)

        #Handles update to name widget
        self.name_search_widget.observe(self.change_made_name_search)
        desc = 'To Search'
        search = self.widget.button(desc)
        search.on_click(self.on_click_search)
        people_search_widget_list.append(search)
        #Formats the widgets into a column
        people_search_container = widgets.VBox([people_search_widget_list[0],
                                                people_search_widget_list[1],
                                                people_search_widget_list[2]])

        return people_search_container

    def general_setting_widgets(self):
        setting_option_widget_list = []
        desc='Display Title:'
        value = self.settings_dict.get('display_title')
        title_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(title_option)

        desc='Display Description:'
        value =self.settings_dict.get('display_description')
        description_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(description_option)


        desc='Display Model Name:'
        value = self.settings_dict.get('display_model_name')
        model_name_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(model_name_option)


        desc='Display Model:'
        value = self.settings_dict.get('display_model')
        model_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(model_option)


        desc='Display Download Link:'
        value = self.settings_dict.get('display_download_link')
        download_link_option =self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(download_link_option)

        column = widgets.VBox([setting_option_widget_list[0],
                                   setting_option_widget_list[1],
                                   setting_option_widget_list[2],
                                   setting_option_widget_list[3],
                                   setting_option_widget_list[4]])


        return column

    def relationship_setting_widgets(self):
        setting_option_widget_list = []
        desc='Display Creator:'
        value = self.settings_dict.get('display_creators')
        creators_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(creators_option)

        desc='Display Submitter:'
        value = self.settings_dict.get('display_submitter')
        submitter_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(submitter_option)

        desc='Display People:'
        value = self.settings_dict.get('display_related_people')
        related_people_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(related_people_option)

        desc='Display Related Projects:'
        value = self.settings_dict.get('display_related_projects')
        related_projects_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(related_projects_option)

        desc='Display Related Investigations:'
        value = self.settings_dict.get('display_related_investigations')
        related_investigations_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(related_investigations_option)

        desc='Display Related Studies:'
        value = self.settings_dict.get('display_related_studies')
        related_studies_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(related_studies_option)

        desc='Display Related Assays:'
        value = self.settings_dict.get('display_related_assays')
        related_assays_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(related_assays_option)

        desc='Display Related Data Files:'
        value = self.settings_dict.get('display_related_data_files')
        related_data_files_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(related_data_files_option)

        desc='Display Related Publications:'
        value = self.settings_dict.get('display_related_publications')
        related_publications_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(related_publications_option)

        desc='Display Related Events:'
        value = self.settings_dict.get('display_related_events')
        related_events_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(related_events_option)

        desc='Display Project Members:'
        value = self.settings_dict.get('display_project_members')
        project_members_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(project_members_option)

        desc='Display Project Admins:'
        value = self.settings_dict.get('display_project_administrators')
        project_admins_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(project_admins_option)

        desc='Display Project Assest HK:'
        value = self.settings_dict.get('display_project_asset_housekeepers')
        project_asset_HK_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(project_asset_HK_option)

        desc='Display Project Assest GK:'
        value = self.settings_dict.get('display_project_asset_gatekeepers')
        project_asset_GK_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(project_asset_GK_option)

        desc='Display Project Organisms:'
        value = self.settings_dict.get('display_project_organisms')
        project_organisms_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(project_organisms_option)

        desc='Display Project Institutions:'
        value = self.settings_dict.get('display_project_institutions')
        project_institutions_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(project_institutions_option)

        desc='Display Project Programmes:'
        value = self.settings_dict.get('display_project_programmes')
        project_institutions_option = self.widget.toggle_button(desc,value)
        setting_option_widget_list.append(project_institutions_option)

        column = widgets.VBox([setting_option_widget_list[0],
                               setting_option_widget_list[1],
                               setting_option_widget_list[2],
                               setting_option_widget_list[3],
                               setting_option_widget_list[4],
                               setting_option_widget_list[5],
                               setting_option_widget_list[6],
                               setting_option_widget_list[7],
                               setting_option_widget_list[8],
                               setting_option_widget_list[9],
                               setting_option_widget_list[10],
                               setting_option_widget_list[11],
                               setting_option_widget_list[12],
                               setting_option_widget_list[13],
                               setting_option_widget_list[14],
                               setting_option_widget_list[15],
                               setting_option_widget_list[16],
                               ])


        return column

    def settings_tab(self):
        '''
        Creates tab relating to settings used for searching
        '''
        settings_widget_list=[]
        desc='Load Settings'
        load_settings_option = self.widget.button(desc)
        settings_widget_list.append(load_settings_option)

        desc='Save Settings'
        save_settings_option = self.widget.button(desc)
        settings_widget_list.append(save_settings_option)


        load_settings_option.on_click(self.on_click_setting_load_save)
        save_settings_option.on_click(self.on_click_setting_load_save)


        widget_list = []
        general_setting_options_list = self.general_setting_widgets()
        widget_list.append(general_setting_options_list)
        relation_setting_option_list = self.relationship_setting_widgets()
        widget_list.append(relation_setting_option_list)

        settings_accordion = self.widget.accordion(widget_list)

        settings_accordion.set_title(0, 'General settings')
        settings_accordion.set_title(1, 'Relationship settings')

        settings_accordion.selected_index = None
        # general_settings_accordion.set_title(1, 'Relationship settings')


        left_column = widgets.VBox([settings_accordion])

        #right column widgets are for saving and loading the options
        right_column = widgets.VBox([settings_widget_list[0],
                                    settings_widget_list[1]])

        #formatted in two columns
        settings_container = widgets.HBox([left_column,right_column])

        return settings_container

    def get_updated_setting_options(self):
        '''
        Get the newest values of the search options from the widgets in the
        Search settings tab
        '''
        value = self.get_query_tab_children_settings_values('display_title')
        self.settings_dict['display_title'] = value

        value= self.get_query_tab_children_settings_values('display_description')
        self.settings_dict['display_description'] = value

        value = self.get_query_tab_children_settings_values('display_model_name')
        self.settings_dict['display_model_name'] = value

        value = self.get_query_tab_children_settings_values('display_download_link')
        self.settings_dict['display_download_link'] = value

        value = self.get_query_tab_children_settings_values('display_model')
        self.settings_dict['display_model'] = value

        value = self.get_query_tab_children_settings_values('display_creators')
        self.settings_dict['display_creators'] = value

        value = self.get_query_tab_children_settings_values('display_submitter')
        self.settings_dict['display_submitter'] = value

        value = self.get_query_tab_children_settings_values('display_related_people')
        self.settings_dict['display_related_people'] = value

        value = self.get_query_tab_children_settings_values('display_related_projects')
        self.settings_dict['display_related_projects'] = value

        value = self.get_query_tab_children_settings_values('display_related_investigations')
        self.settings_dict['display_related_investigations'] = value

        value = self.get_query_tab_children_settings_values('display_related_studies')
        self.settings_dict['display_related_studies'] = value

        value = self.get_query_tab_children_settings_values('display_related_assays')
        self.settings_dict['display_related_assays'] = value

        value = self.get_query_tab_children_settings_values('display_related_data_files')
        self.settings_dict['display_related_data_files'] = value

        value = self.get_query_tab_children_settings_values('display_related_publications')
        self.settings_dict['display_related_publications'] = value

        value = self.get_query_tab_children_settings_values('display_related_events')
        self.settings_dict['display_related_events'] = value

        value = self.get_query_tab_children_settings_values('display_project_members')
        self.settings_dict['display_project_members'] = value

        value = self.get_query_tab_children_settings_values('display_project_administrators')
        self.settings_dict['display_project_administrators'] = value

        value = self.get_query_tab_children_settings_values('display_project_asset_housekeepers')
        self.settings_dict['display_project_asset_housekeepers'] = value

        value = self.get_query_tab_children_settings_values('display_project_asset_gatekeepers')
        self.settings_dict['display_project_asset_gatekeepers'] = value

        value = self.get_query_tab_children_settings_values('display_project_organisms')
        self.settings_dict['display_project_organisms'] = value

        value = self.get_query_tab_children_settings_values('display_project_institutions')
        self.settings_dict['display_project_institutions'] = value

        value = self.get_query_tab_children_settings_values('display_project_programmes')
        self.settings_dict['display_project_programmes'] = value

    def get_query_tab_children_settings_values(self,setting):

        if setting == 'display_title':
            return self.query_tab.children[2].children[0].children[0].children[0].children[0].value
        elif setting == 'display_description':
            return self.query_tab.children[2].children[0].children[0].children[0].children[1].value
        elif setting == 'display_model_name':
            return self.query_tab.children[2].children[0].children[0].children[0].children[2].value
        elif setting == 'display_model':
            return self.query_tab.children[2].children[0].children[0].children[0].children[3].value
        elif setting == 'display_download_link':
            return self.query_tab.children[2].children[0].children[0].children[0].children[4].value

        elif setting == 'display_creators':
            return self.query_tab.children[2].children[0].children[0].children[1].children[0].value
        elif setting == 'display_submitter':
            return self.query_tab.children[2].children[0].children[0].children[1].children[1].value
        elif setting == 'display_related_people':
            return self.query_tab.children[2].children[0].children[0].children[1].children[2].value
        elif setting == 'display_related_projects':
            return self.query_tab.children[2].children[0].children[0].children[1].children[3].value
        elif setting == 'display_related_investigations':
            return self.query_tab.children[2].children[0].children[0].children[1].children[4].value
        elif setting == 'display_related_studies':
            return self.query_tab.children[2].children[0].children[0].children[1].children[5].value
        elif setting == 'display_related_assays':
            return self.query_tab.children[2].children[0].children[0].children[1].children[6].value
        elif setting == 'display_related_data_files':
            return self.query_tab.children[2].children[0].children[0].children[1].children[7].value
        elif setting == 'display_related_publications':
            return self.query_tab.children[2].children[0].children[0].children[1].children[8].value
        elif setting == 'display_related_events':
            return self.query_tab.children[2].children[0].children[0].children[1].children[9].value
        elif setting == 'display_project_members':
            return self.query_tab.children[2].children[0].children[0].children[1].children[10].value
        elif setting == 'display_project_administrators':
            return self.query_tab.children[2].children[0].children[0].children[1].children[11].value
        elif setting == 'display_project_asset_housekeepers':
            return self.query_tab.children[2].children[0].children[0].children[1].children[12].value
        elif setting == 'display_project_asset_gatekeepers':
            return self.query_tab.children[2].children[0].children[0].children[1].children[13].value
        elif setting == 'display_project_organisms':
            return self.query_tab.children[2].children[0].children[0].children[1].children[14].value
        elif setting == 'display_project_institutions':
            return self.query_tab.children[2].children[0].children[0].children[1].children[15].value
        elif setting == 'display_project_programmes':
            return self.query_tab.children[2].children[0].children[0].children[1].children[16].value
        else:
            return 'Error'

    def get_id_to_search(self):
        current_index = self.query_tab.selected_index
        topic = self.query_tab._titles.get(str(current_index))
        if topic == 'Document query':
            id =self.search_doc_id
        else :
            id = self.people_search_ID_widget.value
        return id

    def get_type_to_search(self):
        current_index = self.query_tab.selected_index
        topic = self.query_tab._titles.get(str(current_index))
        if topic == 'Document query':
            type =self.doc_option_selected
        else :
            type = 'Person'
        return type

    def get_topic(self):
        current_index = self.query_tab.selected_index
        topic = self.query_tab._titles.get(str(current_index))
        return topic

    def get_setting_options_dict(self):
        self.get_updated_setting_options()
        return self.settings_dict

    def query(self):
        '''
        Displays interactive widgets seperated out into different tabs
        '''
        tab_list = []
        title_list = []
        doc_tab = self.document_tab()
        tab_list.append(doc_tab)
        title_list.append('Document query')
        person_tab=self.person_tab()
        tab_list.append(person_tab)
        title_list.append('Person query')

        settings_tab =self.settings_tab()
        tab_list.append(settings_tab)
        title_list.append('Search settings')

        self.query_tab = self.widget.tab(tab_list,title_list)

        display(self.query_tab)
        desc = 'Convert widgets to text'
        widgets_to_text_button = self.widget.button(desc)
        widgets_to_text_button.on_click(self.on_click_convert)
        display(widgets_to_text_button)
