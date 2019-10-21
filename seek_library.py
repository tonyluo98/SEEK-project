import requests
import json
import string
import getpass


import ipywidgets as widgets
# Importing the libraries we need to format the data in a more readable way.
import pandas as pd
from pandas.io.json import json_normalize

from IPython.display import display

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
# 
#
# widgets.IntText(
#     value=7,
#     description='ID number:',
#     disabled=False
# )

# to call s = read()
class read():
    def __init__(self):
        self.base_url = 'https://www.fairdomhub.org'
        self.headers = {"Accept": "application/vnd.api+json",
               "Accept-Charset": "ISO-8859-1"}

        self.search_id = None
        self.option_chosen = None
        self.search_id = None



    def search(self):
        isa_options_widget = widgets.Dropdown(
            options=['Investigation', 'Assay', 'Study'],
            value='Investigation',
            description='Search:',
        )
        isa_options_widget.observe(self.change_made)
        display(isa_options_widget)
        self.option_chosen = str(isa_options_widget.value)
        self.search_id = get_input("Search for Item ID:")
        self.find_project()

    def change_made(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            #print("changed to %s" % change['new'])
            self.option_chosen = str(change['new'])

    def option_type(self):
        #s.option_type() to call
        print(self.option_chosen)

    def id_number_to_find(self):
        print(self.search_id)

    def find_project(self):
        print("IT works")
        display(self.option_type)
        display(self.id_number_to_find)

def find_project():
    #from IPython.core.interactiveshell import InteractiveShell
    #InteractiveShell.ast_node_interactivity = "all"
    project_id = input('ID of project')
    result = json_for_resource('projects',project_id)
    print("Project: " + result['data']['attributes']['title'] + "\n")

    display(result['data']['relationships'])
    files = []
    type = 'data_files'

    for item in result['data']['relationships'][type]['data']:
      j = json_for_resource(item['type'],item['id'])
      files.append({
          'id':j['data']['id'],
          'title':j['data']['attributes']['title'],
      })

    print(str(len(files)) + " found")

    display(json_normalize(files))

def test():
    #from IPython.core.interactiveshell import InteractiveShell
    #InteractiveShell.ast_node_interactivity = "all"
    base_url = 'https://testing.sysmo-db.org'
    #base_url = 'https://sandbox3.fairdomhub.org'

    headers = {"Accept": "application/vnd.api+json",
               "Accept-Charset": "ISO-8859-1"}

    session = requests.Session()
    session.headers.update(headers)
    session.auth = (input('Username:'), getpass.getpass('Password'))
    print('hello')

    data_file_id = 734
    data_file_id
    result = json_for_resource('data_files',data_file_id,session)

    title = result['data']['attributes']['title']

    print(title)


    print(result['data']['attributes'])
    print(result['data']['attributes']['policy'])
    print('bye')
