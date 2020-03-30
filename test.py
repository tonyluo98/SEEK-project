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
from json_methods import JSON_methods
from widget import Widget
from write import Write
import unittest
from unittest.mock import patch


import os


class TestJSONhandler(unittest.TestCase):
    #
    # def setUpClass(cls):
    #     pass
    #
    # def tearDownClass(cls):
    #     pass

    def setUp(self):
        self.username = 'DEFAULT'
        self.password = 'DEFAULT'
        self.json_handler_OBJ = JSON_methods()
        self.json_handler_OBJ.session = requests.Session()
        self.json_handler_OBJ.session.auth = (self.username, self.password)

        self.json_no_policy = {}
        self.json_no_policy['data'] = {}
        self.json_no_policy['data']['type'] = 'investigations'
        self.json_no_policy['data']['attributes'] = {}
        self.json_no_policy['data']['attributes']['title'] = 'title'
        self.json_no_policy['data']['attributes']['description'] = 'desc'

        self.json_person = {}
        self.json_person['attributes'] = {}
        self.json_person['attributes']['title'] = 'name'


        self.json = {}
        self.json['id'] = '1'
        self.json['jsonapi'] = {}
        self.json['jsonapi']['version'] = '1.0'

        self.json['data'] = {}
        self.json['data']['type'] = 'investigations'
        self.json['data']['attributes'] = {}
        self.json['data']['attributes']['title'] = 'title'
        self.json['data']['attributes']['description'] = 'desc'
        self.json['data']['attributes']['policy']= {}
        self.json['data']['attributes']['policy']['access']= 'view'
        self.json['data']['attributes']['assay_class'] = 'class'
        self.json['data']['attributes']['assay_type'] = {}
        self.json['data']['attributes']['assay_type']['uri'] = 'uri'
        self.json['data']['attributes']['technology_type'] = {}
        self.json['data']['attributes']['technology_type']['uri'] = 'uri'
        self.json['data']['attributes']['members'] = {}
        self.json['data']['relationships']= {}
        self.json['data']['relationships']['creators'] ={}
        self.json['data']['relationships']['creators']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['submitter'] ={}
        self.json['data']['relationships']['submitter']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['people'] ={}
        self.json['data']['relationships']['people']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['projects'] ={}
        self.json['data']['relationships']['projects']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['investigations'] ={}
        self.json['data']['relationships']['investigations']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['studies'] ={}
        self.json['data']['relationships']['studies']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['assays'] ={}
        self.json['data']['relationships']['assays']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['data_files'] ={}
        self.json['data']['relationships']['data_files']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['project_administrators'] ={}
        self.json['data']['relationships']['project_administrators']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['asset_housekeepers'] ={}
        self.json['data']['relationships']['asset_housekeepers']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['asset_gatekeepers'] ={}
        self.json['data']['relationships']['asset_gatekeepers']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['organisms'] ={}
        self.json['data']['relationships']['organisms']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['institutions'] ={}
        self.json['data']['relationships']['institutions']['data']= {id: "136",type: "people"}
        self.json['data']['relationships']['programmes'] ={}
        self.json['data']['relationships']['programmes']['data']= {id: "136",type: "people"}

    def tearDown(self):
        pass

    def test_set_json_handler_Method(self):
        json_handler = None
        search = Search(json_handler)
        search.set_json_handler(self.json_handler_OBJ)
        self.assertIsInstance(search.json_handler, JSON_methods)

    # @patch('SEEK._get_input', return_value=
    #                                PROT_DEFAULT_AUTHENTICATION_STRING)
    # @patch('getpass.getpass', return_value=PROT_DEFAULT_AUTHENTICATION_STRING)
    def test_auth_request_Method(self):
        self.assertEqual(self.json_handler_OBJ.session.auth,
                        (self.username, self.password))

    def test_new_session_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.new_session(),
                              requests.Session)

    def test_change_url_Method(self):
        self.json_handler_OBJ.change_url('1')
        self.assertEqual(self.json_handler_OBJ.chosen_url,'https://www.fairdomhub.org')

    def test_check_webpage_status_Method(self):
        with patch('json_methods.requests.Session') as mocked_get:
            mocked_get.status_code = 403
            self.assertEqual(self.json_handler_OBJ.check_webpage_status(mocked_get),
                            False)
            mocked_get.status_code = 401
            self.assertEqual(self.json_handler_OBJ.check_webpage_status(mocked_get),
                            False)
            mocked_get.status_code = 422
            self.assertEqual(self.json_handler_OBJ.check_webpage_status(mocked_get),
                            False)
            mocked_get.status_code = 406
            self.assertEqual(self.json_handler_OBJ.check_webpage_status(mocked_get),
                            False)
            mocked_get.status_code = 404
            self.assertEqual(self.json_handler_OBJ.check_webpage_status(mocked_get),
                            False)
            mocked_get.status_code = 200
            self.assertEqual(self.json_handler_OBJ.check_webpage_status(mocked_get),
                            True)

    def test_get_list_of_user_ids_Method(self):
        self.json_handler_OBJ.list_of_user_ids=['1','2','3']
        list = ['1','2','3']
        self.assertEqual(self.json_handler_OBJ.list_of_user_ids,list)

    def test_get_list_of_user_names_Method(self):
        self.json_handler_OBJ.list_of_user_ids=['a','b','c']
        list = ['a','b','c']
        self.assertEqual(self.json_handler_OBJ.list_of_user_ids,list)

    def test_get_data_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_data(self.json),dict)

    def test_get_type_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_type(self.json),str)

    def test_get_title_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_title(self.json),str)

    def test_get_description_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_description(self.json),str)

    def test_get_assay_class_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_assay_class(self.json),str)

    def test_get_assay_type_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_assay_type(self.json),dict)

    def test_get_assay_type_uri_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_assay_type_uri(self.json),str)

    def test_get_assay_tech_type_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_assay_tech_type(self.json),dict)

    def test_get_assay_tech_type_uri_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_assay_tech_type_uri(self.json),str)

    def test_get_relationship_creators_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_relationship_creators(self.json),dict)

    def test_get_relationship_submitters_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_relationship_submitters(self.json),dict)

    def test_get_relationship_people_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_relationship_people(self.json),dict)

    def test_get_relationship_projects_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_relationship_projects(self.json),dict)

    def test_get_relationship_investigations_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_relationship_investigations(self.json),dict)

    def test_get_relationship_studies_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_relationship_studies(self.json),dict)

    def test_get_relationship_assays_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_relationship_assays(self.json),dict)

    def test_get_relationship_data_files_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_relationship_data_files(self.json),dict)

    def test_get_project_members_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_project_members(self.json),dict)

    def test_get_project_admins_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_project_admins(self.json),dict)

    def test_get_asset_HK_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_asset_HK(self.json),dict)

    def test_get_asset_GK_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_asset_GK(self.json),dict)

    def test_get_organisms_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_organisms(self.json),dict)

    def test_get_project_institutions_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_project_institutions(self.json),dict)

    def test_get_project_programmes_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_project_programmes(self.json),dict)

    def test_check_relationship_exists_Method(self):
        self.assertEqual(self.json_handler_OBJ.check_relationship_exists(self.json,'assays'),True)
        self.assertEqual(self.json_handler_OBJ.check_relationship_exists(self.json,'rnd'),False)

    def test_check_policy_exists_Method(self):
        self.assertEqual(self.json_handler_OBJ.check_policy_exists(self.json),True)
        self.assertEqual(self.json_handler_OBJ.check_policy_exists(self.json_no_policy),False)

    def test_get_ID_from_people_JSON_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_ID_from_people_JSON(self.json),str)

    def test_get_name_from_people_JSON_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_name_from_people_JSON(self.json_person),str)

    def test_get_person_name_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_person_name(self.json),str)

    def test_get_version_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_version(self.json),str)

    def test_get_public_access_Method(self):
        self.assertIsInstance(self.json_handler_OBJ.get_public_access(self.json),str)

class TestWrite(unittest.TestCase):

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

class TestSearch(unittest.TestCase):

    def setUp(self):
        self.username = 'DEFAULT'
        self.password = 'DEFAULT'
        self.json_handler_OBJ = JSON_methods()
        self.json_handler_OBJ.session = requests.Session()
        self.json_handler_OBJ.session.auth = (self.username, self.password)
        self.search_OBJ = Search(None)
        settings_dict = {'display_title': 'True',
                        'display_description': 'True',
                        'display_model_name': 'True',
                        'display_model': 'True',
                        'display_title': 'True',
                        'display_download_link': 'True'
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
        self.assertEqual(self.search_OBJ.search_parameters('topic','1','type',[],[],[]),None)

    def test_on_click_convert_Method(self):
        button = None
        self.search_OBJ.title = 'title'
        self.search_OBJ.desc = 'desc'
        self.search_OBJ.model_name = 'model name'
        self.search_OBJ.download_link_text = 'link'
        self.search_OBJ.on_click_convert(button)
        self.assertEqual(self.search_OBJ.title,'title')

    def test_getKeysOfDict_Method(self):
        self.assertNotIsInstance(self.search_OBJ.getKeysOfDict(self.search_OBJ.settings_dict),dict)

    def test_getValuesOfDict_Method(self):
        self.assertNotIsInstance(self.search_OBJ.getValuesOfDict(self.search_OBJ.settings_dict),dict)

    def test_relationship_drop_box_Method(self):
        self.assertNotEqual(self.search_OBJ.relationship_drop_box([],0,'desc'),None)
        list_of_names = ['a','b','c','d','e']
        self.assertNotEqual(self.search_OBJ.relationship_drop_box(list_of_names,0,'desc'),None)
        list_of_names = ['a','b']
        self.assertNotEqual(self.search_OBJ.relationship_drop_box(list_of_names,0,'desc'),None)

    def test_iterate_over_json_list_Method(self):
        return_value= None
        self.assertEqual(return_value, None)
        data = {}
        return_value = self.search_OBJ.iterate_over_json_list(data,[])
        self.assertNotEqual(return_value, None)

    def test_iterate_over_json_list_person_Method(self):
        return_value= None
        self.assertEqual(return_value, None)
        data = {}
        return_value = self.search_OBJ.iterate_over_json_list_person(data,[])
        self.assertNotEqual(return_value, None)

class TestQuery(unittest.TestCase):

    def setUp(self):

        self.username = 'DEFAULT'
        self.password = 'DEFAULT'
        self.json_handler_OBJ = JSON_methods()
        self.json_handler_OBJ.session = requests.Session()
        self.json_handler_OBJ.session.auth = (self.username, self.password)
        self.query_OBJ = Query(self.json_handler_OBJ )
        settings_dict = {'display_title': 'True',
                        'display_description': 'True',
                        'display_model_name': 'True',
                        'display_model': 'True',
                        'display_title': 'True',
                        'display_download_link': 'True'
                            }
        # self.query_OBJ.settings_dict = settings_dict
    def tearDown(self):
        pass

    def test_set_json_handler_Method(self):
        json_handler = None
        self.query_OBJ = Query(json_handler)
        self.query_OBJ.set_json_handler(self.json_handler_OBJ)
        self.assertIsInstance(self.query_OBJ.json_handler, JSON_methods)

    def test_get_list_of_user_names_Method(self):
        self.assertIsInstance(self.query_OBJ.get_list_of_user_names(),list)

    def test_get_list_of_user_ids_Method(self):
        self.assertIsInstance(self.query_OBJ.get_list_of_user_ids(),list)

    def test_get_dict_of_user_names_and_ids_Method(self):
        self.assertIsInstance(self.query_OBJ.get_dict_of_user_names_and_ids(),dict)

    def test_read_settings_file_Method(self):
        self.query_OBJ.read_settings_file()
        self.assertNotEqual(self.query_OBJ.settings_dict,None)

    def test_load_default_settings_Method(self):
        self.query_OBJ.load_default_settings()
        self.assertNotEqual(self.query_OBJ.settings_dict,None)

    def test_document_tab_Method(self):
        self.assertNotEqual(self.query_OBJ.document_tab(),None)

    def test_person_tab_Method(self):
        self.assertNotEqual(self.query_OBJ.person_tab(),None)

    def test_general_setting_widgets_Method(self):
        self.assertNotEqual(self.query_OBJ.general_setting_widgets(),None)

    def test_relationship_setting_widgets_Method(self):
        self.assertNotEqual(self.query_OBJ.relationship_setting_widgets(),None)

    def test_settings_tab_Method(self):
        self.assertNotEqual(self.query_OBJ.settings_tab(),None)



if __name__ == '__main__':

    unittest.main()
