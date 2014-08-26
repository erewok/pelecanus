import os
import json
from unittest import TestCase

from pelecanus import PelicanJson


class TestDictIntegrity(TestCase):

    def setUp(self):
        # Fixture locations
        current_dir = os.path.abspath(os.path.dirname(__file__))
        fixture_dir = os.path.join(current_dir, 'fixtures')
        data = os.path.join(fixture_dir, 'test_data.json')
        with open(data, 'r') as f:
            self.data = json.loads(f.read())

    def test_constructor(self):
        test_pelican = PelicanJson(self.data)

    def test_convert(self):
        test_pelican = PelicanJson(self.data)
        self.assertEqual(test_pelican.convert(), self.data)

    def test_serialize(self):
        test_pelican = PelicanJson(self.data)
        self.assertEqual(json.loads(test_pelican.serialize()),
                         self.data)
