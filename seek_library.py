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

# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "all"


def json_for_resource(type, id, session):
    '''
    Helper method for receiving JSON response given an id and type of data
    '''
    base_url = 'https://www.fairdomhub.org'
    #base_url = 'https://testing.sysmo-db.org'
    #base_url = 'https://sandbox3.fairdomhub.org'

    headers = {"Accept": "application/vnd.api+json",
               "Accept-Charset": "ISO-8859-1"}


    r = session.get(base_url + "/" + type + "/" + str(id), headers=headers)

    if (r.status_code != 200):
        print(r.json())

    r.raise_for_status()
    return r.json()

def json_for_resource_parent(type):
    base_url = 'https://www.fairdomhub.org'

    headers = {
      "Accept": "application/vnd.api+json",
      "Accept-Charset": "ISO-8859-1"
    }

    r = requests.get(base_url + "/" + type, headers=headers)
    r.raise_for_status()
    return r.json()

def json_for_resource(type, id):
    '''
    Helper method for receiving JSON response given an id and type of data
    '''
    base_url = 'https://www.fairdomhub.org'
    #base_url = 'https://testing.sysmo-db.org'
    #base_url = 'https://sandbox3.fairdomhub.org'
    headers = {"Accept": "application/vnd.api+json",
           "Accept-Charset": "ISO-8859-1"}
    r = requests.get(base_url + "/" + type + "/" + str(id), headers=headers)
    r.raise_for_status()
    return r.json()


# to call s = read()
class read():
    '''
    Class used to search/browse data on the FairdomHub website
    (https://www.fairdomhub.org)

    To use :

        import seek_library as s

        x= s.read()

        x.query()
        x.search()
        x.search_custom_settings()
    '''
    def __init__(self):
        '''
        Sets up varaiables for class

        Contains details on what the search items are
        '''
        self.base_url = 'https://www.fairdomhub.org'
        self.headers = {"Accept": "application/vnd.api+json",
               "Accept-Charset": "ISO-8859-1"}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.search_setting_type = None
        self.search_topic = None

        self.search_doc_id = None
        self.doc_option_selected = None
        self.search_doc_id = None
        self.current_blob = None

        self.json = None
        self.data = object()
        self.settings_list =None
        self.relationship_person_id =[]


        self.dict_of_users_and_ids = {}
        self.list_of_user_names=[]
        self.list_of_user_ids=[]

        self.search_person_list = []
        self.max_ID_value=0;

        self.name_search_widget = None
        self.people_search_ID_widget = None

        self.query_tab = None
        self.maxProcesses = 5;
        self.read_settings_file()

        self.get_all_FAIRDOM_user_names_and_ID()


    def get_all_FAIRDOM_user_names_and_ID(self):

        peopleJSON = json_methods.get_id_and_name_from_parent(json_methods.get_JSON_from_parent('people'))
        self.iterate_over_json_list_for_name_ID(peopleJSON)
        # print(self.dict_of_users_and_ids)

    def iterate_over_json_list_for_name_ID(self,data):
        self.dict_of_users_and_ids.clear()
        # print(data)
        for value in data:
            list_of_ID =[]
            # print(value)
            name_key=json_methods.get_name_from_people_JSON(value)
            id_value=json_methods.get_ID_from_people_JSON(value)
            # print(name_value)
            # print(id_key)
            # print()
            # id_value=(id_value)
            if int(id_value) > self.max_ID_value:
                self.max_ID_value = int(id_value)

            if name_key in self.dict_of_users_and_ids:
                list_of_ID = self.dict_of_users_and_ids.get(name_key)

            list_of_ID.append(id_value)
            self.dict_of_users_and_ids[name_key] =list_of_ID

            # print(json_methods.get_ID_from_people_JSON(value))
            # print()
            # print()

            self.list_of_user_ids.append(id_value)
            self.list_of_user_names.append(name_key)

        # display(self.list_of_user_names)
        # display(self.list_of_user_ids)

    def read_settings_file(self):
        fn = 'search_settings.txt'
        try:
            file = open(fn, 'r')
        except IOError:
            file = open(fn, 'w')

        try:
            with file as f:
                self.settings_list = f.readlines()

            self.settings_list = [int(value.strip()) for value in self.settings_list]
            result = 1
            file.close()
        except Exception as e:
            print('Error with settings file')
            print('Delete file to fix')
            result = e

        if isinstance(result,Exception) == False:
            self.load_settings()

    def load_settings(self):
        self.display_title = self.settings_list[0]
        self.display_description = self.settings_list[1]
        self.display_model = self.settings_list[2]
        self.display_model_name =self.settings_list[3]
        self.display_download_link = self.settings_list[4]

    def load_default_settings(self):
        self.display_title = 1
        self.display_description = 1
        self.display_model = 1
        self.display_model_name =1
        self.display_download_link = 1


        # print(*settings_list, sep='\n')





    def change_made_name_search(self, change):
        '''
        Checks for any updates in the text box
        '''



        self.people_search_ID_widget.unobserve(self.change_made_people_search_ID)

        if (change['new'] ==''):
            self.people_search_ID_widget.value = ''
        elif change['type'] == 'change' and change['name'] == 'value':
            name_selected = change['new']

            # print('tttttttt')
            # print(name_selected)
            if name_selected in self.dict_of_users_and_ids.keys():
                ID_index_list = self.dict_of_users_and_ids.get(name_selected)
                # print(ID_index_list)
                if len(ID_index_list) > 1:
                    # idWidget.options = ID_index_list
                    self.people_search_ID_widget.value = ''
                    self.people_search_ID_widget.placeholder = 'Choose ID'
                    self.people_search_ID_widget.options = ID_index_list

                else :
                    self.people_search_ID_widget.value = str(ID_index_list[0])
            else :
                self.people_search_ID_widget.value = ''
                self.people_search_ID_widget.options = []


        self.people_search_ID_widget.observe(self.change_made_people_search_ID)


    def change_made_people_search_ID(self, change):
        '''
        Checks for any updates in the text box
        '''

        self.name_search_widget.unobserve(self.change_made_name_search)
        if change['new'] =='':
            self.name_search_widget.value = ''
        elif change['type'] == 'change' and change['name'] == 'value':
            ID=str(change['new'])
            if (change['new'] in self.list_of_user_ids):
                name = self.list_of_user_names[self.list_of_user_ids.index(ID)]
                self.name_search_widget.value = name
            else:
                self.name_search_widget.value = ''
        self.name_search_widget.observe(self.change_made_name_search)

            # print("changed to %s" % change['new'])
            # self.search_doc_id = int(change['new'])

    # def alter_value_in_person_search(self):


    def change_made_doc_option(self, change):
        '''
        Checks for any updates in the dropdown menu
        '''
        option = None
        if change['type'] == 'change' and change['name'] == 'value':
            if str(change['new']) == 'Investigation':
                option = 'investigations'
            elif str(change['new']) == 'Assay':
                option = 'assays'
            elif str(change['new']) == 'Study':
                option = 'studies'
            elif str(change['new']) == 'Data File':
                option = 'data_files'
            #sets the class variable to option
            self.doc_option_selected = option

    def change_made_ID(self, change):
        '''
        Checks for any updates in the text box
        '''
        if change['type'] == 'change' and change['name'] == 'value':
            #print("changed to %s" % change['new'])
            self.search_doc_id = int(change['new'])

    def change_made_search_related_person(self, change):
        '''
        Checks for any updates in the select multiple
        '''
        self.search_person_list = change['new']

    def document_tab(self):
        doc_option_widget = widgets.Dropdown(
            options=['Investigation', 'Assay', 'Study', 'Data File'],
            # value='Investigation',
            description='Search Type:',
        )
        #calls a function that checks for updates in the drop down menu
        doc_option_widget.observe(self.change_made_doc_option)
        # display(doc_option_widget)
        # self.doc_option_selected = str('investigations')

        doc_id_search_widget= widgets.BoundedIntText(
            value=1,
            description='ID number:',
            disabled=False,
            min=1,
            max = sys.maxsize
        )
        #calls a function that checks for updates in the text box
        doc_id_search_widget.observe(self.change_made_ID)
        # display(doc_id_search_widget)
        self.search_doc_id = doc_id_search_widget.value


        doc_select_widget_list  = [
            doc_option_widget,
            doc_id_search_widget
                        ]

        doc_select_widgets_container = widgets.VBox([doc_select_widget_list[0],
                                                    doc_select_widget_list[1]])
        return doc_select_widgets_container

    def person_tab(self):
        #
        #
        # print(self.list_of_user_names[0])
        # print(self.list_of_user_ids[0])
        user_list_alphabet_order = []
        user_list_alphabet_order = self.list_of_user_names[:]
        user_list_alphabet_order = list(dict.fromkeys(user_list_alphabet_order))
        user_list_alphabet_order.sort()
        user_list_alphabet_order.append('')

        # print(self.list_of_user_names)


        self.people_search_ID_widget = widgets.Combobox(
            # value='',
            placeholder='Enter ID',
            options=[],
            description='ID :',
            ensure_option=False,
            disabled=False
        )
        #
        # people_search_ID_widget= widgets.BoundedIntText(
        #     value=1,
        #     description='Person ID :',
        #     disabled=False,
        #     min=1,
        #     max = self.max_ID_value
        # )

        self.people_search_ID_widget.observe(self.change_made_people_search_ID)

        self.name_search_widget = widgets.Combobox(
            # value='',
            placeholder='Enter Name',
            options=user_list_alphabet_order,
            description='Name :',
            ensure_option=False,
            disabled=False
        )
        self.name_search_widget.observe(self.change_made_name_search)

        people_search_widget_list  = [
            self.name_search_widget,
            self.people_search_ID_widget
                        ]

        people_search_container = widgets.VBox([people_search_widget_list[0], people_search_widget_list[1]])

        return people_search_container

    def settings_tab(self):

        style = {'description_width': '150px'}
        layout = {'width': '500px'}

        title_option = widgets.ToggleButtons(
            options=['Yes', 'No'],
            description='Display Title:',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltips=['', ''],
            style =style,
            layout=layout,
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
        #     icons=['check'] * 3
        )


        settings_widget_list  = [
            title_option,
            description_option,
            model_option,
            model_name_option,
            download_link_option
                        ]

        settings_container = widgets.VBox([settings_widget_list[0],
                                           settings_widget_list[1],
                                           settings_widget_list[2],
                                           settings_widget_list[3],
                                           settings_widget_list[4]])

        return settings_container


    def query(self):
        '''
        Displays interactive widgets in forms of a dropdown bar for the TYPE of
        file to search and a text box for the ID of the file.
        Text box doesn't accept numbers less than 1
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


        print(self.query_tab.children[2].children[2].value)
        display(self.query_tab)


    def search(self):
        '''
        Searches Fairdom for the file based on user input
        '''
        self.search_setting_type = 'default'
        clear_output()

        self.load_default_settings()
        self.display_doc()

    def search_custom_settings(self):
        '''
        Searches Fairdom for the file based on user input
        '''
        self.search_setting_type = 'specific'

        clear_output()

        self.load_settings()
        self.display_doc()


    def option_type(self):
        '''
        returns the TYPE of file to search for
        '''
        #s.option_type() to call
        print(self.doc_option_selected)

    def doc_id_search_widget(self):
        '''
        returns the file ID number
        '''
        print(self.search_doc_id)

    def display_doc(self):
        '''
        displays the file by getting the appropriate data from the JSON tags
        '''
        #File ID to search for
        id = self.search_doc_id
        # File type
        type = self.doc_option_selected
        # print(id)
        # print(type)
        # result_datafile = json_for_resource('investigations',id)
        # print(result_datafile)
        #turns the JSON response into a object
        # self._request(str(type),str(id))
        self.json =json_methods.get_JSON(type,id)
        # print(self.json)

        #title and description of file

        title = json_methods.get_title(self.json)
        description = json_methods.get_description(self.json)
        if self.display_title == 1:
            display(HTML('<h1><u>{0}</u></h1>'.format(title)))
        # display(HTML('<p>{0}</p>'.format(description)))
        if self.display_description == 1:
            print(description)

        if type == 'data_files':
            self.display_datafile()

        # print(json_methods.get_relationship_creators(self.json))
        # print(self.json)
        self.display_relationship()

    def display_relationship(self):
        # print(self.json)
        # print()
        # print()
        # print()
        # print()
        #
        # print(json_methods.get_relationship_creators(self.json))
        self.iterate_over_json_list(json_methods.get_relationship_creators(self.json))
        names = self.multiprocess_search(self.relationship_person_id)
        people_relation = self.relationship_drop_box(names)

        relationship_accordian_widget = widgets.Accordion(children=[people_relation])
        relationship_accordian_widget.set_title(0,'related people')
        relationship_accordian_widget.selected_index = None

        relation_people_search_button = widgets.Button(
            description='Search',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
        )

        relationship_widget_list  = [
            relationship_accordian_widget,
            relation_people_search_button
                        ]



        relationshi_people_container = widgets.VBox([relationship_widget_list[0], relationship_widget_list[1]])

        related_info_tab = widgets.Tab()
        related_info_tab.children =[relationshi_people_container,relation_people_search_button]
        related_info_tab.set_title(0, 'Related People')
        related_info_tab.set_title(1, 'Copy ')


        relation_people_search_button.on_click(self.related_people_search)
        display(related_info_tab)

    def relationship_drop_box(self,list_of_names):
        x =list_of_names
        default_value =[]
        default_value.append(x[0])
        relationship_dropdown_widget = widgets.SelectMultiple(
            options=x,
            value=default_value,
            rows=5,
            description='Person ID',
            disabled=False
        )
        relationship_dropdown_widget.observe(self.change_made_search_related_person,names='value')
        return relationship_dropdown_widget

    def iterate_over_json_list(self,data):
        self.relationship_person_id.clear()
        # print(data)
        for value in data:
            # print(value)
            self.relationship_person_id.append(value.get('id'))
            # x = value
            # print(x)
            # for key,value in x.items():
            #     # if key == :
            #         # pass
            #     print('key {!r} -> value {!r}'.format(key, value))

    def display_datafile(self):
        '''
        displays the file by getting the appropriate data from the JSON tags
        '''

        self.current_blob = json_methods.get_blob(self.json)
        link = blob_methods.get_link(self.current_blob)
        filename = blob_methods.get_filename(self.current_blob)

        headers = { "Accept": "text/csv" }
        r = requests.get(link, headers=headers, params={'sheet':'1'})
        r.raise_for_status()
        #gets spreadsheet from data file
        csv = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        if self.display_model_name ==1:
            display(HTML('<h4>File Name: {0}</h4>'.format(filename)))
        # display(filename)
        if self.display_download_link == 1:
            self.download_link()
        if self.display_model ==1:
            display(csv)

    def download_link(self):
        link = blob_methods.get_link(self.current_blob)
        filename = blob_methods.get_filename(self.current_blob)
        download_link = link+"/download"
        print("Download link: " + download_link + "\n")
        HTML("<a href='"+ download_link + "'>Download + " + filename + "</a>")

    def multiprocess_search(self,idNumbers):
        # processesBeingRun =[]
        # maxProcesses =self.maxProcesses
        # if len(idNumbers) < maxProcesses:
        #     maxProcesses = len(idNumbers)
        #
        # for processNumber in range (5)
        #     currentProcess = multiprocessing.Process(target =retrieve_person_name,args=())
        #     currentProcess.start()
        #     processesBeingRun.append(currentProcess)
        #
        # for process in processesBeingRun:
        #     process.join()

        processesBeingRun = Pool(processes = 15)
        dataRec = processesBeingRun.map(self.retrieve_person_name,idNumbers)

        processesBeingRun.close()
        return dataRec

    def retrieve_person_name(self,idNumber):
        personMetaData = json_methods.get_JSON('people',idNumber)
        return json_methods.get_title(personMetaData)

    def related_people_search(self,target):

        if self.search_setting_type == 'default':
            self.search()
        else:
            self.search_custom_settings()
        # for x in range(len(self.search_person_list)):
        #     print(self.search_person_list[x])


class blob_methods():
    '''
    Functions that associate with the blob data
    '''
    def get_link(blob):
        return blob[0]['link']

    def get_filename(blob):
        return blob[0]['original_filename']

class json_methods():
    '''
    Functions that associate with JSON data
    '''
    def get_JSON(type,id):
        return json_for_resource(str(type),str(id))

    def get_JSON_from_parent(type):
        return json_for_resource_parent(str(type))

    def get_title(json):
        # print(data.attributes.title)
        return json['data']['attributes']['title']

    def get_description(json):
        # print(data.attributes.description)
        return json['data']['attributes']['description']

    def get_relationship_creators(json):
        # iterate_over_json_array(json)accordion
        return json['data']['relationships']['creators']['data']

    def get_id_and_name_from_parent(json):
        return json['data']

    def get_ID_from_people_JSON(json):
        return json['id']

    def get_name_from_people_JSON(json):
        return json['attributes']['title']

    def get_person_name(json):
        return json['data']['attributes']['title']

    def get_blob(json):
        return json['data']['attributes']['content_blobs']
