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



class Requester():
    '''
    Functions that associate with JSON data
    '''
    def __init__(self,auth = None):
        self.urls = []
        self.urls.append('https://www.fairdomhub.org')
        self.urls.append('https://sandbox3.fairdomhub.org')
        self.chosen_url = self.urls[0]
        self.headers  = {"Accept": "application/vnd.api+json",
                         "Connection": "close",
                         "Accept-Charset": "ISO-8859-1"}
        self.write_headers = {"Content-type": "application/vnd.api+json",
                              "Accept": "application/vnd.api+json",
                              "Connection": "close",
                              "Accept-Charset": "ISO-8859-1"}
        self.session = None
        # self.session = requests.Session()
        # self.session.headers.update(self.headers)
        # self.session.auth = auth

    def auth_request(self):
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.auth = (input('Username:'), getpass.getpass('Password'))

    def new_session(self,auth = None):
        request = requests.Session()
        request.headers.update(self.headers)
        if auth != None :
            request.auth = auth
        return(request)

    def change_url(self,url_index):
        self.chosen_url = self.urls[int(url_index)-1]

    def check_webpage_status(self,r):
        if r.status_code == 403:
            print('Not visible for you as you do not have access')
            return False
        elif r.status_code == 422:
            print('No permission to post at this url')
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
        '''
        base_url = self.chosen_url
        #base_url = 'https://testing.sysmo-db.org'
        #base_url =
        # headers = {"Accept": "application/vnd.api+json",
        #        "Accept-Charset": "ISO-8859-1"}
        if self.session == None:
            requester = self.new_session()
        else :
            requester = self.new_session(self.session.auth)
        r = requester.get(base_url + "/" + type + "/" + str(id), headers=self.headers)
        # if self.session == None:
        #     r = requests.get(base_url + "/" + type + "/" + str(id),
        #                      headers=self.headers)
        # else :
        #     r = self.session.get(base_url + "/" + type + "/" + str(id),
        #                          headers=self.headers)
        r.close()

        valid = self.check_webpage_status(r)

        if valid:
            r.raise_for_status()
            return r.json()
        else:
            print('invalid for {} {}'.format(type,id))
            return []


            # sys.exit(0)

    def json_for_resource_type(self,type):
        '''
        Helper method for receiving JSON response given just the type of data
        '''
        base_url = self.chosen_url

        headers = {
          "Accept": "application/vnd.api+json",
          "Accept-Charset": "ISO-8859-1"
        }

        if self.session == None:
            requester = self.new_session()
        else :
            requester = self.new_session(self.session.auth)

        r = requester.get(base_url + "/" + type, headers=self.headers)

        # if self.session == None:
        #     r = requests.get(base_url + "/" + type, headers=self.headers)
        # else :
        #     r = self.session.get(base_url + "/" + type, headers=self.headers)
        r.close()
        valid = self.check_webpage_status(r)

        if valid:
            r.raise_for_status()
            return r.json()
        else:
            return []

    def post_json(self,type,hash):
        base_url = 'https://sandbox3.fairdomhub.org'
        if type == 'Investigation':
            url = base_url +'/investigations'
        elif type == 'Study':
            url = base_url +'/studies'
        elif type == 'Assay':
            url = base_url +'/assays'
        if self.session == None:
            self.auth_request()
        requester = self.new_session(self.session.auth)
        requester.headers.update(self.write_headers)
        r = requester.post(url, json=hash)
        valid = self.check_webpage_status(r)
        if valid:
            r.raise_for_status()
            # print('END')
            # print()
            # print(r.json())
            json_posted =r.json()
            print(json_posted)
            id = json_posted['data']['id']
            return id
        else:
            # return []
            pass
