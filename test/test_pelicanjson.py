import os
import json
import copy
from unittest import TestCase

from pelecanus import PelicanJson
from pelecanus.exceptions import BadPath
from pelecanus.exceptions import EmptyPath


# Fixture locations
current_dir = os.path.abspath(os.path.dirname(__file__))
fixture_dir = os.path.join(current_dir, 'fixtures')
# Actual datasets
data = os.path.join(fixture_dir, 'datadoc.json')
book = os.path.join(fixture_dir, 'book.json')
ricketts = os.path.join(fixture_dir, 'ricketts.json')
monterrey = os.path.join(fixture_dir, 'monterrey.json')
pelecanus_occidentalis = os.path.join(fixture_dir,
                                      'pelecanus_occidentalis.json')


class TestDictIntegrity(TestCase):

    def setUp(self):
        with open(data, 'r') as f:
            self.data = json.loads(f.read())

    def test_constructor(self):
        test_pelican = PelicanJson(self.data['items'][0])
        self.assertTrue(isinstance(test_pelican['attributes'],
                                   PelicanJson))
        self.assertTrue(isinstance(test_pelican['links'],
                                   PelicanJson))
        self.assertTrue(isinstance(test_pelican['attributes']['tags'],
                                   list))

    def test_convert(self):
        test_pelican = PelicanJson(self.data)
        self.assertEqual(test_pelican.convert(), self.data)
        self.assertTrue(isinstance(test_pelican.convert(),
                                   dict))

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
        with open(book, 'r') as f:
            self.book = json.loads(f.read())
        with open(ricketts, 'r') as f:
            self.ricketts = json.loads(f.read())
        with open(monterrey, 'r') as f:
            self.monterrey = json.loads(f.read())
        with open(pelecanus_occidentalis, 'r') as f:
            self.pelecanus_occidentalis = json.loads(f.read())

    def test_to_string(self):
        test_pelican = PelicanJson(self.ricketts)
        self.assertNotIn("<PelicanJson:", str(test_pelican))

    def test_update_from_list(self):
        test_pelican = PelicanJson(self.ricketts)
        values = [{'*': '//www.worldcat.org/identities/lccn-n79-055298'},
                  {'*': 'http://edricketts.stanford.edu/'},
                  {'*': 'http://holisticbiology.stanford.edu/philosophy.html'}]
        extlinks = self.ricketts['query']['pages']['1422396']['extlinks']
        first, *_, second_last, last = test_pelican._update_from_list(extlinks)
        self.assertEqual(first, PelicanJson(values[0]))
        self.assertEqual(second_last, PelicanJson(values[1]))
        self.assertEqual(last, PelicanJson(values[2]))

    def test_contains(self):
        test_pelican = PelicanJson(self.book)
        self.assertIn('ISBN:9780804720687', test_pelican)
        self.assertIn('preview', test_pelican)
        self.assertIn('bib_key', test_pelican)
        test_pelican = PelicanJson(self.monterrey)
        for key in test_pelican.keys():
            self.assertIn(key, test_pelican)
        self.assertFalse(test_pelican.__contains__('NADA'))

    def test_get_item(self):
        query_continue = self.ricketts['query-continue']
        test_pelican = PelicanJson(self.ricketts)
        query_pelican = PelicanJson(query_continue)
        self.assertEqual(test_pelican.get('query-continue'),
                         query_pelican)
        self.assertEqual(test_pelican.get('NO-KEY'),
                         None)

    def test_set_item(self):
        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        test_pelican['query'] = ['some', 'new' 'vals']
        self.assertEqual(test_pelican['query'], ['some', 'new' 'vals'])

    def test_set_item_dictionary(self):
        test_pelican = PelicanJson(self.book)
        newdict = {'somekey': 'somevalue',
                   'somenested': {'somenestedkey': 'somenestedvalue'}}
        expected = PelicanJson(newdict)
        test_pelican['TEST'] = newdict
        self.assertTrue(isinstance(test_pelican, PelicanJson))
        self.assertEqual(test_pelican['TEST'], expected)

    def test_set_item_list(self):
        test_pelican = PelicanJson(self.book)
        newlist = ['item1', 'item2', {'somenestedkey': 'somenestedvalue'}]
        expected = PelicanJson({'newlist': newlist})
        test_pelican['newlist'] = newlist
        self.assertEqual(test_pelican['newlist'], expected['newlist'])

    def test_delete_item(self):
        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        test_pelican['query'] = ['some', 'new' 'vals']
        self.assertEqual(test_pelican['query'], ['some', 'new' 'vals'])
        del test_pelican['query']
        self.assertEqual(test_pelican.get('query'),
                         None)
        with self.assertRaises(KeyError):
            del test_pelican['none']

    def test_len(self):
        keys = {'query', 'normalized', 'to', 'from', 'pages',
                '1266004', 'ns', 'title', 'pageid'}
        length = len(keys)
        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        self.assertEqual(len(test_pelican), length)
        self.assertEqual(set(test_pelican.keys()), keys)
        self.assertEqual(len(test_pelican), len(list(test_pelican.keys())),
                         len(keys))
        test_pelican['new'] = 'VALUE'
        self.assertEqual(len(test_pelican), length + 1)

    def test_iter(self):
        pkeys = {'query', 'normalized', 'to', 'from', 'pages',
                 '1266004', 'ns', 'title', 'pageid'}
        bkeys = {'thumbnail_url', 'preview_url', 'bib_key',
                 'info_url', 'ISBN:9780804720687', 'preview'}
        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        test_book = PelicanJson(self.book)
        self.assertEqual(set(test_pelican.keys()), pkeys)
        self.assertEqual(set(test_book.keys()), bkeys)


class TestPelicanMethods(TestCase):

    def setUp(self):
        with open(data, 'r') as f:
            rdata = json.loads(f.read())
            self.item = rdata['items'][-1]
        with open(book, 'r') as f:
            self.book = json.loads(f.read())
        with open(ricketts, 'r') as f:
            self.ricketts = json.loads(f.read())
        with open(monterrey, 'r') as f:
            self.monterrey = json.loads(f.read())
        with open(pelecanus_occidentalis, 'r') as f:
            self.pelecanus_occidentalis = json.loads(f.read())

    def test_items(self):
        answer_dict = {'ns': 0,
                       'title': 'Pelecanus occidentalis',
                       'pageid': 1266004,
                       'to': 'Pelecanus occidentalis',
                       'from': 'Pelecanus_occidentalis'}
        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        test_book = PelicanJson(self.book)
        self.assertEqual(len(list(test_book.keys())),
                         len(list(test_book.items())))
        self.assertEqual(len(list(test_pelican.keys())),
                         len(list(test_pelican.items())))
        for key, value in test_pelican.items():
            if key in answer_dict:
                self.assertEqual(answer_dict[key], value)

    def test_enumerate(self):
        book_url = 'https://openlibrary.org/books/OL7928788M/'
        book_url += 'Between_Pacific_Tides'
        test_book_enums = [
            (['ISBN:9780804720687', 'thumbnail_url'],
             'https://covers.openlibrary.org/b/id/577352-S.jpg'),
            (['ISBN:9780804720687', 'bib_key'],
             'ISBN:9780804720687'),
            (['ISBN:9780804720687', 'preview_url'], book_url),
            (['ISBN:9780804720687', 'info_url'], book_url),
            (['ISBN:9780804720687', 'preview'], 'noview')]
        test_book = PelicanJson(self.book)
        for path, value in test_book.enumerate():
            self.assertIn((path, value), test_book_enums)

    def test_paths(self):
        test_book = PelicanJson(self.book)
        book_paths = [['ISBN:9780804720687', 'thumbnail_url'],
                      ['ISBN:9780804720687', 'bib_key'],
                      ['ISBN:9780804720687', 'preview_url'],
                      ['ISBN:9780804720687', 'info_url'],
                      ['ISBN:9780804720687', 'preview']]
        for item in test_book.paths():
            self.assertIn(item, book_paths)

    def test_keys(self):
        pkeys = {'query', 'normalized', 'to', 'from', 'pages',
                 '1266004', 'ns', 'title', 'pageid'}
        bkeys = {'thumbnail_url', 'preview_url', 'bib_key',
                 'info_url', 'ISBN:9780804720687', 'preview'}
        test_book = PelicanJson(self.book)
        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        self.assertEqual(set(test_pelican.keys()), pkeys)
        self.assertEqual(set(test_book.keys()), bkeys)
        self.assertEqual(len(test_pelican), len(set(test_pelican.keys())),
                         len(pkeys))

    def test_keys_flat(self):
        test_book = PelicanJson(self.book)
        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        assert set(test_book.keys(flat=True)) == {'ISBN:9780804720687'}
        assert set(test_pelican.keys(flat=True)) == {"query"}

    def test_values(self):
        pvalues = {'Pelecanus occidentalis', 'Pelecanus_occidentalis',
                   0, 'Pelecanus occidentalis', 1266004}
        book_url = 'https://openlibrary.org/books/OL7928788M/'
        book_url += 'Between_Pacific_Tides'
        monty_uid = 'gov.noaa.ncdc:C00345'
        rval = 'Ed_Ricketts'
        rval2 = 'File:Pacific Biological Laboratories.JPG'
        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        test_book = PelicanJson(self.book)
        test_monty = PelicanJson(self.monterrey)
        test_rickettsi = PelicanJson(self.ricketts)
        self.assertEqual(pvalues, set(test_pelican.values()))
        self.assertIn(book_url, set(test_book.values()))
        self.assertIn(monty_uid, set(test_monty.values()))
        self.assertIn(rval, set(test_rickettsi.values()))
        self.assertIn(rval2, set(test_rickettsi.values()))

    def test_count_key(self):
        test_pelican = PelicanJson(self.item)
        self.assertEqual(test_pelican.count_key('href'),
                         11)
        test_rickettsi = PelicanJson(self.ricketts)
        self.assertEqual(test_rickettsi.count_key('extlinks'),
                         2)
        self.assertEqual(test_rickettsi.count_key('*'),
                         10)
        self.assertEqual(test_rickettsi.count_key('title'),
                         8)

    def test_create_path_totally_new_path(self):
        test_rickettsi = PelicanJson(self.ricketts)
        path = ['new', 'path', 'in', 1, 'object']
        with self.assertRaises(KeyError):
            test_rickettsi.get_nested_value(path)
        test_rickettsi.create_path(path, "TEST VALUE")
        self.assertEqual(test_rickettsi.get_nested_value(path), "TEST VALUE")

    def test_create_path_in_dict(self):
        test_rickettsi = PelicanJson(self.ricketts)
        overwrite_path = ['query-continue', 'extlinks',
                          'eloffset', 'newdict-with-key']
        msg = "Previous value overwritten with dictionary"
        test_rickettsi.create_path(overwrite_path, msg)
        self.assertEqual(test_rickettsi.get_nested_value(overwrite_path),
                         msg)
        newdict = test_rickettsi.get_nested_value(overwrite_path[:-1])
        self.assertTrue(isinstance(newdict, PelicanJson))

        paths = [['query-continue', 'extlinks', 'newkey1'],
                 ['query-continue', 'newkey1', 'newkey2'],
                 ['newkey1', 'newkey2', 'newkey3']]
        for path in paths:
            with self.assertRaises(KeyError):
                test_rickettsi.get_nested_value(path)
            test_rickettsi.create_path(path, "NEWVALUE")
            self.assertEqual(test_rickettsi.get_nested_value(path),
                             "NEWVALUE")

    def test_create_path_new_object_inside_list(self):
        test_rickettsi = PelicanJson(self.ricketts)
        paths = [['query', 'pages', '1422396', 'images', 7, 'title'],
                 ['query', 'normalized', 10, 'NEW']]
        check_for_none = ['query', 'normalized', 5]
        test_rickettsi.create_path(paths[0], "VALUE APPENDED TO LIST")
        test_rickettsi.create_path(paths[1], "VALUE in LIST with BACKFILL")
        self.assertEqual(test_rickettsi.get_nested_value(paths[0]),
                         "VALUE APPENDED TO LIST")
        self.assertEqual(test_rickettsi.get_nested_value(paths[1]),
                         "VALUE in LIST with BACKFILL")
        self.assertEqual(test_rickettsi.get_nested_value(check_for_none),
                         None)
        self.assertEqual(len(test_rickettsi.get_nested_value(['query',
                                                              'normalized'])),
                         11)

    def test_create_path_add_item_to_list(self):
        test_item = PelicanJson(self.item)
        paths = [['attributes', 'tags', 2],
                 ['attributes', 'tags', 5]]
        check_for_none = paths[1][:-1]
        check_for_none.append(4)
        test_item.create_path(paths[0], "New value inside list")
        self.assertEqual(test_item.get_nested_value(paths[0]),
                         "New value inside list")
        test_item.create_path(paths[1], "New value inside list with None")
        self.assertEqual(test_item.get_nested_value(paths[1]),
                         "New value inside list with None")
        self.assertEqual(test_item.get_nested_value(check_for_none),
                         None)

    def test_create_path_raise_badpath(self):
        test_rickettsi = PelicanJson(self.ricketts)
        bad_path = [[4, 'query', 'normalized', 0, 'from'],
                    [('some', 'tuple'), 'query'],
                    [{'some': 'dict'}, 'query']]
        with self.assertRaises(BadPath):
            test_rickettsi.create_path(bad_path[0], "VALUE")
            test_rickettsi.create_path(bad_path[1], "VALUE")
            test_rickettsi.create_path(bad_path[2], "VALUE")

    def test_create_path_raise_indexerror(self):
        test_rickettsi = PelicanJson(self.ricketts)
        bad_path = ['query', 'normalized', 'badkey', 'from']
        with self.assertRaises(IndexError):
            test_rickettsi.create_path(bad_path, "VALUE")

    def test_searchkey(self):
        test_rickettsi = PelicanJson(self.ricketts)
        paths = [['query', 'pages', '1422396', 'extlinks'] + [n, '*']
                 for n in range(10)]
        for item in test_rickettsi.search_key('*'):
            self.assertIn(item, paths)
        for key in test_rickettsi.keys():
            self.assertTrue(next(test_rickettsi.search_key(key)))
        pelican_item = PelicanJson(self.item)
        for key in pelican_item.keys():
            self.assertTrue(next(pelican_item.search_key(key)))

    def test_searchvalue(self):
        test_monty = PelicanJson(self.monterrey)
        values = list(test_monty.values())
        self.assertEqual(len(values), 63)
        answers = [('gov.noaa.ncdc:C00822', ['results', 7, 'uid']),
                   ('gov.noaa.ncdc:C00040', ['results', 0, 'uid'])]
        for item, answer in answers:
            self.assertEqual(next(test_monty.search_value(item)),
                             answer)
        self.assertEqual(list(test_monty.search_value('2014-08-25')),
                         [['results', 1, 'maxdate'],
                          ['results', 3, 'maxdate']])
        npr_api_tag = [['attributes', 'tags', 0],
                       ['items', 0, 'attributes', 'tags', 0]]
        pelican_item = PelicanJson(self.item)
        for path in pelican_item.search_value('npr_api'):
            self.assertIn(path, npr_api_tag)

    def test_pluck(self):
        answer = PelicanJson({'to': 'Pelecanus occidentalis',
                              'from': 'Pelecanus_occidentalis'})
        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        self.assertEqual(answer,
                         next(test_pelican.pluck('to',
                                                 'Pelecanus occidentalis')))
        self.assertEqual(answer,
                         next(test_pelican.pluck('from',
                                                 'Pelecanus_occidentalis')))
        pelican_item = PelicanJson(self.item)
        self.assertEqual(pelican_item['attributes'],
                         next(pelican_item.pluck('byline', 'Emily Reddy')))

    def test_get_nested_value(self):
        pelican_item = PelicanJson(self.item)
        answer = pelican_item.get_nested_value(['attributes', 'tags', 0])
        self.assertEqual(answer, 'npr_api')
        test_monty = PelicanJson(self.monterrey)
        answers = [('gov.noaa.ncdc:C00822', ['results', 7, 'uid']),
                   ('gov.noaa.ncdc:C00040', ['results', 0, 'uid'])]
        for answer, path in answers:
            self.assertEqual(test_monty.get_nested_value(path),
                             answer)
        # Testing with a tuple, also should be allowed
        path = ('results', 9, 'uid')
        self.assertEqual(test_monty.get_nested_value(path),
                         'gov.noaa.ncdc:C00313')

    def test_get_nested_value_raises_empty_path(self):
        test_pelican = PelicanJson(self.monterrey)
        with self.assertRaises(EmptyPath):
            test_pelican.get_nested_value([])

    def test_get_nested_value_raises_bad_path(self):
        test_pelican = PelicanJson(self.monterrey)
        # Try a string
        with self.assertRaises(BadPath):
            test_pelican.get_nested_value("STRING")
        # Howsbout a dict?
        somedict = {'results': 'value', '9': 'value2'}
        with self.assertRaises(BadPath):
            test_pelican.get_nested_value(somedict)
        # What happens with an integer?
        with self.assertRaises(BadPath):
            test_pelican.get_nested_value(8)
        # ...and a set?
        with self.assertRaises(BadPath):
            test_pelican.get_nested_value({'results', 8})

    def test_set_nested_value(self):
        new_path = ['ISBN:9780804720687', 'book_title']
        test_book = PelicanJson(self.book)
        test_book.set_nested_value(new_path, 'Between Pacific Tides')
        self.assertEqual(test_book.get_nested_value(new_path),
                         'Between Pacific Tides')

        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        values = []
        self.assertEqual(len(list(test_pelican.values())), 5)
        for path, value in test_pelican.enumerate():
            values.append(value)
            test_pelican.set_nested_value(path, None)
        self.assertEqual(len(set(test_pelican.values())), 1)
        for path in test_pelican.search_value(None):
            test_pelican.set_nested_value(path, values.pop())
        self.assertEqual(len(list(test_pelican.values())), 5)

        pelican_item = PelicanJson(self.item)
        pelican_item.set_nested_value(['href'], None)
        self.assertEqual(pelican_item['href'], None)

    def test_set_nested_value_raises_error(self):
        # Wish to raise IndexError, KeyError, TypeError
        test_rickettsi = PelicanJson(self.ricketts)
        key_error_paths = [['unknownKey', 'unknownKey2'],
                           ['query-continue', 'unknownKey']]
        # KeyErrors
        with self.assertRaises(KeyError):
            for path in key_error_paths:
                test_rickettsi.set_nested_value(path, "Shouldn't Work")

        # TypeErrors
        type_error_path = ['query-continue', 'extlinks',
                           'eloffset', 'newdict-with-key']
        with self.assertRaises(TypeError):
            test_rickettsi.set_nested_value(type_error_path,
                                            "Shouldn't Work")

        # IndexErrors
        index_error_paths = [['query', 'normalized', 1, 'from'],
                             ['query', 'normalized', 1, 'to']]
        with self.assertRaises(IndexError):
            for path in index_error_paths:
                test_rickettsi.set_nested_value(path, "Shouldn't Work")

    # Attempt to set paths that previously raised: IndexError, KeyError,
    # TypeError
    def test_set_nested_value_force_key_error(self):
        test_rickettsi = PelicanJson(self.ricketts)
        success_msg = "Should now work"
        # KeyErrors overidden
        key_error_paths = [['unknownKey', 'unknownKey2'],
                           ['query-continue', 'unknownKey']]
        for path in key_error_paths:
            test_rickettsi.set_nested_value(path,
                                            success_msg,
                                            force=True)
            self.assertEqual(test_rickettsi.get_nested_value(path),
                             success_msg)

    def test_set_nested_value_force_type_error(self):
        test_rickettsi = PelicanJson(self.ricketts)
        success_msg = "Should now work"
        # TypeErrors overridden: path created
        type_error_path = ['query-continue', 'extlinks',
                           'eloffset', 'newdict-with-key']
        test_rickettsi.set_nested_value(type_error_path,
                                        success_msg,
                                        force=True)
        self.assertEqual(test_rickettsi.get_nested_value(type_error_path),
                         success_msg)

    def test_set_nested_value_force_previous_index_error(self):
        test_rickettsi = PelicanJson(self.ricketts)
        success_msg = "Should now work"
        # IndexErrors overridden: paths created
        index_error_paths = [['query', 'normalized', 1, 'from'],
                             ['query', 'normalized', 1, 'to']]
        for path in index_error_paths:
            test_rickettsi.set_nested_value(path, success_msg, force=True)
            self.assertEqual(test_rickettsi.get_nested_value(path),
                             success_msg)

    def test_set_nested_value_force_add_to_list(self):
        path = ['attributes', 'tags', 4]
        test_pelican = PelicanJson(self.item)
        test_pelican.set_nested_value(path, 'New Tag', force=True)
        new_tag = test_pelican.get_nested_value(path)
        self.assertEqual(new_tag, 'New Tag')
        none_placeholder = ['attributes', 'tags', 3]
        self.assertEqual(test_pelican.get_nested_value(none_placeholder),
                         None)

    def test_safe_get_nested_value(self):
        test_pelican = PelicanJson(self.monterrey)
        assert test_pelican.safe_get_nested_value(["STRING"]) is None
        badpath = ('results', 'value', '9')
        assert test_pelican.safe_get_nested_value(badpath,
                                                  default="la") == "la"
        assert test_pelican.safe_get_nested_value([8], default=0) == 0
        tp = (1, 2)
        assert test_pelican.safe_get_nested_value(['results', 1000],
                                                  default=tp) == tp

        assert test_pelican.safe_get_nested_value(["results", 10000],
                                                  default="test") == "test"
        assert test_pelican.safe_get_nested_value(["results", "key"],
                                                  default="test") == "test"

        with self.assertRaises(EmptyPath):
            test_pelican.safe_get_nested_value([])
        with self.assertRaises(BadPath):
            test_pelican.safe_get_nested_value({'results', 8})

    def test_find_and_replace(self):
        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        test_pelican.find_and_replace('Pelecanus occidentalis',
                                      'Brown Pelican')
        replace_paths = [['query', 'normalized', 0, 'to'],
                         ['query', 'pages', '1266004', 'title']]
        for path in test_pelican.search_value('Brown Pelican'):
            self.assertIn(path, replace_paths)
