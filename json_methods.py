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



class JSON_methods():
    '''
    Functions that associate with JSON data
    '''
    def __init__(self):
        self.max_ID_value = 0
        self.list_of_user_ids =[]
        self.list_of_user_names =[]
        self.people_JSON = None

    def check_webpage_status(self,r):

        if r.status_code != 200:
            print('Web site does not exist')
            return False
        return True

    def json_for_resource_type_id_session(self,type, id, session):
        '''
        Helper method for receiving JSON response given an id, type of data and
        session
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

    def json_for_resource_type_id(self,type, id):
        '''
        Helper method for receiving JSON response given an id and type of data
        '''
        base_url = 'https://www.fairdomhub.org'
        #base_url = 'https://testing.sysmo-db.org'
        #base_url = 'https://sandbox3.fairdomhub.org'
        headers = {"Accept": "application/vnd.api+json",
               "Accept-Charset": "ISO-8859-1"}
        r = requests.get(base_url + "/" + type + "/" + str(id), headers=headers)
        valid = self.check_webpage_status(r)

        if valid:
            r.raise_for_status()
            return r.json()
        else:
            print('invalid for {} type {}'.format(id,type))
            return []


            # sys.exit(0)

    def json_for_resource_type(self,type):
        '''
        Helper method for receiving JSON response given just the type of data
        '''
        base_url = 'https://www.fairdomhub.org'

        headers = {
          "Accept": "application/vnd.api+json",
          "Accept-Charset": "ISO-8859-1"
        }

        r = requests.get(base_url + "/" + type, headers=headers)
        r.raise_for_status()
        return r.json()

    def get_JSON(self,type,id,session):


        if type == 'Project':
            type = 'projects'
        elif type == 'Investigation':
            type = 'investigations'
        elif type == 'Study':
            type = 'studies'
        elif type == 'Assay':
            type = 'assays'
        elif type == 'Data File':
            type = 'data_files'
        elif type == 'Project Organisms':
            type = 'organisms'
        elif type == 'Project Institute':
            type = 'institutions'
        elif type == 'Project Program':
            type = 'programmes'
        elif type == 'Person':
            type = 'people'

        if session == 'None' and id != 'None':
            return self.json_for_resource_type_id(str(type),
                                             str(id))
        elif id == 'None':
            return self.json_for_resource_type(str(type))
        else:
            return self.json_for_resource_type_id_session(str(type),
                                                     str(id),
                                                     str(session))

    def get_dictionary_of_user_and_id(self):
        '''
        returns names and corresponding ID of all users
        '''
        self.people_JSON = self.get_data(self.get_JSON('people','None','None'))
        dict_of_users_and_ids = {}
        for value in self.people_JSON:
            list_of_ID =[]
            name_key=self.get_name_from_people_JSON(value)
            id_value=self.get_ID_from_people_JSON(value)
            #Find out the biggest ID number of users
            if int(id_value) > self.max_ID_value:
                self.max_ID_value = int(id_value)

            #This checks if the user name is a duplicate
            #If the name is a duplicate, then the value in the dictionary will
            #be a list of different IDs, corresponding to different users with
            #the same name
            if name_key in dict_of_users_and_ids:
                list_of_ID = dict_of_users_and_ids.get(name_key)
            list_of_ID.append(id_value)

            #Add details to dictionary
            #   key = user name
            #   value = ID
            dict_of_users_and_ids[name_key] =list_of_ID

            #List of names and IDs
            self.list_of_user_ids.append(id_value)
            self.list_of_user_names.append(name_key)


        return dict_of_users_and_ids

    def get_list_of_user_ids(self):
        temp_list = list(self.list_of_user_ids)
        self.list_of_user_ids = []
        return temp_list

    def get_list_of_user_names(self):
        temp_list = list(self.list_of_user_names)
        self.list_of_user_names = []
        return temp_list

    def get_data(self,json):
        return json['data']

    def get_title(self,json):
        # print(data.attributes.title)
        return json['data']['attributes']['title']

    def get_description(self,json):
        # print(data.attributes.description)
        return json['data']['attributes']['description']

    def get_relationship_creators(self,json):
        # iterate_over_json_array(json)accordion
        # print(json)
        return json['data']['relationships']['creators']['data']

    def get_relationship_submitters(self,json):
        return json['data']['relationships']['submitter']['data']

    def get_relationship_people(self,json):
        return json['data']['relationships']['people']['data']

    def get_relationship_projects(self,json):
        bool = self.check_relationship_exists(json,'projects')
        bool2 = self.check_relationship_exists(json,'project')
        if bool == True:
            return json['data']['relationships']['projects']['data']
        elif bool2 == True :
            convertDictToList = []
            convertDictToList.append(json['data']['relationships']['project']['data'])
            return convertDictToList
        else :
            return []

    def get_relationship_investigations(self,json):
        '''
        inconsistent json as investigation has no s
        '''
        bool = self.check_relationship_exists(json,'investigations')
        bool2 = self.check_relationship_exists(json,'investigation')
        if bool == True:
            return json['data']['relationships']['investigations']['data']
        elif bool2 == True :
            convertDictToList = []
            convertDictToList.append(json['data']['relationships']['investigation']['data'])
            return convertDictToList
        else :
            return []

    def get_relationship_studies(self,json):
        bool = self.check_relationship_exists(json,'studies')
        bool2 = self.check_relationship_exists(json,'study')

        if bool == True :
            return json['data']['relationships']['studies']['data']
        elif bool2 == True :
            convertDictToList = []
            convertDictToList.append(json['data']['relationships']['study']['data'])
            return convertDictToList
        else :
            return []

    def get_relationship_assays(self,json):
        bool = self.check_relationship_exists(json,'assays')
        bool2 = self.check_relationship_exists(json,'assay')

        if bool == True:
            return json['data']['relationships']['assays']['data']
        elif bool2 == True :
            convertDictToList = []
            convertDictToList.append(json['data']['relationships']['assay']['data'])
            return convertDictToList
        else :
            return []

    def get_project_members(self,json):
        # print(json['data']['attributes']['members'])
        return json['data']['attributes']['members']

    def get_project_admins(self,json):
        return json['data']['relationships']['project_administrators']['data']

    def get_asset_HK(self,json):
        return json['data']['relationships']['asset_housekeepers']['data']

    def get_asset_GK(self,json):
        return json['data']['relationships']['asset_gatekeepers']['data']

    def get_organisms(self,json):
        return json['data']['relationships']['organisms']['data']

    def get_project_institutions(self,json):
        return json['data']['relationships']['institutions']['data']

    def get_project_programmes(self,json):
        return json['data']['relationships']['programmes']['data']

    def check_relationship_exists(self,json,type):
        relations = json['data']['relationships']
        if type in relations:
            return True
        else:
            return False

    def get_ID_from_people_JSON(self,json):
        return json['id']

    def get_name_from_people_JSON(self,json):
        return json['attributes']['title']

    def get_person_name(self,json):
        return json['data']['attributes']['title']

    def get_blob(self,json):
        return json['data']['attributes']['content_blobs']

    def get_link(self,blob):
        return blob[0]['link']

    def get_filename(self,blob):
        return blob[0]['original_filename']
