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
    def __init__(self):
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
        self.json = None

        self.json_handler = JSON_methods()
        # self.search_and_display_handler =  search_and_display()
        self.search_doc_id = None
        self.doc_option_selected = None
        self.current_blob = None

        self.settings_dict_from_file={}
        self.settings_dict = {}


        self.dict_of_users_and_ids = {}
        self.list_of_user_names=[]
        self.list_of_user_ids=[]

        self.search_person_list = []
        self.max_ID_value=0;

        self.name_search_widget = None
        self.people_search_ID_widget = None

        self.query_tab = None
        self.maxProcesses = 5;

        self.load_default_settings()
        self.get_all_FAIRDOM_user_names_and_ID()

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

    def return_dict_of_user_names_and_ids(self):
        return self.dict_of_users_and_ids
    def return_list_of_user_names(self):
        return self.list_of_user_names
    def return_list_of_user_ids(self):
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
        self.query_tab.children[2].children[0].children[0].children[1].children[7].value = self.settings_dict_from_file.get('display_related_publications')
        self.query_tab.children[2].children[0].children[0].children[1].children[8].value = self.settings_dict_from_file.get('display_related_events')

    def load_default_settings(self):
        '''
        Default settings for the search options
        '''

        self.settings_dict['display_title'] = 'Yes'
        self.settings_dict['display_description'] = 'Yes'
        self.settings_dict['display_model_name'] = 'Yes'
        self.settings_dict['display_model'] = 'Yes'
        self.settings_dict['display_download_link'] = 'Yes'

        self.settings_dict['display_creators'] = 'Yes'
        self.settings_dict['display_submitter'] = 'Yes'
        self.settings_dict['display_related_people'] = 'Yes'
        self.settings_dict['display_related_projects'] = 'Yes'
        self.settings_dict['display_related_investigations'] = 'Yes'
        self.settings_dict['display_related_studies'] = 'Yes'
        self.settings_dict['display_related_assays'] = 'Yes'
        self.settings_dict['display_related_publications'] = 'Yes'
        self.settings_dict['display_related_events'] = 'Yes'

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
        elif change['type'] == 'change' and change['name'] == 'value':
            ID=str(change['new'])
            #If ID is in database, display the name associated
            if (change['new'] in self.list_of_user_ids):
                name = self.list_of_user_names[self.list_of_user_ids.index(ID)]
                self.name_search_widget.value = name
            else:
                self.name_search_widget.value = ''
        self.name_search_widget.observe(self.change_made_name_search)

    def change_made_doc_option(self, change):
        '''
        Deals with update in Search Type dropdown widget in the Document Tab
        Store the working document type
        '''
        option = None
        if change['type'] == 'change' and change['name'] == 'value':
            if str(change['new']) == 'Investigation':
                option = 'Investigation'
            elif str(change['new']) == 'Assay':
                option = 'Assay'
            elif str(change['new']) == 'Study':
                option = 'Study'
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

    def document_tab(self):
        '''
        Creates tab relating to searching for a working document
        '''
        doc_option_widget = widgets.Dropdown(
            options=['Investigation', 'Assay', 'Study', 'Data File'],
            value='Investigation',
            description='Search Type:',
        )

        #calls a function that handles updates in the drop down menu
        doc_option_widget.observe(self.change_made_doc_option)
        self.doc_option_selected = doc_option_widget.value

        doc_id_search_widget= widgets.BoundedIntText(
            value=1,
            description='ID number:',
            disabled=False,
            min=1,
            max = sys.maxsize
        )
        #calls a function that handles updates in the int box
        doc_id_search_widget.observe(self.change_made_ID)

        self.search_doc_id = doc_id_search_widget.value

        doc_select_widget_list  = [
            doc_option_widget,
            doc_id_search_widget
                        ]

        #Formats the widgets into a column
        doc_select_widgets_container = widgets.VBox([doc_select_widget_list[0],
                                                    doc_select_widget_list[1]])
        return doc_select_widgets_container

    def person_tab(self):
        '''
        Creates tab relating to searching for a person
        '''
        #Get the list of users sorted in alphbetical order and removes
        #duplicates
        user_list_alphabet_order = []
        user_list_alphabet_order = list(self.list_of_user_names)
        #removes duplicates
        user_list_alphabet_order = list(dict.fromkeys(user_list_alphabet_order))
        #sort alphabetically
        user_list_alphabet_order.sort()
        #add empty string for when the widget is empty
        user_list_alphabet_order.append('')

        self.people_search_ID_widget = widgets.Combobox(
            # value='',
            placeholder='Enter ID',
            options=[],
            description='ID :',
            ensure_option=False,
            disabled=False
        )
        #Handles update to ID widget
        self.people_search_ID_widget.observe(self.change_made_people_search_ID)

        self.name_search_widget = widgets.Combobox(
            # value='',
            placeholder='Enter Name',
            options=user_list_alphabet_order,
            description='Name :',
            ensure_option=False,
            disabled=False,
        )

        #Handles update to name widget
        self.name_search_widget.observe(self.change_made_name_search)

        people_search_widget_list  = [
            self.name_search_widget,
            self.people_search_ID_widget
                        ]

        #Formats the widgets into a column
        people_search_container = widgets.VBox([people_search_widget_list[0], people_search_widget_list[1]])

        return people_search_container

    def general_setting_widgets(self):

        style = {'description_width': '180px'}

        layout = {'width': '600px'}


        title_option = widgets.ToggleButtons(
            options=['Yes', 'No'],
            description='Display Title:',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['', ''],
            style =style,
            layout=layout,
            value = self.settings_dict.get('display_title')
        #     icons=['check'] * 3
        )

        description_option = widgets.ToggleButtons(
            options=['Yes', 'No'],
            description='Display Description:',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['', ''],
            style =style,
            layout=layout,
            value =self.settings_dict.get('display_description')

        #     icons=['check'] * 3
        )


        model_name_option = widgets.ToggleButtons(
            options=['Yes', 'No'],
            description='Display Model Name:',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['', ''],
            style =style,
            layout=layout,
            value = self.settings_dict.get('display_model_name')

        #     icons=['check'] * 3
        )

        model_option = widgets.ToggleButtons(
            options=['Yes', 'No'],
            description='Display Model:',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['', ''],
            style =style,
            layout=layout,
            value = self.settings_dict.get('display_model')

        #     icons=['check'] * 3
        )

        download_link_option = widgets.ToggleButtons(
            options=['Yes', 'No'],
            description='Display Download Link:',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['', ''],
            style =style,
            layout=layout,
            value = self.settings_dict.get('display_download_link')

        #     icons=['check'] * 3
        )


        setting_option_widget_list  = [
            title_option,
            description_option,
            model_name_option,
            model_option,
            download_link_option
                        ]

        column = widgets.VBox([setting_option_widget_list[0],
                                   setting_option_widget_list[1],
                                   setting_option_widget_list[2],
                                   setting_option_widget_list[3],
                                   setting_option_widget_list[4]])


        return column

    def relationship_setting_widgets(self):
            style = {'description_width': '180px'}
            layout = {'width': '600px'}

            creators_option = widgets.ToggleButtons(
                options=['Yes', 'No'],
                description='Display Creator:',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltips=['', ''],
                style =style,
                layout=layout,
                value = self.settings_dict.get('display_creators')

                # value = self.display_title
            #     icons=['check'] * 3
            )

            submitter_option = widgets.ToggleButtons(
                options=['Yes', 'No'],
                description='Display Submitter:',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltips=['', ''],
                style =style,
                layout=layout,
                value = self.settings_dict.get('display_submitter')

                # value = self.display_description

            #     icons=['check'] * 3
            )

            related_people_option = widgets.ToggleButtons(
                options=['Yes', 'No'],
                description='Display People:',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltips=['', ''],
                style =style,
                layout=layout,
                value = self.settings_dict.get('display_related_people')

                # value = self.display_model

            #     icons=['check'] * 3
            )

            related_projects_option = widgets.ToggleButtons(
                options=['Yes', 'No'],
                description='Display Related Projects:',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltips=['', ''],
                style =style,
                layout=layout,
                value = self.settings_dict.get('display_related_projects')

                # value = self.display_model_name

            #     icons=['check'] * 3
            )

            related_investigations_option = widgets.ToggleButtons(
                options=['Yes', 'No'],
                description='Display related investigations:',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltips=['', ''],
                style =style,
                layout=layout,
                value = self.settings_dict.get('display_related_investigations')

                # value = self.display_download_link

            #     icons=['check'] * 3
            )

            related_studies_option = widgets.ToggleButtons(
                options=['Yes', 'No'],
                description='Display related studies:',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltips=['', ''],
                style =style,
                layout=layout,
                value = self.settings_dict.get('display_related_studies')

                # value = self.display_download_link

            #     icons=['check'] * 3
            )

            related_assays_option = widgets.ToggleButtons(
                options=['Yes', 'No'],
                description='Display related assays:',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltips=['', ''],
                style =style,
                layout=layout,
                value = self.settings_dict.get('display_related_assays')

                # value = self.display_download_link

            #     icons=['check'] * 3
            )

            related_publications_option = widgets.ToggleButtons(
                options=['Yes', 'No'],
                description='Display related publications:',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltips=['', ''],
                style =style,
                layout=layout,
                value = self.settings_dict.get('display_related_publications')

                # value = self.display_download_link

            #     icons=['check'] * 3
            )

            related_events_option = widgets.ToggleButtons(
                options=['Yes', 'No'],
                description='Display related events:',
                disabled=False,
                button_style='', # 'success', 'info', 'warning', 'danger' or ''
                tooltips=['', ''],
                style =style,
                layout=layout,
                value = self.settings_dict.get('display_related_events')

                # value = self.display_download_link

            #     icons=['check'] * 3
            )
            setting_option_widget_list  = [
                creators_option,
                submitter_option,
                related_people_option,
                related_projects_option,
                related_investigations_option,
                related_studies_option,
                related_assays_option,
                related_publications_option,
                related_events_option
                            ]

            column = widgets.VBox([setting_option_widget_list[0],
                                   setting_option_widget_list[1],
                                   setting_option_widget_list[2],
                                   setting_option_widget_list[3],
                                   setting_option_widget_list[4],
                                   setting_option_widget_list[5],
                                   setting_option_widget_list[6],
                                   setting_option_widget_list[7],
                                   setting_option_widget_list[8]])


            return column

    def settings_tab(self):
        '''
        Creates tab relating to settings used for searching
        '''

        layout = {'width': '635px'}

        load_settings_option = widgets.Button(
            description='Load Settings',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
            # style =style_right,
            # layout=layout_right,
            # icon='check'
        )

        save_settings_option = widgets.Button(
            description='Save Settings',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
            # style =style_right,
            # layout=layout_right,
            # icon='check'
        )

        load_settings_option.on_click(self.on_click_setting_load_save)
        save_settings_option.on_click(self.on_click_setting_load_save)


        # relationship_setting_options_list = self.relationship_setting_widgets()
        settings_widget_list = [
            load_settings_option,
            save_settings_option
        ]
        general_setting_options_list = self.general_setting_widgets()
        relation_setting_option_list = self.relationship_setting_widgets()
        settings_accordion = widgets.Accordion(
                                    children=[general_setting_options_list,
                                              relation_setting_option_list],
                                              layout = layout)

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

        value = self.get_query_tab_children_settings_values('display_related_publications')
        self.settings_dict['display_related_publications'] = value

        value = self.get_query_tab_children_settings_values('display_related_events')
        self.settings_dict['display_related_events'] = value

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
        elif setting == 'display_related_publications':
            return self.query_tab.children[2].children[0].children[0].children[1].children[7].value
        elif setting == 'display_related_events':
            return self.query_tab.children[2].children[0].children[0].children[1].children[8].value
        else:
            return 'Error'

    def get_id_to_search(self):
        return self.search_doc_id

    def get_type_to_search(self):
        return self.doc_option_selected

    def get_topic(self):
        return self.query_tab._titles.get('0')

    def get_setting_options_dict(self):
        self.get_updated_setting_options()
        return self.settings_dict

    def query(self):
        '''
        Displays interactive widgets seperated out into different tabs
        '''
        doc_tab = self.document_tab()
        person_tab=self.person_tab()
        settings_tab =self.settings_tab()

        self.query_tab = widgets.Tab()
        self.query_tab.children =[doc_tab,
                                  person_tab,
                                  settings_tab]
        self.query_tab.set_title(0, 'Document query')
        self.query_tab.set_title(1, 'Person query')
        self.query_tab.set_title(2, 'Search settings')
        # print(self.query_tab.children[2].children[2].value)
        display(self.query_tab)
