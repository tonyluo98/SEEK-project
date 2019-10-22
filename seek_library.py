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
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"



def json_for_resource(type, id, session):
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
    base_url = 'https://www.fairdomhub.org'
    #base_url = 'https://testing.sysmo-db.org'
    #base_url = 'https://sandbox3.fairdomhub.org'
    headers = {"Accept": "application/vnd.api+json",
           "Accept-Charset": "ISO-8859-1"}
    r = requests.get(base_url + "/" + type + "/" + str(id), headers=headers)
    r.raise_for_status()
    return r.json()

def get_input(prompt):
    return input(prompt)

def get_number_input():

    return id_number_to_find


# to call s = read()
class read():
    def __init__(self):
        self.base_url = 'https://www.fairdomhub.org'
        self.headers = {"Accept": "application/vnd.api+json",
               "Accept-Charset": "ISO-8859-1"}

        self.search_id = None
        self.option_chosen = None
        self.search_id = None
        self.current_blob = None



    def query(self):
        isa_options_widget = widgets.Dropdown(
            options=['Investigation', 'Assay', 'Study', 'Data File'],
            value='Investigation',
            description='Search Type:',
        )
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
        id_number_to_find.observe(self.change_made_ID)
        display(id_number_to_find)
        self.search_id = id_number_to_find.value

    def search(self):
        self.display_datafile()

    def change_made_ISA(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            #print("changed to %s" % change['new'])
            self.option_chosen = str(change['new'])

    def change_made_ID(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            #print("changed to %s" % change['new'])
            self.search_id = int(change['new'])

    def option_type(self):
        #s.option_type() to call
        print(self.option_chosen)

    def id_number_to_find(self):
        print(self.search_id)

    def display_datafile(self):
        datafile_id = self.search_id
        result_datafile = json_for_resource('data_files',datafile_id)
        title = json_methods.get_title(result_datafile)
        description = json_methods.get_description(result_datafile)

        self.current_blob = json_methods.get_blob(result_datafile)
        link = blob_methods.get_link(self.current_blob)
        filename = blob_methods.get_filename(self.current_blob)

        headers = { "Accept": "text/csv" }
        r = requests.get(link, headers=headers, params={'sheet':'1'})
        r.raise_for_status()

        csv = pd.read_csv(io.StringIO(r.content.decode('utf-8')))

        display(HTML('<h1><u>{0}</u></h1>'.format(title)))
        display(HTML('<p>{0}</p>'.format(description)))
        # display()
        display(HTML('<h4>{0}</h4>'.format(filename)))
        # display(filename)
        display(csv)

    def download_link(self):
        link = self.current_blob['link']
        filename = self.current_blob['original_filename']
        download_link = link+"/download"
        print("Download link: " + download_link + "\n")
        HTML("<a href='"+ download_link + "'>Download + " + filename + "</a>")
class blob_methods():
    def get_link(blob):
        return blob['link']

    def get_filename(blob):
        return blob['original_filename']

class json_methods():
    def get_title(r):
        return r['data']['attributes']['title']

    def get_description(r):
        return r['data']['attributes']['description']

    def get_blob(r):
        return r['data']['attributes']['content_blobs'][0]
