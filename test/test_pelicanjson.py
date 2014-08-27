import os
import json
from unittest import TestCase

from pelecanus import PelicanJson

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
        test_book_enums = [(['ISBN:9780804720687', 'thumbnail_url'],
                            'https://covers.openlibrary.org/b/id/577352-S.jpg'),
                           (['ISBN:9780804720687', 'bib_key'],
                            'ISBN:9780804720687'),
                           (['ISBN:9780804720687', 'preview_url'], book_url),
                           (['ISBN:9780804720687', 'info_url'], book_url),
                           (['ISBN:9780804720687', 'preview'], 'noview')]
        test_book = PelicanJson(self.book)
        check_enums = list(test_book.enumerate())
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
        pelican_item = PelicanJson(self.item)
        self.assertEqual(next(pelican_item.search_value('Cove')),
                         ['attributes', 'tags', 2])

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
        self.assertEqual(pelican_item,
                         next(pelican_item.pluck('version', '1.0')))

    def test_get_nested_value(self):
        pelican_item = PelicanJson(self.item)
        answer = pelican_item.get_nested_value(['attributes', 'tags', 2])
        self.assertEqual(answer, 'Cove')
        test_monty = PelicanJson(self.monterrey)
        answers = [('gov.noaa.ncdc:C00822', ['results', 7, 'uid']),
                   ('gov.noaa.ncdc:C00040', ['results', 0, 'uid'])]
        for answer, path in answers:
            self.assertEqual(test_monty.get_nested_value(path),
                             answer)

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

    def test_find_and_replace(self):
        test_pelican = PelicanJson(self.pelecanus_occidentalis)
        test_pelican.find_and_replace('Pelecanus occidentalis',
                                      'Brown Pelican')
        replace_paths = [['query', 'normalized', 0, 'to'],
                         ['query', 'pages', '1266004', 'title']]
        for path in test_pelican.search_value('Brown Pelican'):
            self.assertIn(path, replace_paths)
