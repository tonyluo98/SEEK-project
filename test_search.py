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
from query import Query
from search import Search
from write import Write

from json_methods import JSON_methods
from widget import Widget
import unittest
from unittest.mock import patch


import os


class TestJSONhandler(unittest.TestCase):

    def setUp(self):
        self.username = 'DEFAULT'
        self.password = 'DEFAULT'
        self.json_handler_OBJ = JSON_methods()
        self.json_handler_OBJ.session = requests.Session()
        self.json_handler_OBJ.session.auth = (self.username, self.password)
        self.search_OBJ = Search(None)
        settings_dict = {'display_title':'True',
                        'display_description':'True'
                        'display_model_name':'True'
                        'display_model':'True'
                        'display_title':'True'
                        'display_download_link':'True'
                            }
        self.search_OBJ.settings_dict = settings_dict
    def tearDown(self):
        pass

    def test_set_json_handler_Method(self):
        json_handler = None
        self.search_OBJ = Search(json_handler)
        self.search_OBJ.set_json_handler(self.json_handler_OBJ)
        self.assertIsInstance(self.search_OBJ.json_handler, JSON_methods)

    def test_search_Method(self):
        self.assertEqual(self.search_OBJ.search(),None)
        self.search_OBJ.topic ='To be implemented'
        self.assertEqual(self.search_OBJ.search(),None)

    def test_search_parameters_Method(self):
        button = None
        self.search_OBJ.on_click_convert(button)



if __name__ == '__main__':
    unittest.main()
