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


    def _loadJSON(self, layerName, layer):
        '''
        Code from Bogdan
        '''

        """Parses the json that each request returns

        Recursively creates an attribute for the read object with the request
        JSON. The attribute contains the structured object with the parsed JSON

        :param layerName: the field that will contain the structure
        :param layer: the json that needs to be parsed
        :type layerName: str
        :type layer: obj
        :returns: void
        :rtype: None

        :Example:

        >>> import SEEK as S
        >>> request = S.read()
        >>> request.request('assays',100)
        >>> request._loadJSON(request, request.json['data'])
        >>> request.data
        <function SEEK.read._loadJSON.<locals>.<lambda>()>
        >>> request.data.attributes.description
        Proton fluxes ensue a change in the membrane potential to which the
        potassium uptake responds. The membrane potential changes depend on the
        extrusion of protons, buffering capacities of the media and experimental
        parametes.
        """

        try:
            layerName = lambda: None

            # if hasattr(layer, 'items'):

            for key, value in layer.items():


                if hasattr(value, 'items'):

                    # print(str(key))
                    setattr(layerName, key, self._loadJSON(key, value))
                else:
                    # print(str(key))
                    setattr(layerName, key, value)

            setattr(self,'data', layerName)

            # else:
            #     for item in range(0, len(layer)):

            #         for key, value in layer[item].items():

            #             if hasattr(value, 'items'):

            #                 setattr(layerName, key, self.loadJSON(key, value))
            #             else:

            #                 setattr(layerName, key, value)
            return layerName
        except Exception as e:
            print(str(e))

    def _request(self, type, id):
        '''
        Code from Bogdan
        '''

        """Uses python requests to query the SEEK API, then parses the JSON
        using the loadJSON method.

        :param type: type of the element eg: assays/studie/data_files
        :param id: id of the element
        :type type: str
        :type id: str
        :returns: True if request fulfils or False otherwise
        :rtype: bool

        :Example:

        >>> import SEEK as S
        >>> request = S.read()
        >>> request._request('assays',100)
        >>> request.data
        <function SEEK.read._loadJSON.<locals>.<lambda>()>
        >>> request.data.attributes.description
        Proton fluxes ensue a change in the membrane potential to which the
        potassium uptake responds. The membrane potential changes depend on the
        extrusion of protons, buffering capacities of the media and experimental
        parametes.
        """

        r = None

        try:
            # print(self.base_url + "/" + type + "/" + id)

            r = self.session.get(self.base_url + "/" + type + "/" + id)
            # r = self.session.get("https://fairdomhub.org/data_files/2222")


            self.session.close()
            r.close()

            if r.status_code != 200:
                return False
            self.json = r.json()
            self._loadJSON(self, self.json['data'])
            self.requestList = []

            return True

        except Exception as e:
            print(str(e))

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
        self.option_chosen = str(isa_options_widget.value)

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
        self.display_datafile()

    def change_made_ISA(self, change):
        '''
        Checks for any updates in the dropdown menu
        '''
        choice = None
        if change['type'] == 'change' and change['name'] == 'value':
            #print("changed to %s" % change['new'])

            #assigns equivalent url address term
            if str(change['new']) == 'Investigation':
                choice = 'investigation'
            elif str(change['new']) == 'Assay':
                choice = 'assay'
            elif str(change['new']) == 'Investigation':
                choice = 'investigation'
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

    def display_datafile(self):
        '''
        displays the file by getting the appropriate data from the JSON tags
        '''
        #File ID to search for
        datafile_id = self.search_id
        # File type
        type = self.option_chosen
        # result_datafile = json_for_resource('data_files',datafile_id)

        #turns the JSON response into a object
        self._request(str(type),str(datafile_id))

        #title and description of file
        title = json_methods.get_title(self.data)
        description = json_methods.get_description(self.data)
        #Gets blob data
        self.current_blob = json_methods.get_blob(self.data)
        link = blob_methods.get_link(self.current_blob)
        filename = blob_methods.get_filename(self.current_blob)

        headers = { "Accept": "text/csv" }
        r = requests.get(link, headers=headers, params={'sheet':'1'})
        r.raise_for_status()
        #gets spreadsheet from data file
        csv = pd.read_csv(io.StringIO(r.content.decode('utf-8')))

        display(HTML('<h1><u>{0}</u></h1>'.format(title)))
        # display(HTML('<p>{0}</p>'.format(description)))
        print(description)
        display(HTML('<h4>File Name: {0}</h4>'.format(filename)))
        # display(filename)
        display(csv)

    def download_link(self):
        link = self.current_blob['link']
        filename = self.current_blob['original_filename']
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
    def get_title(data):
        # print(data.attributes.title)
        return data.attributes.title

    def get_description(data):
        # print(data.attributes.description)
        return data.attributes.description


    def get_blob(data):
        return data.attributes.content_blobs
