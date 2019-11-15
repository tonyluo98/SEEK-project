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

def get_input(prompt):
    '''
    Get user input
    '''
    return input(prompt)

def get_number_input():
    '''
    Get user input
    '''
    return id_number_to_find

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
        x.search_properties()
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
        self.search_method = None
        self.search_topic = None

        self.search_id = None
        self.option_chosen = None
        self.search_id = None
        self.current_blob = None

        self.json = None
        self.data = object()
        self.settings_list =None
        self.relationship_person_id =[]


        self.dict_of_users_and_ids = {}
        self.list_of_user_names=[]
        self.list_of_user_ids=[]

        self.search_person_list = []
        self.max_id=0;


        self.maxProcesses = 5;
        self.read_settings_file()

        self.get_all_FAIRDOM_user_names_ID()


    def get_all_FAIRDOM_user_names_ID(self):

        usersJSON = json_methods.get_id_and_name_from_parent(json_methods.get_JSON_from_parent('people'))
        self.iterate_over_json_list_for_name_ID(usersJSON)
        # print(self.dict_of_users_and_ids)

    def iterate_over_json_list_for_name_ID(self,data):
        self.dict_of_users_and_ids.clear()
        # print(data)
        for value in data:
            # print(value)
            id_key=json_methods.get_ID_from_person_parent(value)
            name_value=json_methods.get_name_from_person_parent(value)
            # print(name_value)
            # print(id_key)
            # print()
            id_key=int(id_key)
            if id_key > self.max_id:
                self.max_id = id_key
            self.dict_of_users_and_ids[id_key] =name_value
            # print(json_methods.get_ID_from_person_parent(value))
            # print()
            # print()

        self.list_of_user_ids=list(self.dict_of_users_and_ids.keys())
        self.list_of_user_names=list(self.dict_of_users_and_ids.values())

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
        self.display_desc = self.settings_list[1]
        self.display_model = self.settings_list[2]
        self.display_model_name =self.settings_list[3]
        self.display_download_link = self.settings_list[4]

    def load_default_settings(self):
        self.display_title = 1
        self.display_desc = 1
        self.display_model = 1
        self.display_model_name =1
        self.display_download_link = 1


        # print(*settings_list, sep='\n')

    def query(self):
        '''
        Displays interactive widgets in forms of a dropdown bar for the TYPE of
        file to search and a text box for the ID of the file.
        Text box doesn't accept numbers less than 1
        '''
        isa_options_widget = widgets.Dropdown(
            options=['Investigation', 'Assay', 'Study', 'Data File'],
            value='Investigation',
            description='Search Type:',
        )
        #calls a function that checks for updates in the drop down menu
        isa_options_widget.observe(self.change_made_ISA)
        # display(isa_options_widget)
        self.option_chosen = str('investigations')

        id_number_to_find= widgets.BoundedIntText(
            value=1,
            description='ID number:',
            disabled=False,
            min=1,
            max = sys.maxsize
        )
        #calls a function that checks for updates in the text box
        id_number_to_find.observe(self.change_made_ID)
        # display(id_number_to_find)
        self.search_id = id_number_to_find.value


        ISAwidgets  = [
            isa_options_widget,
            id_number_to_find
                        ]

        ISAContainerBox = widgets.VBox([ISAwidgets[0], ISAwidgets[1]])

        #
        #
        # print(self.list_of_user_names[0])
        # print(self.list_of_user_ids[0])
        sortedUserList = []
        sortedUserList = self.list_of_user_names[:]
        sortedUserList.sort()
        # print(self.list_of_user_names)
        nameBoxSearch = widgets.Combobox(
            value='Vid A',
            placeholder='Enter Name',
            options=sortedUserList,
            description='Person Name :',
            ensure_option=True,
            disabled=False
        )
        nameBoxSearch.observe(self.change_made_person_name)


        personIDSearch= widgets.BoundedIntText(
            value=1,
            description='Person ID :',
            disabled=False,
            min=1,
            max = self.max_id
        )

        personIDSearch.observe(self.change_made_person_name)

        PersonwWidgets  = [
            nameBoxSearch,
            personIDSearch
                        ]

        personContainerBox = widgets.VBox([PersonwWidgets[0], PersonwWidgets[1]])



        query_tab = widgets.Tab()
        query_tab.children =[ISAContainerBox,personContainerBox]
        query_tab.set_title(0, 'ISA query')
        query_tab.set_title(1, 'Person query ')


        #
        # print(self.list_of_user_names[0])
        # print(self.list_of_user_ids[0])

        display(query_tab)

    def search(self):
        '''
        Searches Fairdom for the file based on user input
        '''
        self.search_method = 'default'
        clear_output()

        self.load_default_settings()
        self.display_ISA()

    def search_properties(self):
        '''
        Searches Fairdom for the file based on user input
        '''
        self.search_method = 'specific'

        clear_output()

        self.load_settings()
        self.display_ISA()

    def change_made_person_name(self, change):
        '''
        Checks for any updates in the text box
        '''
        if change['type'] == 'change' and change['name'] == 'value':
            print("changed to %s" % change['new'])
            print("Old to %s" % change['old'])

        #
        # print(self.list_of_user_ids)
        # print()
        # print()
        # print()
        # print('---------------')
        # print(change['new'].get('value'))
        # print(self.list_of_user_names[0])
        # # print()
        # if change['old'] is not '':

        nameChosen = change['new'].get('value')
        print('tttttttt')
        print(nameChosen)
        newIDIndex = self.list_of_user_ids[self.list_of_user_names.index(nameChosen)]
        print(newIDIndex)



    def change_made_person_ID(self, change, nameWidget):
        '''
        Checks for any updates in the text box
        '''
        if change['type'] == 'change' and change['name'] == 'value':
            print("changed to %s" % change['new'])
            # self.search_id = int(change['new'])

    # def alter_value_in_person_search(self):


    def change_made_ISA(self, change):
        '''
        Checks for any updates in the dropdown menu
        '''
        choice = None
        if change['type'] == 'change' and change['name'] == 'value':
            #print("changed to %s" % change['new'])

            #assigns equivalent url address term
            if str(change['new']) == 'Investigation':
                choice = 'investigations'
            elif str(change['new']) == 'Assay':
                choice = 'assays'
            elif str(change['new']) == 'Study':
                choice = 'studies'
            elif str(change['new']) == 'Data File':
                choice = 'data_files'
            #sets the class variable to option
            self.option_chosen = choice
            # print('Chosen ' +self.option_chosen)

    def change_made_ID(self, change):
        '''
        Checks for any updates in the text box
        '''
        if change['type'] == 'change' and change['name'] == 'value':
            #print("changed to %s" % change['new'])
            self.search_id = int(change['new'])

    def change_made_search_related_person(self, change):
        '''
        Checks for any updates in the select multiple
        '''
        self.search_person_list = change['new']

    def option_type(self):
        '''
        returns the TYPE of file to search for
        '''
        #s.option_type() to call
        print(self.option_chosen)

    def id_number_to_find(self):
        '''
        returns the file ID number
        '''
        print(self.search_id)

    def display_ISA(self):
        '''
        displays the file by getting the appropriate data from the JSON tags
        '''
        #File ID to search for
        id = self.search_id
        # File type
        type = self.option_chosen
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
        if self.display_desc == 1:
            print(description)

        if type == 'data_files':
            self.display_datafile()

        # print(json_methods.get_relationship_creators(self.json))
        # print(self.json)
        self.relationship_display()

    def relationship_display(self):
        # print(self.json)
        # print()
        # print()
        # print()
        # print()
        #
        # print(json_methods.get_relationship_creators(self.json))
        self.iterate_over_json_list(json_methods.get_relationship_creators(self.json))
        names = self.multiprocess_search(self.relationship_person_id)
        personRelations = self.relationship_drop_box(names)

        relationshipAccordion = widgets.Accordion(children=[personRelations])
        relationshipAccordion.set_title(0,'related people')
        relationshipAccordion.selected_index = None

        relatedPeopleSearchButton = widgets.Button(
            description='Search',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
        )



        listOfWidgets  = [
            relationshipAccordion,
            relatedPeopleSearchButton
                        ]



        containerBox = widgets.VBox([listOfWidgets[0], listOfWidgets[1]])

        relatedInfoTab = widgets.Tab()
        relatedInfoTab.children =[containerBox,relatedPeopleSearchButton]
        relatedInfoTab.set_title(0, 'Related People')
        relatedInfoTab.set_title(1, 'Copy ')


        relatedPeopleSearchButton.on_click(self.related_people_search)
        display(relatedInfoTab)

    def relationship_drop_box(self,listOfNames):
        x =listOfNames
        defaultValue =[]
        defaultValue.append(x[0])
        dropdownRelationship = widgets.SelectMultiple(
            options=x,
            value=defaultValue,
            rows=5,
            description='Person ID',
            disabled=False
        )
        dropdownRelationship.observe(self.change_made_search_related_person,names='value')
        return dropdownRelationship

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

        if self.search_method == 'default':
            self.search()
        else:
            self.search_properties()
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

    def get_ID_from_person_parent(json):
        return json['id']

    def get_name_from_person_parent(json):
        return json['attributes']['title']

    def get_person_name(json):
        return json['data']['attributes']['title']

    def get_blob(json):
        return json['data']['attributes']['content_blobs']
