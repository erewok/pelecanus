import os
import json
import copy
from unittest import TestCase

from pelecanus.toolbox import backfill_append
from pelecanus.toolbox import new_json_from_path
from pelecanus.toolbox import find_value

# Fixture locations
current_dir = os.path.abspath(os.path.dirname(__file__))
fixture_dir = os.path.join(current_dir, 'fixtures')
# Actual datasets
data = os.path.join(fixture_dir, 'test_data.json')
book = os.path.join(fixture_dir, 'book.json')
ricketts = os.path.join(fixture_dir, 'ricketts.json')
monterrey = os.path.join(fixture_dir, 'monterrey.json')
pelecanus_occidentalis = os.path.join(fixture_dir,
                                      'pelecanus_occidentalis.json')


class TestBackfillAppend(TestCase):

    def setUp(self):
        self.test_list = list(range(10))

    def test_original_list_unmodified(self):
        new_list = backfill_append(self.test_list, 20, "TEST")
        self.assertNotEqual(self.test_list, new_list)

    def test_modify_regular_index(self):
        new_list = backfill_append(self.test_list, 5, "TEST")
        self.assertEqual(new_list[5], "TEST")

        new_list = backfill_append(self.test_list, 0, "TEST")
        self.assertEqual(new_list[0], "TEST")

    def test_with_empty_list(self):
        newlist = []
        test_list = backfill_append(newlist, 0, "TEST")
        self.assertEqual(test_list[0], "TEST")

    def test_backfill(self):
        none_list = [None for x in range(10)]
        new_list = backfill_append(self.test_list, 20, "TEST")
        self.assertEqual(new_list[10:20], none_list)
        self.assertEqual(new_list[20], "TEST")


class TestNewJsonFromPath(TestCase):

    def test_no_path(self):
        self.assertEqual(new_json_from_path([], "TEST"),
                         "TEST")

    def test_dicts(self):
        expected = {'one': {'two': {'three': {'four': {'five': "VALUE"}}}}}
        path = ['one', 'two', 'three', 'four', 'five']
        new_json = new_json_from_path(path, "VALUE")
        self.assertEqual(expected, new_json)

    def test_lists(self):
        expected = [None, [None, None, [None, None, None, [None, None,
                                                           None, None,
                                                           "VALUE"]]]]
        path = [1, 2, 3, 4]
        new_json = new_json_from_path(path, "VALUE")
        self.assertEqual(expected, new_json)

    def test_mixed(self):
        expected = {'one': {'two': [None, None, None, [{'four': "VALUE"}]]}}
        path = ['one', 'two', 3, 0, 'four']
        new_json = new_json_from_path(path, "VALUE")
        self.assertEqual(expected, new_json)


class TestFindValue(TestCase):

    def setUp(self):
        self.fail("IMPLEMENT!!")


class TestFindValue(TestCase):

    def setUp(self):
        self.fail("IMPLEMENT!!")
        pass


class TestCountKey(TestCase):

    def setUp(self):
        self.fail("IMPLEMENT!!")
        pass


class TestGeneratePaths(TestCase):

    def setUp(self):
        self.fail("IMPLEMENT!!")
        pass


class TestReverseResultDecorator(TestCase):

    def setUp(self):
        self.fail("IMPLEMENT!!")
        pass


class TestGetPath(TestCase):
    
    def setUp(self):
        self.fail("IMPLEMENT!!")
        pass


class TestGetNestedValue(TestCase):
    
    def setUp(self):
        self.fail("IMPLEMENT!!")
        pass


class TestSetNestedValue(TestCase):
    
    def setUp(self):
        self.fail("IMPLEMENT!!")
        pass

# class EXAMPLES:
    # def test_enumerate(self):
    #     book_url = 'https://openlibrary.org/books/OL7928788M/'
    #     book_url += 'Between_Pacific_Tides'
    #     test_book_enums = [(['ISBN:9780804720687', 'thumbnail_url'],
    #                         'https://covers.openlibrary.org/b/id/577352-S.jpg'),
    #                        (['ISBN:9780804720687', 'bib_key'],
    #                         'ISBN:9780804720687'),
    #                        (['ISBN:9780804720687', 'preview_url'], book_url),
    #                        (['ISBN:9780804720687', 'info_url'], book_url),
    #                        (['ISBN:9780804720687', 'preview'], 'noview')]
    #     test_book = PelicanJson(self.book)
    #     check_enums = list(test_book.enumerate())
    #     for path, value in test_book.enumerate():
    #         self.assertIn((path, value), test_book_enums)

    # def test_paths(self):
    #     test_book = PelicanJson(self.book)
    #     book_paths = [['ISBN:9780804720687', 'thumbnail_url'],
    #                   ['ISBN:9780804720687', 'bib_key'],
    #                   ['ISBN:9780804720687', 'preview_url'],
    #                   ['ISBN:9780804720687', 'info_url'],
    #                   ['ISBN:9780804720687', 'preview']]
    #     for item in test_book.paths():
    #         self.assertIn(item, book_paths)

    # def test_keys(self):
    #     pkeys = {'query', 'normalized', 'to', 'from', 'pages',
    #              '1266004', 'ns', 'title', 'pageid'}
    #     bkeys = {'thumbnail_url', 'preview_url', 'bib_key',
    #              'info_url', 'ISBN:9780804720687', 'preview'}
    #     test_book = PelicanJson(self.book)
    #     test_pelican = PelicanJson(self.pelecanus_occidentalis)
    #     self.assertEqual(set(test_pelican.keys()), pkeys)
    #     self.assertEqual(set(test_book.keys()), bkeys)
    #     self.assertEqual(len(test_pelican), len(set(test_pelican.keys())),
    #                      len(pkeys))

    # def test_values(self):
    #     pvalues = {'Pelecanus occidentalis', 'Pelecanus_occidentalis',
    #                0, 'Pelecanus occidentalis', 1266004}
    #     book_url = 'https://openlibrary.org/books/OL7928788M/'
    #     book_url += 'Between_Pacific_Tides'
    #     monty_uid = 'gov.noaa.ncdc:C00345'
    #     rval = 'Ed_Ricketts'
    #     rval2 = 'File:Pacific Biological Laboratories.JPG'
    #     test_pelican = PelicanJson(self.pelecanus_occidentalis)
    #     test_book = PelicanJson(self.book)
    #     test_monty = PelicanJson(self.monterrey)
    #     test_rickettsi = PelicanJson(self.ricketts)
    #     self.assertEqual(pvalues, set(test_pelican.values()))
    #     self.assertIn(book_url, set(test_book.values()))
    #     self.assertIn(monty_uid, set(test_monty.values()))
    #     self.assertIn(rval, set(test_rickettsi.values()))
    #     self.assertIn(rval2, set(test_rickettsi.values()))

    # def test_count_key(self):
    #     test_pelican = PelicanJson(self.item)
    #     self.assertEqual(test_pelican.count_key('href'),
    #                      11)
    #     test_rickettsi = PelicanJson(self.ricketts)
    #     self.assertEqual(test_rickettsi.count_key('extlinks'),
    #                      2)
    #     self.assertEqual(test_rickettsi.count_key('*'),
    #                      10)
    #     self.assertEqual(test_rickettsi.count_key('title'),
    #                      8)

    # def test_searchkey(self):
    #     test_rickettsi = PelicanJson(self.ricketts)
    #     paths = [['query', 'pages', '1422396', 'extlinks'] + [n, '*']
    #              for n in range(10)]
    #     for item in test_rickettsi.search_key('*'):
    #         self.assertIn(item, paths)
    #     for key in test_rickettsi.keys():
    #         self.assertTrue(next(test_rickettsi.search_key(key)))
    #     pelican_item = PelicanJson(self.item)
    #     for key in pelican_item.keys():
    #         self.assertTrue(next(pelican_item.search_key(key)))

    # def test_searchvalue(self):
    #     test_monty = PelicanJson(self.monterrey)
    #     values = list(test_monty.values())
    #     self.assertEqual(len(values), 63)
    #     answers = [('gov.noaa.ncdc:C00822', ['results', 7, 'uid']),
    #                ('gov.noaa.ncdc:C00040', ['results', 0, 'uid'])]
    #     for item, answer in answers:
    #         self.assertEqual(next(test_monty.search_value(item)),
    #                          answer)
    #     self.assertEqual(list(test_monty.search_value('2014-08-25')),
    #                      [['results', 1, 'maxdate'],
    #                       ['results', 3, 'maxdate']])
    #     pelican_item = PelicanJson(self.item)
    #     self.assertEqual(next(pelican_item.search_value('Cove')),
    #                      ['attributes', 'tags', 2])

    # def test_pluck(self):
    #     answer = PelicanJson({'to': 'Pelecanus occidentalis',
    #                           'from': 'Pelecanus_occidentalis'})
    #     test_pelican = PelicanJson(self.pelecanus_occidentalis)
    #     self.assertEqual(answer,
    #                      next(test_pelican.pluck('to',
    #                                              'Pelecanus occidentalis')))
    #     self.assertEqual(answer,
    #                      next(test_pelican.pluck('from',
    #                                              'Pelecanus_occidentalis')))
    #     pelican_item = PelicanJson(self.item)
    #     self.assertEqual(pelican_item,
    #                      next(pelican_item.pluck('version', '1.0')))

    # def test_get_nested_value(self):
    #     pelican_item = PelicanJson(self.item)
    #     answer = pelican_item.get_nested_value(['attributes', 'tags', 2])
    #     self.assertEqual(answer, 'Cove')
    #     test_monty = PelicanJson(self.monterrey)
    #     answers = [('gov.noaa.ncdc:C00822', ['results', 7, 'uid']),
    #                ('gov.noaa.ncdc:C00040', ['results', 0, 'uid'])]
    #     for answer, path in answers:
    #         self.assertEqual(test_monty.get_nested_value(path),
    #                          answer)
    #     # Testing with a tuple, also should be allowed
    #     path = ('results', 9, 'uid')
    #     self.assertEqual(test_monty.get_nested_value(path),
    #                      'gov.noaa.ncdc:C00313')

    # def test_get_nested_value_raises_empty_path(self):
    #     test_pelican = PelicanJson(self.monterrey)
    #     with self.assertRaises(EmptyPath):
    #         test_pelican.get_nested_value([])

    # def test_get_nested_value_raises_bad_path(self):
    #     test_pelican = PelicanJson(self.monterrey)
    #     # Try a string
    #     with self.assertRaises(BadPath):
    #         test_pelican.get_nested_value("STRING")
    #     # Howsbout a dict?
    #     somedict = {'results': 'value', '9': 'value2'}
    #     with self.assertRaises(BadPath):
    #         test_pelican.get_nested_value(somedict)
    #     # What happens with an integer?
    #     with self.assertRaises(BadPath):
    #         test_pelican.get_nested_value(8)
    #     # ...and a set?
    #     with self.assertRaises(BadPath):
    #         test_pelican.get_nested_value({'results', 8})

    # def test_set_nested_value(self):
    #     new_path = ['ISBN:9780804720687', 'book_title']
    #     test_book = PelicanJson(self.book)
    #     test_book.set_nested_value(new_path, 'Between Pacific Tides')
    #     self.assertEqual(test_book.get_nested_value(new_path),
    #                      'Between Pacific Tides')

    #     test_pelican = PelicanJson(self.pelecanus_occidentalis)
    #     values = []
    #     self.assertEqual(len(list(test_pelican.values())), 5)
    #     for path, value in test_pelican.enumerate():
    #         values.append(value)
    #         test_pelican.set_nested_value(path, None)
    #     self.assertEqual(len(set(test_pelican.values())), 1)
    #     for path in test_pelican.search_value(None):
    #         test_pelican.set_nested_value(path, values.pop())
    #     self.assertEqual(len(list(test_pelican.values())), 5)

    #     pelican_item = PelicanJson(self.item)
    #     pelican_item.set_nested_value(['href'], None)
    #     self.assertEqual(pelican_item['href'], None)

    # def test_find_and_replace(self):
    #     test_pelican = PelicanJson(self.pelecanus_occidentalis)
    #     test_pelican.find_and_replace('Pelecanus occidentalis',
    #                                   'Brown Pelican')
    #     replace_paths = [['query', 'normalized', 0, 'to'],
    #                      ['query', 'pages', '1266004', 'title']]
    #     for path in test_pelican.search_value('Brown Pelican'):
    #         self.assertIn(path, replace_paths)
