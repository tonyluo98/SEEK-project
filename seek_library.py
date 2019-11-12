import requests
import json
import string
import getpass
import sys
import io
import ipywidgets as widgets
# Importing the libraries we need to format the data in a more readable way.
import pandas as pd
from pandas.io.json import json_normalize

from IPython.display import display
from IPython.display import HTML
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
        x.read()
        x.Query()
        x.Search()
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

        self.search_id = None
        self.option_chosen = None
        self.search_id = None
        self.current_blob = None

        self.json = None
        self.data = object()
        self.settings_list =None



        self.read_settings_file()


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
        display(isa_options_widget)
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
        display(id_number_to_find)
        self.search_id = id_number_to_find.value

    def search(self):
        '''
        Searches Fairdom for the file based on user input
        '''
        self.load_default_settings()
        self.display_ISA()

    def search_properties(self):
        '''
        Searches Fairdom for the file based on user input
        '''
        self.load_settings()
        self.display_ISA()

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
        self.json = json_for_resource(str(type),str(id))


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

        print(json_methods.get_relationship_creators(self.json))

    def display_datafile(self,):
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
    def get_title(json):
        # print(data.attributes.title)
        return json['data']['attributes']['title']

    def get_description(json):
        # print(data.attributes.description)
        return json['data']['attributes']['description']

    def get_relationship_creators(json):
        return json['data']['relationships']['creators']['data']

    def get_blob(json):
        return json['data']['attributes']['content_blobs']
