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
    Functions that associate with:
            Splitting JSON data
            Getting JSON from FAIRDOM
            Sending JSON to FAIRDOM
            Stores authorisation of user if provided
    '''
    def __init__(self):
        self.max_ID_value = 0
        self.list_of_user_ids =[]
        self.list_of_user_names =[]
        self.people_JSON = None
        self.urls = []
        # URL for sandbox and official website
        self.urls.append('https://www.fairdomhub.org')
        self.urls.append('https://sandbox3.fairdomhub.org')
        self.chosen_url = self.urls[0]

        self.headers  = {"Accept": "application/vnd.api+json",
                         "Connection": "close",
                         "Accept-Charset": "ISO-8859-1"}
        self.write_headers = {"Content-type": "application/vnd.api+json",
                              "Accept": "application/vnd.api+json",
                              "Accept-Charset": "ISO-8859-1"}
        self.session = None

    def auth_request(self):
        '''
        Get user login details

        RETURNS N/A
        '''
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.auth = (input('Username:'), getpass.getpass('Password'))

    def new_session(self,auth = None):
        '''
        Create new session

        RETURNS session
        '''
        request = requests.Session()
        request.headers.update(self.headers)
        if auth != None :
            request.auth = auth
        return(request)
    def change_url(self,url_index):
        '''
        Changes URL for getting and sending JSON to

        RETURNS N/A
        '''
        self.chosen_url = self.urls[int(url_index)-1]

    def check_webpage_status(self,r):
        '''
        Check if response is valid or not

        RETURNS boolean
        '''
        if r.status_code == 403:
            print('Not visible for you as you do not have access')
            return False
        elif r.status_code ==401 :
            print('Login details wrong')
            return False
        elif r.status_code == 422:
            print('No permission to post at this url')
            return False
        elif r.status_code == 406:
            print('Not acceptable')
            return False
        elif r.status_code == 404:
            print('Web Page does not exist')
            return False
        elif r.status_code != 200:
            print(r.status_code)
            print('Web site does not exist')
            print('or web site is down')
            try:
                sys.exit(1)
            except Exception as e:
                raise
            return False
        return True

    def json_for_resource_type_id(self,type, id):
        '''
        Helper method for receiving JSON response given an id and type of data

        RETURNS : JSON recieved
                  Empty list if invalid
        '''
        base_url = self.chosen_url
        # Create a new session
        if self.session == None:
            requester = self.new_session()
        else :
            requester = self.new_session(self.session.auth)
        # Get JSON of that type and id
        r = requester.get(base_url + "/" + type + "/" + str(id), headers=self.headers)
        # Close session
        r.close()
        # Check response
        valid = self.check_webpage_status(r)
        if valid:
            r.raise_for_status()
            return r.json()
        else:
            print('invalid for {} {}'.format(type,id))
            return []


    def json_for_resource_type(self,type):
        '''
        Helper method for receiving JSON response given just the type of data

        RETURNS : JSON recieved
                  Empty list if invalid
        '''
        base_url = self.chosen_url
        # Create a new session
        if self.session == None:
            requester = self.new_session()
        else :
            requester = self.new_session(self.session.auth)
        # Get JSON of that type and id
        r = requester.get(base_url + "/" + type, headers=self.headers)
        # Close session
        r.close()
        # Check response
        valid = self.check_webpage_status(r)
        if valid:
            r.raise_for_status()
            return r.json()
        else:
            print('invalid for {}'.format(type))
            return []

    def post_json(self,type,hash,post_type,id = None):
        '''
        Post JSON to Fairdom
        JSON posted is either for a new post or to update a existing post

        RETURNS ID of uploaded JSON
        '''
        # Sandbox url is used for project purposes
        base_url = 'https://sandbox3.fairdomhub.org'
        # URL based on file type
        if type == 'Investigation':
            url = base_url +'/investigations'
        elif type == 'Study':
            url = base_url +'/studies'
        elif type == 'Assay':
            url = base_url +'/assays'
        elif type == 'Data File':
            url = base_url +'/data_files'
        else :
            print('NEW TYPE UNEXPECTED')
        # Requires user login details
        if self.session == None:
            print('Login details required')
        else :
            # Set Headers for upload
            r = None
            requester = self.new_session(self.session.auth)
            requester.headers.update(self.write_headers)
            # POST command for putting new data
            # PUT command for updating data
            if post_type == 'Create':
                r = requester.post(url, json=hash)
            else :
                url = url +'/'+id
                r = requester.put(url, json=hash)
            # Check valid
            # print(url)
            # print(hash)
            valid = self.check_webpage_status(r)
            if valid:
                r.raise_for_status()
                json_posted =r.json()
                id = json_posted['data']['id']
                print('SUCCESSFULLY POSTED')
                if post_type == 'Create':
                    url = url +'/'+id
                    print(url)
                else :
                    print(url)
                # Returns ID of posted JSON
                return id
            else:
                return None

    def get_csv_sheet(self,link):
        '''
        Gets the excel sheet and converts to csvv and returns the first sheet
        '''
        headers = { "Accept": "text/csv" }
        # Create a new session
        if self.session == None:
            requester = self.new_session()
        else :
            requester = self.new_session(self.session.auth)
        # get excel sheet
        r = requester.get(link, headers=headers, params={'sheet':'1'})
        # Close session
        r.close()
        # Check response
        valid = self.check_webpage_status(r)
        if valid:
            r.raise_for_status()
            # convert to csv
            csv = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
            return csv
        else:
            print('invalid for {}'.format(type))
            print('Can not display file ')
            print('Reason could be : permission is not allowed ')
            print('                  file is not a excel sheet ')

    def get_user_id(self):
        '''
        METHOD TO BE IMPLEMENTED WHEN NEW API IS RELEASED

        Helper method for receiving JSON response

        RETURNS JSON for user
        '''
        base_url = self.chosen_url
        # Create Session
        if self.session == None:
            requester = self.new_session()
        else :
            requester = self.new_session(self.session.auth)

        requester = self.new_session(self.session.auth)


        r = requester.get(base_url + "/whoami?format=json", headers=self.headers)
        urlTest = base_url+"/whoami?format=json"
        print(urlTest)
        print(r)
        r.close()
        valid = self.check_webpage_status(r)

        if valid:
            r.raise_for_status()
            return r.json()
        else:
            return []

    def get_JSON(self,type,id):
        '''
        Get JSON based on type and id
        '''
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
        elif type == 'Project People':
            type = 'people'

        # GET JSON
        if id != 'None':
            return self.json_for_resource_type_id(str(type),
                                                  str(id))
        elif id == 'None':
            return self.json_for_resource_type(str(type))

    def get_dictionary_of_user_and_id(self):
        '''
        RETURNS names and corresponding ID of all users
        '''
        people_meta_data_json = self.get_JSON('people','None')
        if people_meta_data_json != []:
            self.people_JSON = self.get_data(people_meta_data_json)
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
        else:
            return {}

    def get_list_of_user_ids(self):
        '''
        User IDS are taken
        RETURNS user IDS
        '''
        temp_list = list(self.list_of_user_ids)
        self.list_of_user_ids = []
        return temp_list

    def get_list_of_user_names(self):
        '''
        User IDS are taken
        RETURNS user names
        '''
        temp_list = list(self.list_of_user_names)
        self.list_of_user_names = []
        return temp_list

    def get_data(self,json):
        '''
        RETURNS 'data' of JSON
        '''
        return json['data']

    def get_type(self,json):
        '''
        RETURNS 'type' of JSON [data]
        '''
        return json['data']['type']

    def get_title(self,json):
        '''
        RETURNS 'title' of JSON [data]['attributes']
        '''
        return json['data']['attributes']['title']

    def get_description(self,json):
        '''
        RETURNS 'description' of JSON [data]['attributes']
        '''
        desc = json['data']['attributes']['description']
        if desc == None:
            return ''
        else :
            return desc

    def get_assay_class(self,json):
        '''
        RETURNS 'assay_class' of JSON [data]['attributes']
        '''
        return json['data']['attributes']['assay_class']

    def get_assay_type(self,json):
        '''
        RETURNS 'assay_type' of JSON [data]['attributes']
        '''
        return json['data']['attributes']['assay_type']

    def get_assay_type_uri(self,json):
        '''
        RETURNS 'assay_type' of JSON [data]['attributes']
        '''
        return json['data']['attributes']['assay_type']['uri']

    def get_assay_tech_type(self,json):
        '''
        RETURNS 'technology_type' of JSON [data]['attributes']
        '''
        return json['data']['attributes']['technology_type']

    def get_assay_tech_type_uri(self,json):
        '''
        RETURNS 'technology_type' of JSON [data]['attributes']
        '''
        return json['data']['attributes']['technology_type']['uri']

    def get_relationship_creators(self,json):
        '''
        RETURNS 'data' of JSON ['relationships']['creators']['data']
        '''
        return json['data']['relationships']['creators']['data']

    def get_relationship_submitters(self,json):
        '''
        RETURNS 'data' of JSON ['relationships']['submitter']['data']
        '''
        return json['data']['relationships']['submitter']['data']

    def get_relationship_people(self,json):
        '''
        RETURNS 'data' of JSON ['relationships']['people']['data']
        '''
        return json['data']['relationships']['people']['data']

    def get_relationship_projects(self,json):
        '''
        JSON for related projects differs based on which JSON you are viewing
        JSON for related projects is written either :
                                                      'projects'
                                                      'project'
        plural version ('projects') is written everywhere but within a project
        json

        RETURNS 'data' of JSON ['relationships']['project']['data']
        '''

        bool = self.check_relationship_exists(json,'projects')
        bool2 = self.check_relationship_exists(json,'project')
        if bool == True:
            # List of projects is the format in the JSON
            return json['data']['relationships']['projects']['data']
        elif bool2 == True :
            # Only one exist therefore it is converted to a list
            convertDictToList = []
            convertDictToList.append(json['data']['relationships']['project']['data'])
            return convertDictToList
        else :
            return []

    def get_relationship_investigations(self,json):
        '''
        JSON for related investigations differs based on which JSON you are
        viewing
        JSON for related investigations is written either :
                                                      'investigations'
                                                      'investigation'
        plural version ('investigations') is written everywhere but within a
        investigation json

        RETURNS 'data' of JSON ['relationships']['project']['data']
        '''
        bool = self.check_relationship_exists(json,'investigations')
        bool2 = self.check_relationship_exists(json,'investigation')
        if bool == True:
            # List of investigations is the format in the JSON
            return json['data']['relationships']['investigations']['data']
        elif bool2 == True :
            # Only one exist therefore it is converted to a list
            convertDictToList = []
            convertDictToList.append(json['data']['relationships']['investigation']['data'])
            return convertDictToList
        else :
            return []

    def get_relationship_studies(self,json):
        '''
        JSON for related studies differs based on which JSON you are viewing
        JSON for related studies is written either :
                                                      'studies'
                                                      'study'
        plural version ('studies') is written everywhere but within a
        study json

        RETURNS 'data' of JSON ['relationships']['project']['data']
        '''
        bool = self.check_relationship_exists(json,'studies')
        bool2 = self.check_relationship_exists(json,'study')

        if bool == True :
            # List of studies is the format in the JSON
            return json['data']['relationships']['studies']['data']
        elif bool2 == True :
            # Only one exist therefore it is converted to a list
            convertDictToList = []
            convertDictToList.append(json['data']['relationships']['study']['data'])
            return convertDictToList
        else :
            return []

    def get_relationship_assays(self,json):
        '''
        JSON for related assays differs based on which JSON you are viewing
        JSON for related assays is written either :
                                                      'assays'
                                                      'assay'
        plural version ('investigations') is written everywhere but within a
        investigation json

        RETURNS 'data' of JSON ['relationships']['project']['data']
        '''
        bool = self.check_relationship_exists(json,'assays')
        bool2 = self.check_relationship_exists(json,'assay')

        if bool == True:
            # List of assays is the format in the JSON
            return json['data']['relationships']['assays']['data']
        elif bool2 == True :
            # Only one exist therefore it is converted to a list
            convertDictToList = []
            convertDictToList.append(json['data']['relationships']['assay']['data'])
            return convertDictToList
        else :
            return []

    def get_relationship_data_files(self,json):
        '''
        Checks if data files exist in that JSON

        RETURNS 'data' of JSON ['relationships']['data_files']['data']
        '''
        bool = self.check_relationship_exists(json,'data_files')

        if bool == True:
            return json['data']['relationships']['data_files']['data']
        else :
            return []

    def get_project_members(self,json):
        '''
        RETURNS 'data' of JSON ['attributes']['members']
        '''
        return json['data']['attributes']['members']

    def get_project_admins(self,json):
        '''
        RETURNS 'data' of
                JSON ['data']['relationships']['project_administrators']['data']
        '''
        return json['data']['relationships']['project_administrators']['data']

    def get_asset_HK(self,json):
        '''
        RETURNS 'data' of
                JSON ['data']['relationships']['asset_housekeepers']['data']
        '''
        return json['data']['relationships']['asset_housekeepers']['data']

    def get_asset_GK(self,json):
        '''
        RETURNS 'data' of
                JSON ['data']['relationships']['asset_gatekeepers']['data']
        '''
        return json['data']['relationships']['asset_gatekeepers']['data']

    def get_organisms(self,json):
        '''
        RETURNS 'data' of
                JSON ['data']['relationships']['organisms']['data']
        '''
        return json['data']['relationships']['organisms']['data']

    def get_project_institutions(self,json):
        '''
        RETURNS 'data' of
                JSON ['data']['relationships']['institutions']['data']
        '''
        return json['data']['relationships']['institutions']['data']

    def get_project_programmes(self,json):
        '''
        RETURNS 'data' of
                JSON ['data']['relationships']['programmes']['data']
        '''
        return json['data']['relationships']['programmes']['data']

    def check_relationship_exists(self,json,type):
        '''
        Check if a relation exists in the JSON
        '''
        relations = json['data']['relationships']
        if type in relations:
            return True
        else:
            return False

    def check_policy_exists(self,json):
        '''
        Check if a relation exists in the JSON
        '''
        type = 'policy'
        attribute = json['data']['attributes']
        if type in attribute:
            return True
        else:
            return False

    def get_ID_from_people_JSON(self,json):
        '''
        RETURNS 'id' of json
        '''
        return json['id']

    def get_name_from_people_JSON(self,json):
        '''
        RETURNS 'title' of json ['attributes']
        '''
        return json['attributes']['title']

    def get_person_name(self,json):
        '''
        RETURNS 'title' of json ['data']['attributes']
        '''
        return json['data']['attributes']['title']

    def get_version(self,json):
        '''
        RETURNS 'version' of json ['jsonapi']['version']
        '''
        return json['jsonapi']['version']

    def get_public_access(self,json):
        '''
        RETURNS 'access' of json ['data']['attributes']['policy']['access']
        '''
        bool = self.check_policy_exists(json)
        if bool == True:
            return json['data']['attributes']['policy']['access']
        else :
            return('view')

    def get_blob(self,json):
        '''
        RETURNS 'content_blobs' of json ['data']['attributes']
        '''
        return json['data']['attributes']['content_blobs']

    def get_link(self,blob):
        '''
        RETURNS 'link' of json
        '''
        return blob[0]['link']

    def get_url(self,blob):
        '''
        RETURNS 'url' of json
        '''
        try:
            url = blob[0]['url']
            if url == None :
                url = ''
            return url
        except Exception as e:

            url = ''
            return url

    def get_filename(self,blob):
        '''
        RETURNS 'original_filename' of json
        '''
        return blob[0]['original_filename']

    def get_license(self,json):
        '''
        RETURNS 'license' of json['data']['attributes']
        '''
        return json['data']['attributes']['license']
