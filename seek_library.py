import requests
import json
import string

import getpass

# Importing the libraries we need to format the data in a more readable way.
import pandas as pd
from pandas.io.json import json_normalize


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

def find_project():
    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.ast_node_interactivity = "all"

    from IPython.display import display

    project_id = 60

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
