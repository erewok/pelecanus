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
        test_pelican = PelicanJson(self.data['items'][0])
        self.assertTrue(isinstance(test_pelican['attributes'],
                                   PelicanJson))
        self.assertTrue(isinstance(test_pelican['attributes']['tags'],
                                   list))

    def test_convert(self):
        test_pelican = PelicanJson(self.data)
        self.assertEqual(test_pelican.convert(), self.data)

    def test_serialize(self):
        test_pelican = PelicanJson(self.data)
        self.assertEqual(json.loads(test_pelican.serialize()),
                         self.data)

    def general_test_enum_nestedval(self):
        test_pelican = PelicanJson(self.data)
        for path, value in test_pelican.enumerate():
            retrieved_value = test_pelican.get_nested_value(path)
            self.assertEqual(retrieved_value,
                             value)


class TestDunderMethods(TestCase):

    def setUp(self):
        # Fixture locations
        current_dir = os.path.abspath(os.path.dirname(__file__))
        fixture_dir = os.path.join(current_dir, 'fixtures')
        data = os.path.join(fixture_dir, 'test_data.json')
        with open(data, 'r') as f:
            self.data = json.loads(f.read())
            self.item = self.data['items'][-1]

    def test_update_from_list(self):
        self.fail('update test not implemented')

    def test_contains(self):
        self.fail('contains test not implemented')

    def test_get_item(self):
        self.fail('get_items test not implemented')

    def test_set_item(self):
        self.fail('set_items test not implemented')

    def test_delete_item(self):
        self.fail('delete_items test not implemented')

    def test_len(self):
        self.fail('len test not implemented')

    def test_iter(self):
        self.fail('iter test not implemented')


class TestPelicanMethods(TestCase):

    def setUp(self):
        # Fixture locations
        current_dir = os.path.abspath(os.path.dirname(__file__))
        fixture_dir = os.path.join(current_dir, 'fixtures')
        data = os.path.join(fixture_dir, 'test_data.json')
        with open(data, 'r') as f:
            self.data = json.loads(f.read())
            self.item = self.data['items'][-1]

    def test_items(self):
        self.fail('items test not implemented')

    def test_enumerate(self):
        self.fail('enumerate test not implemented')

    def test_keys(self):
        self.fail('keys test not implemented')

    def test_values(self):
        self.fail('values test not implemented')

    def test_convert(self):
        self.fail('convert test not implemented')

    def test_serialize(self):
        self.fail('serialize test not implemented')

    def test_count_key(self):
        test_pelican = PelicanJson(self.item)
        self.assertEqual(test_pelican.count_key('href'),
                         11)
        self.assertEqual(test_pelican.count_key('byline'),
                         0)

    def test_searchkey(self):
        self.fail('searchkey test not implemented')

    def test_searchvalue(self):
        self.fail('searchvalue test not implemented')

    def test_get_nested_value(self):
        self.fail('get_nested_value test not implemented')

    def test_set_nested_value(self):
        self.fail('set_nested_value test not implemented')

    def test_pluck(self):
        self.fail('pluck test not implemented')

    def test_find_and_replace(self):
        self.fail('find_and_replace test not implemented')
