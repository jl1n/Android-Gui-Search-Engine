from django.test import TestCase
from searchEngine.models import Application
from searchEngine.models import File
from searchEngine.models import Component
from haystack.query import SearchQuerySet
from searchEngine.search_indexes import FileIndex
from searchEngine.search_indexes import ComponentIndex
import pysolr

# Create your tests here.

class BaseTest(TestCase):
       
    def test_solr(self):
        # test that solr is up and running
        solr = pysolr.Solr('http://localhost:8983/solr', timeout=10)
        if solr == None:
            self.assertTrue(False)
        try:
            solr.get_session
        except:
            self.assertTrue(False)
        indexes = solr.search('*:*')
        self.assertNotEqual(len(indexes), 0)

    def test_view(self):
        # test that things are loading correctly
        resp = self.client.get('/about')
        self.assertEqual(resp.status_code, 200)
        resp_us = self.client.get('/usage')
        self.assertEqual(resp_us.status_code, 200)
        resp_add = self.client.get('/add_data')
        self.assertEqual(resp_add.status_code, 200)
        
