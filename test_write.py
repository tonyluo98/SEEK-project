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
        self.write_OBJ = Write(None)

    def tearDown(self):
        pass

    def test_set_json_handler_Method(self):
        json_handler = None
        self.write_OBJ = Write(json_handler)
        self.write_OBJ.set_json_handler(self.json_handler_OBJ)
        self.assertIsInstance(self.write_OBJ.json_handler, JSON_methods)

    def test_data_file_hash_Method(self):
        return_value = self.write_OBJ.data_file_hash('title','desc','view','1','licence','url','filename')
        self.assertIsInstance(return_value, dict)

    def test_assay_hash_Method(self):
        return_value = self.write_OBJ.assay_hash('title','desc','view','1','assay_class','assay_type','assay_tech_type')
        self.assertIsInstance(return_value, dict)

    def test_study_hash_Method(self):
        return_value = self.write_OBJ.study_hash('title','desc','view','1')
        self.assertIsInstance(return_value, dict)

    def test_investigation_hash_Method(self):
        return_value = self.write_OBJ.investigation_hash('title','desc','view','1')
        self.assertIsInstance(return_value, dict)

    def test_post_tab_creation_Method(self):
        self.assertEqual(self.write_OBJ.create_tab, None)
        self.write_OBJ.post_tab_creation('desc','Create')
        self.assertNotEqual(self.write_OBJ.create_tab, None)
        self.write_OBJ.post_tab_creation('desc','Update')
        self.assertNotEqual(self.write_OBJ.create_tab, None)

    def test_doc_write_Method(self):
        self.assertEqual(self.write_OBJ.doc_write_tab, None)
        self.write_OBJ.doc_write('Create')
        self.assertNotEqual(self.write_OBJ.doc_write_tab, None)
        self.write_OBJ.doc_write('Update')
        self.assertNotEqual(self.write_OBJ.doc_write_tab, None)

    def test_compulsory_fields_Method(self):
        return_value= None
        self.assertEqual(return_value, None)
        return_value = self.write_OBJ.compulsory_fields()
        self.assertNotEqual(return_value, None)

    def test_data_file_fields_Method(self):
        return_value= None
        self.assertEqual(return_value, None)
        return_value = self.write_OBJ.data_file_fields()
        self.assertNotEqual(return_value, None)

    def test_optional_fields_Method(self):
        return_value= None
        self.assertEqual(return_value, None)
        return_value = self.write_OBJ.data_file_fields()
        self.assertNotEqual(return_value, None)

    def test_assay_fields_Method(self):
        return_value= None
        self.assertEqual(return_value, None)
        return_value = self.write_OBJ.assay_fields()
        self.assertNotEqual(return_value, None)

    def test_iterate_over_json_list_Method(self):
        return_value= None
        self.assertEqual(return_value, None)
        data = {}
        return_value = self.write_OBJ.iterate_over_json_list(data)
        self.assertNotEqual(return_value, None)

if __name__ == '__main__':
    unittest.main()
