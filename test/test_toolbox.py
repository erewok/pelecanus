import os
import json
from unittest import TestCase

from pelecanus import PelicanJson
from pelecanus.toolbox import backfill_append
from pelecanus.toolbox import new_json_from_path
from pelecanus.toolbox import find_value
from pelecanus.toolbox import count_key
from pelecanus.toolbox import generate_paths
from pelecanus.toolbox import generate_paths_to_key
from pelecanus.toolbox import reverse_result
from pelecanus.toolbox import get_path
from pelecanus.toolbox import get_nested_value
from pelecanus.toolbox import set_nested_value

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
        with open(ricketts, 'r') as f:
            self.ricketts = json.loads(f.read())
        with open(pelecanus_occidentalis, 'r') as f:
            self.pelecanus_occidentalis = json.loads(f.read())
        with open(data, 'r') as f:
            rdata = json.loads(f.read())
            self.item = rdata['items'][-1]

    def test_find_value(self):
        expected = ['query', 'normalized', 0, 'from']
        seek_value = 'Pelecanus_occidentalis'
        value_gen = find_value(self.pelecanus_occidentalis, seek_value)
        self.assertEqual(next(value_gen), expected)
        with self.assertRaises(StopIteration):
            next(value_gen)
        answer_template = ['query', 'pages', '1422396', 'images']
        answers = [answer_template + [n, 'ns'] for n in range(7)]
        for path in find_value(self.ricketts, 6):
            self.assertIn(path, answers)

    def test_find_value_inside_lists(self):
        paths = [['links', 'enclosure', 0, 'meta', 'program_guid'],
                 ['attributes', 'tags', 0],
                 ['attributes', 'guid']]
        for path in find_value(self.item, 'someGUID'):
            self.assertIn(path, paths)


class TestCountKey(TestCase):

    def setUp(self):
        with open(data, 'r') as f:
            rdata = json.loads(f.read())
            self.item = rdata['items'][-1]
        with open(ricketts, 'r') as f:
            self.ricketts = json.loads(f.read())

    def test_count_key(self):
        print("counting 'href'")
        self.assertEqual(count_key(self.item, 'href'), 11)
        print("counting 'extlinks'")
        self.assertEqual(count_key(self.ricketts, 'extlinks'), 2)
        print("counting '*'")
        self.assertEqual(count_key(self.ricketts, '*'), 10)
        print("counting 'title'")
        self.assertEqual(count_key(self.ricketts, 'title'), 8)


class TestGeneratePaths(TestCase):

    def setUp(self):
        with open(book, 'r') as f:
            self.book = json.loads(f.read())
        with open(data, 'r') as f:
            rdata = json.loads(f.read())
            self.item = rdata['items'][8]

    def test_generate_paths(self):
        book_paths = [['ISBN:9780804720687'],
                      ['ISBN:9780804720687', 'thumbnail_url'],
                      ['ISBN:9780804720687', 'bib_key'],
                      ['ISBN:9780804720687', 'preview_url'],
                      ['ISBN:9780804720687', 'info_url'],
                      ['ISBN:9780804720687', 'preview']]
        for path in generate_paths(self.book):
            self.assertIn(path, book_paths)

    def test_generate_paths_inside_list(self):
        test_pelican = PelicanJson(self.item)
        expected_paths = []
        for path in test_pelican.search_value(''):
            expected_paths.append(path)
        for path in generate_paths(self.item):
            value = get_nested_value(self.item, path)
            if value == '':
                self.assertIn(path, expected_paths)


class TestGeneratePathsToKey(TestCase):

    def setUp(self):
        with open(book, 'r') as f:
            self.book = json.loads(f.read())
        with open(data, 'r') as f:
            rdata = json.loads(f.read())
            self.item = rdata['items'][0]

    def test_generate_paths_to_key(self):
        book_template = ['query', 'pages', '1422396', 'extlinks']
        book_paths = [book_template + [n, "*"] for n in range(10)]
        for path in generate_paths_to_key(self.book, "*"):
            self.assertIn(path, book_paths)

    def test_generate_paths_to_key_inside_list(self):
        paths = [['links', 'profile', 0, 'type'],
                 ['links', 'enclosure', 0, 'type'],
                 ['links', 'schema', 0, 'type'],
                 ['links', 'documentation', 0, 'type'],
                 ['links', 'self', 0, 'type'],
                 ['links', 'edit-form', 0, 'type'],
                 ['links', 'extends', 0, 'type']]
        for path in generate_paths_to_key(self.item, 'type'):
            self.assertIn(path, paths)


class TestReverseResultDecorator(TestCase):

    def test_reverse_result(self):
        answer = "THIs is a A reversed string"

        def dummy_func1():
            return list(range(19, 0, -1))

        def dummy_func2():
            return answer[::-1]

        range_test = reverse_result(dummy_func1)
        string_test = reverse_result(dummy_func2)

        self.assertEqual(range_test(), list(dummy_func1())[::-1])
        self.assertEqual(string_test(), "".join(list(dummy_func2())[::-1]))

    def test_reverse_result_should_return_none(self):
        def dummy_func():
            return None
        reverser = reverse_result(dummy_func)
        self.assertEqual(reverser(), None)


class TestGetPath(TestCase):
    def setUp(self):
        with open(data, 'r') as f:
            rdata = json.loads(f.read())
            self.item = rdata['items'][4]

    def test_get_path(self):
        found_path1 = get_path(self.item, 'premiere_date')
        answer1 = ['links', 'enclosure', 0, 'meta', 'premiere_date']
        found_path2 = get_path(self.item, 'documentation')
        answer2 = ['links', 'documentation']
        self.assertEqual(found_path1, answer1)
        self.assertEqual(found_path2, answer2)
        self.assertEqual(get_path(self.item, 'NO PATH'),
                         None)


class TestGetNestedValue(TestCase):
    def setUp(self):
        with open(data, 'r') as f:
            rdata = json.loads(f.read())
            self.item = rdata['items'][-1]
        with open(monterrey, 'r') as f:
            self.monterrey = json.loads(f.read())

    def test_get_nested_value(self):
        answer = get_nested_value(self.item, ['attributes', 'tags', 2])
        self.assertEqual(answer, 'Cove')
        answers = [('gov.noaa.ncdc:C00822', ['results', 7, 'uid']),
                   ('gov.noaa.ncdc:C00040', ['results', 0, 'uid'])]
        for answer, path in answers:
            self.assertEqual(get_nested_value(self.monterrey, path),
                             answer)
        # Testing with a tuple, also should be allowed
        path = ('results', 9, 'uid')
        self.assertEqual(get_nested_value(self.monterrey, path),
                         'gov.noaa.ncdc:C00313')

    def test_get_nested_value_raises_empty_path(self):
        self.assertEqual(get_nested_value(self.monterrey, []),
                         None)


class TestSetNestedValue(TestCase):
    def setUp(self):
        with open(data, 'r') as f:
            rdata = json.loads(f.read())
            self.item = rdata['items'][4]
        with open(book, 'r') as f:
            self.book = json.loads(f.read())
        with open(pelecanus_occidentalis, 'r') as f:
            self.pelecanus_occidentalis = json.loads(f.read())

    def test_set_nested_value(self):
        new_path = ['ISBN:9780804720687', 'book_title']
        set_nested_value(self.book, new_path, 'Between Pacific Tides')
        self.assertEqual(get_nested_value(self.book, new_path),
                         'Between Pacific Tides')

        set_nested_value(self.pelecanus_occidentalis, ['href'], None)
        self.assertEqual(self.pelecanus_occidentalis['href'], None)

    def test_set_all_paths(self):
        test_pelican = PelicanJson(self.item)
        for path in test_pelican.paths():
            set_nested_value(self.item, path, "NEWVALUE")
        for path in test_pelican.paths():
            value = get_nested_value(self.item, path)
            self.assertEqual(value, "NEWVALUE")
