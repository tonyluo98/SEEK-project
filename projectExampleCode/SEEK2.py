"""
TESTING THE
Package SEEK - THE SEEK NOTEBOOK
___________________

Third Year Project, Bogdan Gherasim, The University of Manchester, 2019
"""
import getpass
from io import StringIO
import ipywidgets as widgets
import os
import pandas
import sys
import SEEK
import time
import unittest
from unittest import TestCase
from unittest.mock import patch


PROT_DEFAULT_AUTHENTICATION_STRING = "DEFAULT"

class TestSEEK(TestCase):

    def setUp(self):

        self.auth = (PROT_DEFAULT_AUTHENTICATION_STRING,
                    PROT_DEFAULT_AUTHENTICATION_STRING)

        self.testOBJ = SEEK.read(self.auth)

        self.testWriteOBJ = SEEK.write(self.auth)

        self.goodFormat_RequestList = [{'id':'281','type':'investigations'},
                                       {'id':'953','type':'assays'}]

        self.empty_RequestList = [{}]

        self.badRequest_RequestList = [{'id':'1','type':'wrong type'}]

        self.badFormat_RequestList = {'id':'1','type':'assays',
                                      'id':'2','type':'assays'}

    def tearDown(self):

        del self.auth

        del self.testOBJ

        del self.goodFormat_RequestList

        del self.badFormat_RequestList



    @patch("SEEK._get_input", return_value="some input")
    def test_get_input_Method(self, input):

        self.assertEqual(SEEK._get_input("Prompt:"), "some input")

    @patch("SEEK._get_input_testing", return_value="some other input")
    def test_get_input_testing_Method(self, input):

        self.assertEqual(SEEK._get_input_testing("Prompt:"), 'some other input')

    @patch('SEEK._get_input', return_value=
                                   PROT_DEFAULT_AUTHENTICATION_STRING)
    @patch('getpass.getpass', return_value=PROT_DEFAULT_AUTHENTICATION_STRING)
    def test_init_WithAuth(self, username, password):

        self.testOBJ.session.auth = SEEK.auth()
        self.assertEqual(self.testOBJ.session.auth,
                        (PROT_DEFAULT_AUTHENTICATION_STRING,
                        PROT_DEFAULT_AUTHENTICATION_STRING))

    @patch('SEEK._get_input', return_value=
                                   PROT_DEFAULT_AUTHENTICATION_STRING)
    @patch('getpass.getpass', return_value=PROT_DEFAULT_AUTHENTICATION_STRING)
    def test_init_WithoutAuth(self, username, password):

        self.testOBJ = SEEK.read()

        self.assertEqual(self.testOBJ.session.auth,
                         (PROT_DEFAULT_AUTHENTICATION_STRING,
                          PROT_DEFAULT_AUTHENTICATION_STRING))

    @patch('SEEK._get_input', return_value="1")
    def test_relationsFormat(self, relNumber):

        JSON = {}
        JSON['data'] = {}
        JSON["data"]["relationships"] = {}

        SEEK._relationsFormat(JSON, 'creators', 'assay')

        result = [{'id': 1, 'type': 'creators'}]
        self.assertEqual(JSON['data']['relationships']['creators']['data'],
                                        result)

    @patch('SEEK._get_input', return_value='1')
    def test_studyFormat(self, val):

        JSON = {}
        JSON['data'] = {}
        JSON['data']['type'] = 'studies'
        JSON['data']['attributes'] = {}
        JSON['data']['attributes']['title'] = '1'
        JSON['data']['attributes']['description'] = '1'
        JSON['data']['attributes']['policy'] = {'access': '1', 'permissions': [{'resource': {'id': '1','type': 'people'},'access': 'manage'}]}
        JSON['data']['relationships'] = {}
        JSON['data']['relationships']['investigation'] = {}
        JSON['data']['relationships']['investigation']['data'] = {'id' : '1', 'type' : 'investigations'}

        JSON["data"]["attributes"]["other_creators"] = '1'

        JSON['data']['attributes']['experimentalists'] = '1'
        JSON['data']['attributes']['person_responsible_id'] = '1'

        SEEK._relationsFormat(JSON, 'assays', 'study')
        SEEK._relationsFormat(JSON, 'creators', 'study')
        SEEK._relationsFormat(JSON, 'data_files', 'study')
        SEEK._relationsFormat(JSON, 'documents', 'study')
        SEEK._relationsFormat(JSON, 'models', 'study')
        SEEK._relationsFormat(JSON, 'people', 'study')
        SEEK._relationsFormat(JSON, 'projects', 'study')
        SEEK._relationsFormat(JSON, 'publications', 'study')
        SEEK._relationsFormat(JSON, 'sops', 'study')

        studyJSON = SEEK._studyFormat('1', '1')
        self.assertEqual(JSON, studyJSON)

    @patch('SEEK._get_input', return_value='1')
    def test_investigationFormat(self, val):

        JSON = {}
        JSON['data'] = {}
        JSON['data']['type'] = '1'
        JSON['data']['attributes'] = {}
        JSON['data']['attributes']['title'] = '1'
        JSON['data']['attributes']['description'] = '1'
        JSON['data']['relationships'] = {}



        SEEK._relationsFormat(JSON, 'assays', 'study')
        SEEK._relationsFormat(JSON, 'creators', 'study')
        SEEK._relationsFormat(JSON, 'data_files', 'study')
        SEEK._relationsFormat(JSON, 'documents', 'study')
        SEEK._relationsFormat(JSON, 'models', 'study')
        SEEK._relationsFormat(JSON, 'people', 'study')
        SEEK._relationsFormat(JSON, 'projects', 'study')
        SEEK._relationsFormat(JSON, 'publications', 'study')
        SEEK._relationsFormat(JSON, 'sops', 'study')
        SEEK._relationsFormat(JSON, 'studies', 'investigation')
        SEEK._relationsFormat(JSON, 'submitters', 'investigation')

        investigationJSON = SEEK._investigationFormat()
        self.assertEqual(JSON, investigationJSON)

    @patch('SEEK._get_input', return_value='10')
    def test_assayFormat(self, val):

        JSON = {}
        JSON['data'] = {}
        JSON['data']['type'] = 'assays'
        JSON['data']['attributes'] = {}
        JSON['data']['attributes']['title'] = '1'
        JSON['data']['attributes']['description'] = '1'
        JSON['data']['attributes']['policy'] = {'access':'1', 'permissions': []}
        JSON["data"]["attributes"]["other_creators"] = '1'

        JSON["data"]["attributes"]["assay_class"] = {}
        JSON["data"]["attributes"]["assay_class"]["key"] = '1'

        JSON["data"]["attributes"]["assay_type"] = {}
        JSON["data"]["attributes"]["assay_type"]["uri"] = '1'

        JSON["data"]["attributes"]["technology_type"] = {}
        JSON["data"]["attributes"]["technology_type"]["uri"] = '1'

        JSON["data"]["relationships"] = {}


        SEEK._relationsFormat(JSON, "data_files", "assay")
        SEEK._relationsFormat(JSON, "documents", "assay")

        JSON["data"]["relationships"]["investigation"] = {}
        JSON["data"]["relationships"]["investigation"]["data"] = {"id": '1', "type":"investigations"}

        SEEK._relationsFormat(JSON, "models", "assay")
        SEEK._relationsFormat(JSON, "people", "assay")
        SEEK._relationsFormat(JSON, "publications", "assay")
        SEEK._relationsFormat(JSON, "sops", "assay")

        JSON["data"]["relationships"]["study"] = {}
        JSON["data"]["relationships"]["study"]["data"] = {"id": '1', "type":"studies"}

        SEEK._relationsFormat(JSON, "organisms", "assay")

        assayJSON = SEEK._assayFormat("1","1", "1")
        self.assertEqual(JSON, assayJSON)

    @patch('SEEK._get_input', return_value='10')
    def test_dataFileFormat(self, val):

        JSON = {}
        JSON['data'] = {}
        JSON['data']['type'] = 'data_files'
        JSON['data']['attributes'] = {}
        JSON['data']['attributes']['title'] = '1'

        JSON["data"]["attributes"]["tags"] = []

        JSON["data"]["attributes"]["tags"].append('1')

        JSON['data']['attributes']['license'] = '1'
        JSON['data']['attributes']['description'] = '1'
        JSON['data']['attributes']['policy'] = {'access': '1'}

        remote_blob = {'url' :'1', 'original_filename': '1'}

        JSON['data']['attributes']['content_blobs'] = [remote_blob]


        JSON['data']['relationships'] = {}
        SEEK._relationsFormat(JSON, 'projects', 'data file')
        SEEK._relationsFormat(JSON, 'creators', 'data file')
        SEEK._relationsFormat(JSON, 'assays', 'data file')
        SEEK._relationsFormat(JSON, 'publications', 'data file')
        SEEK._relationsFormat(JSON, 'events', 'data file')

        fileJSON = SEEK._data_fileFormat('1', '1')

        self.assertEqual(JSON, fileJSON)

    def test_loadJSON_Method(self):

        r = self.testOBJ.session.get(self.testOBJ.base_url + "assays/576")

        self.testOBJ.session.close()

        self.testOBJ.json = r.json()
        self.testOBJ._loadJSON(self.testOBJ, self.testOBJ.json['data'])

        for item in ['attributes','id','links','meta','relationships','type']:
            self.assertIn(item, dir(self.testOBJ.data))

    def test_request_Method(self):
        self.assertTrue(self.testOBJ._request(type="assays", id="576"))

    def test_request_Method_BadRequest(self):
        self.assertFalse(self.testOBJ._request(type="assays", id="0"))

    def test_request_Method_HasError(self):

        self.testOBJ.base_url = "www.wrong.url.com/"
        self.assertRaises(Exception,
                            self.testOBJ._request(type="assays", id="576"))

    def test_printAttributes(self):

        capturedOutput = StringIO()

        sys.stdout = capturedOutput

        self.testOBJ._request("assays","576")

        self.testOBJ._printAttributes()

        sys.stdout = sys.__stdout__

        self.assertEqual(capturedOutput.getvalue(),
        "PGK 70C model(id: 576 | type: assays)\n\nDescription: PGK 70C model\n")

    def test_printAttributesMissingDescription(self):

        capturedOutput = StringIO()

        sys.stdout = capturedOutput

        self.testOBJ._request("assays","945")

        self.testOBJ._printAttributes()

        sys.stdout = sys.__stdout__

        self.assertEqual(capturedOutput.getvalue(),
        "Hormone concentrations(id: 945 | type: assays)\n\nDescription: missing\n")

    def test_printRelationshipsSearch(self):

        capturedOutput = StringIO()

        sys.stdout = capturedOutput

        self.testOBJ.search("assays","576")

        self.testOBJ._printRelationshipsSearch()

        sys.stdout = sys.__stdout__

        self.assertEqual(capturedOutput.getvalue(),
            "(9 s estimated)\nLoading 0.0%\rLoading 11.11%\rLoading 22.22%\rLoading 33.33%\rLoading 44.44%\rLoading 55.56%\rLoading 66.67%\rLoading 77.78%\rLoading 88.89%\r\rLoading Completed\n<IPython.core.display.HTML object>\n")

    def test_printRelationshipsSearchNoRelationships(self):

        capturedOutput = StringIO()

        sys.stdout = capturedOutput

        self.testOBJ.search("people","526")

        self.testOBJ._printRelationshipsSearch()

        sys.stdout = sys.__stdout__

        self.assertEqual(capturedOutput.getvalue(),
            "(0 s estimated)\nObject has no relationships\n")

    @patch("SEEK._get_input", return_value='3')
    @patch("SEEK._get_input_testing", return_value='10')
    def test_searchAdvancedSettings_Method(self, srpt, rpt):

        self.testOBJ.searchAdvancedSetup()
        self.assertEqual(self.testOBJ.searchResultsPerThread, 3)
        self.assertEqual(self.testOBJ.relationshipsPerThread, 10)

    @patch("SEEK._get_input", return_value='douazecisitrei')
    @patch("SEEK._get_input_testing", return_value='august')
    def test_searchAdvancedSettings_Method_BadInput(self, srpt, rpt):

        self.assertRaises(Exception, self.testOBJ.searchAdvancedSetup)

    def test_print(self):

        capturedOutput = StringIO()

        sys.stdout = capturedOutput

        self.testOBJ.search("assays","576")

        self.testOBJ.printSearch()

        sys.stdout = sys.__stdout__

        self.assertEqual(capturedOutput.getvalue(),
        "(9 s estimated)\nLoading 0.0%\rLoading 11.11%\rLoading 22.22%\rLoading 33.33%\rLoading 44.44%\rLoading 55.56%\rLoading 66.67%\rLoading 77.78%\rLoading 88.89%\r\rLoading Completed\nPGK 70C model(id: 576 | type: assays)\n\nDescription: PGK 70C model\n\n\n<IPython.core.display.HTML object>\n")

    @patch("SEEK._get_input", return_value="liver")
    @patch("SEEK._get_input_testing", return_value="assays")
    def test_APISearch_Method(self, keyword, type):

        self.assertTrue(self.testOBJ.APISearch())

    @patch("SEEK._get_input", return_value="liver")
    @patch("SEEK._get_input_testing", return_value="wrong type")
    def test_APISearch_Method_BadRequest(self, keyword, type):

        self.assertFalse(self.testOBJ.APISearch())

    @patch("SEEK._get_input", return_value="liver")
    @patch("SEEK._get_input_testing", return_value="assays")
    def test_createRequestList_Method(self, keyword, type):

        self.testOBJ.APISearch()
        self.testOBJ.createRequestList()

        self.assertTrue(len(self.testOBJ.requestList) ,6)

    def test_makeRequests_Method(self):

        self.testOBJ._makeRequests(self.goodFormat_RequestList,
                                  len(self.goodFormat_RequestList))

        properties = [
            'attributes',
            'id',
            'type',
            'links',
            'meta',
            'relationships']

        for request in self.testOBJ.requestList:
            for prop in properties:
                self.assertIn(prop, dir(request.data))

    def test_makeRequests_Method_EmptyList(self):

        self.assertRaises(Exception,
                         self.testOBJ._makeRequests(self.empty_RequestList,
                                                   len(self.empty_RequestList)))

    def test_makeRequests_Method_ListWithBadItem(self):

        self.assertRaises(Exception,
                          self.testOBJ._makeRequests(self.badRequest_RequestList,
                                              len(self.badRequest_RequestList)))

    def test_makeRequests_Method_BadFormat(self):

        self.assertRaises(Exception,
                         self.testOBJ._makeRequests(self.badFormat_RequestList,
                                                   len(self.badFormat_RequestList)))

    def test_parallelRequest_Method(self):

        self.testOBJ.parallelRequest(self.goodFormat_RequestList, 1)
        for thread in self.testOBJ.threadList:
            thread.join()

        properties = [
            'attributes',
            'id',
            'type',
            'links',
            'meta',
            'relationships']

        for request in self.testOBJ.requestList:
            for prop in properties:
                self.assertIn(prop, dir(request.data))

    def test_parallelRequest_Method_ManyRequestPerThread(self):

        self.testOBJ.parallelRequest(self.goodFormat_RequestList, 15)
        for thread in self.testOBJ.threadList:
            thread.join()

        properties = [
            'attributes',
            'id',
            'type',
            'links',
            'meta',
            'relationships']

        for request in self.testOBJ.requestList:
            for prop in properties:
                self.assertIn(prop, dir(request.data))

    def wait(self, rList):

        self.testOBJ.parallelRequest(rList, 1)
        for thread in self.testOBJ.threadList:
            thread.join()

    def test_parallelRequest_Method_EmptyRequestList(self):

        self.assertRaises(Exception, self.wait(self.empty_RequestList))

    def test_parallelRequest_Method_ZeroRequestsPerThread(self):

        self.testOBJ.parallelRequest(self.goodFormat_RequestList, 0)
        for thread in self.testOBJ.threadList:
            thread.join()

        properties = [
            'attributes',
            'id',
            'type',
            'links',
            'meta',
            'relationships']

        for request in self.testOBJ.requestList:
            for prop in properties:
                self.assertIn(prop, dir(request.data))

    def test_parallelRequest_Method_BadRequestList(self):

        self.assertRaises(Exception, self.wait(self.badRequest_RequestList))

    def test_createRelationshipsList_Method(self):

        self.testOBJ.parallelRequest(self.goodFormat_RequestList,1)
        for thread in self.testOBJ.threadList:
            thread.join()

        self.testOBJ.createRelationshipList()
        self.assertEqual(len(self.testOBJ.relationshipList), 17)

    def test_removeDuplicateRelationships_Method(self):

        self.testOBJ.parallelRequest(self.goodFormat_RequestList,1)
        for thread in self.testOBJ.threadList:
            thread.join()

        self.testOBJ.createRelationshipList()
        self.testOBJ.removeDuplicateRelationships()

        for i in range(0,len(self.testOBJ.relationshipList)):
            for j in range(0, len(self.testOBJ.relationshipList)):

                if i is not j:
                    self.assertNotEquals(self.testOBJ.relationshipList[i],
                                         self.testOBJ.relationshipList[j])

    def test_substituteRelationships_Method(self):

        self.testOBJ.parallelRequest(self.goodFormat_RequestList,1)
        for thread in self.testOBJ.threadList:
            thread.join()

        self.testOBJ.createRelationshipList()
        self.testOBJ.substituteRelationships(self.testOBJ.relationshipList)
        self.assertEqual(1,1)

    @patch('SEEK._get_input', return_value="liver")
    @patch('SEEK._get_input_testing', return_value="assays")
    def test_browse_Method(self, name, key):
        self.assertTrue(self.testOBJ.browse())

    def test_download_Method(self):

        self.testOBJ._request(type="data_files", id="2813")
        self.assertTrue(self.testOBJ.download())
        self.assertTrue(os.path.isfile(self.testOBJ.fileName))

    def test_download_Method_NoDataFile(self):

        self.testOBJ._request(type="assays", id="43")
        self.assertFalse(self.testOBJ.download())

    def test_view_Method(self):

        self.testOBJ._request(type="data_files", id="2813")
        self.assertTrue(self.testOBJ.download())
        self.assertTrue(os.path.isfile(self.testOBJ.fileName))
        self.assertEquals(type(pandas.read_excel(self.testOBJ.fileName)),
            type(self.testOBJ.view(columnForHeader=1, page='6h results genes')))

    @patch('SEEK._get_input', return_value=
                                   PROT_DEFAULT_AUTHENTICATION_STRING)
    @patch('getpass.getpass', return_value=PROT_DEFAULT_AUTHENTICATION_STRING)
    def test_initWrite_WithAuth(self, username, password):

        self.testWriteOBJ.session.auth = SEEK.auth()
        self.assertEqual(self.testWriteOBJ.session.auth,
                        (PROT_DEFAULT_AUTHENTICATION_STRING,
                        PROT_DEFAULT_AUTHENTICATION_STRING))

    @patch('SEEK._get_input', return_value=
                                   PROT_DEFAULT_AUTHENTICATION_STRING)
    @patch('getpass.getpass', return_value=PROT_DEFAULT_AUTHENTICATION_STRING)
    def test_initWrite_WithoutAuth(self, username, password):

        self.testWriteOBJ = SEEK.write()

        self.assertEqual(self.testWriteOBJ.session.auth,
                         (PROT_DEFAULT_AUTHENTICATION_STRING,
                          PROT_DEFAULT_AUTHENTICATION_STRING))

    @patch('SEEK._get_input', return_value='1')
    def test_post_Method(self, rofl):

        self.type = widgets.Dropdown(
            options=[
                "assays",
                "data_files",
                "studies",
                "investigations",
                "models",
                "sops",
                "publications"
            ],
            value='studies',
            disabled=False,
        )
        self.testWriteOBJ.JSON = SEEK._studyFormat('1','1')
        self.assertTrue(self.testWriteOBJ.post())

if __name__ == '__main__':
    unittest.main()
