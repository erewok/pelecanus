"""Free-floating versions of a number of methods associated with
PelicanJson. None of these functions create PelicanJson objects.
Instead they operate on nested Python dictionaries.
"""
from functools import wraps


def new_json_from_path(path, value):
        """Recursive function for translating a path and a value into a new,
        nested JSON object.
        Usage::

           >>> path = ['one', 'two', 0, 'three']
           >>> new_json_from_path(path, 'value')
           {'one' : {'two': [{'three': 'value'}]}}

        """
        if len(path) == 0:
            return value
        else:
            current, *rest = path
            if isinstance(current, str):
                return {current: new_json_from_path(rest, value)}
            elif isinstance(current, int):
                newlist = []
                return backfill_append(newlist,
                                       current,
                                       new_json_from_path(rest, value))


def backfill_append(listobject, index, item):
    """Returns a newlist with `item` inserted at `index`.
    Inserts None between last used index of `listobject` and
    `index` at which `item` is inserted::

       >>> backfill_append(['1', '2'], 5, '6')
       ['1', '2', None, None, None, '6']

    """
    temp_list = listobject[:]
    if index >= len(temp_list):
        difference = index - len(temp_list)
        backfill = [None for x in range(difference)]
        backfill.append(item)
        temp_list.extend(backfill)
    else:
        temp_list[index] = item
    return temp_list


def find_value(json_result, value, path=None):
    """Generator function for finding various paths to the value passed in.
    This function can handle arrays or objects and will return indices for
    array values and string keys for dictionary keys accessed to find the
    value.

    Args:

       `json_result` -- JSON object
       `value` -- value to search for

    Returns:

       Generator of lists that each represent a path to the value searched for.

    Usage::

       >>> list(find_value(some_nested_json, 'SOMEVALUE'))
       [['key1, 'key2', key3']['another_object', 1, 'akey']]
       >>> get_nested_value(some_nested_json, ['another_object', 1, 'akey'])
       'SOMEVALUE'

    """
    if path is None:
        path = []
    if isinstance(json_result, dict):
        for k, v in json_result.items():
            current_path = path[:]
            current_path.append(k)
            if value == v:
                yield current_path
            else:
                yield from find_value(v, value, path=current_path)

    elif isinstance(json_result, list):
        for idx, item in enumerate(json_result):
            current_path = path[:]
            current_path.append(idx)
            yield from find_value(item, value, path=current_path)
    else:
        if json_result == value:
            yield path


def count_key(json_result, key):
    """Recursive method for counting the appearance of a particular key
    inside a nested JSON object. This was created mostly to make sure that the
    generator below stays honest.

    Args:

       `json_result` -- JSON object
       `key` -- Key to count

    Returns:

       Sum of key's appearances in `json_result`.

       >>> count_key(JSON_OBJECT, "someKey")
       10

    """
    def counter(jresult):
        if isinstance(jresult, dict):
            for k, v in jresult.items():
                if key == k:
                    yield 1
                if isinstance(v, dict):
                    yield from counter(v)
                elif isinstance(v, list):
                    for item in v:
                        yield from counter(item)
        elif isinstance(jresult, list):
            for item in jresult:
                yield from counter(item)
        else:
            yield 0
    return sum(counter(json_result))


def generate_paths(json_result, path=None):
    """Generator function for introspecting a nested JSON object and finding all
    routes. Unlike `paths` for a `PelicanJson` object, which only yields paths
    that lead directly to whole values (and not nested objects), the
    `generate_paths` function also yields paths that lead to nested objects.

    The values at these pathways can be returned with `get_nested_value'
    or set with `set_nested_value`.

    Args:

       `json_result` -- JSON object

    Returns:

       Generator of lists that each represent a path inside the object.

    Usage::

       >>> list(generate_paths(some_nested_json))
       [['key1, 'key2', key3']['another_object', 'another_key', 1']]

    """
    if path is None:
        path = []
    if isinstance(json_result, dict):
        for k, v in json_result.items():
            current_path = path[:]
            current_path.append(k)
            yield current_path

            if isinstance(v, dict) or isinstance(v, list):
                yield from generate_paths(v, path=current_path)

    elif isinstance(json_result, list):
        for idx, item in enumerate(json_result):
            current_path = path[:]
            current_path.append(idx)
            yield from generate_paths(item, path=current_path)
    else:
        yield path


def generate_paths_to_key(json_result, key, path=None):
    """Generator function for introspecting a nested JSON object and finding all
    routes to a particular key. If, for instance, the key 'href' appears inside
    the JSON object 11 times, this generator will return 11 separate results,
    representing pathways to those 11 results.

    The values at these pathways can be returned with `get_nested_value' or set
    with `set_nested_value`.

    Args:

       `json_result` -- JSON object
       `key` -- Key to find routes for

    Returns:

       Generator of lists that each represent one path to the key passed in.

    Usage::

       >>> list(generate_paths(some_nested_json, 'SOMEKEY'))
       [['key1, 'key2', key3']['another_object', 'another_key', 1']]
       >>> get_nested_value(some_nested_json, ['key1, 'key2', key3'])
       'SOMEVALUE'

    """
    if path is None:
        path = []
    if isinstance(json_result, dict):
        for k, v in json_result.items():
            if key == k:
                current_path = path[:]
                current_path.append(key)
                yield current_path
            else:
                current_path = path[:]
                current_path.append(k)
                yield from generate_paths_to_key(v, key, path=current_path)

    elif isinstance(json_result, list):
        for idx, item in enumerate(json_result):
            current_path = path[:]
            current_path.append(idx)
            yield from generate_paths_to_key(item, key, path=current_path)


def reverse_result(func):
    """The recursive function `get_path` returns results in order reversed
    from desired. This decorator just reverses those results before returning
    them to caller.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is not None:
            return result[::-1]
    return inner


@reverse_result
def get_path(json_result, key, path=None):
    """Find first occurrence of a key inside a nested dictionary. This is helpful
    only for unique keys across all nested brances of a dictionary and will
    return confusing results for dictionaries that do not conform to this rule.

    Returns list of results::

       >>> content =
       ...  {'attributes':
       ...      {'contentencoded': None, 'tags': [None], 'published': None,
       ...       'contenttemplated': None, 'title': None, 'guid': inf,
       ...       'description': None, 'byline': None, 'teaser': None},
       ...       'version': None, 'links': {'collection': [inf], '
       ...        item': [None],
       ...   'links' : [{'creator': 'https://someurl'}]
       ...     }
       >>> get_path(content, 'attributes')
       ['attributes']
       >>> get_path(content, 'tags')
       ['attributes', 'tags']
       >>> get_path(conent, 'creator')
       ['links', 0, 'creator']

    Args:

       `json_result` -- nested JSON dictionary values
       `key` -- key whose path we'd like to discover

    Kwargs:

       `path` -- The path gets built on recursive calls.

    This function is only valid for unique keys. Use `generate_paths` to
    find all routes to a particular key inside a JSON object.
    """
    if path is None:
        path = []
    if isinstance(json_result, int) or isinstance(json_result, str):
        path = []
        return path
    elif isinstance(json_result, dict):
        for k, v in json_result.items():
            if key == k:
                path.append(key)
                return path
            else:
                result = get_path(v, key, path)
                if result:
                    path.append(k)
                    return path
    elif isinstance(json_result, list):
        for idx, item in enumerate(json_result):
            result = get_path(item, key, path)
            if result:
                path.append(idx)
                return path


def get_nested_value(json_result, keys):
    """Returns JSON value retrieved by following *known* keys.

    This function makes it easy to plumb the depths of a nested
    dict with using an iterable of keys and integers.

    It will go as deep as keys/indices exist and return None if it
    doesn't find one or if it runs into a value it can't parse.

    Usage::

       >>> some_dict = {'links': {'collection' : [{'a': 'b'}]}}
       >>> get_nested_value(some_dict, ['links', 'collection'])
       [{'a': 'b'}]
       >>> # with a list index
       >>> get_nested_value(some_dict, ['links', 'collection', 0, 'a'])
       'b'
    """
    if json_result is None or len(keys) < 1:
        return
    if len(keys) == 1:
        key = keys[0]
        if all((isinstance(key, int),
                isinstance(json_result, list))) and key < len(json_result):
            return json_result[key]
        elif isinstance(json_result, dict):
            return json_result.get(key, None)
    else:
        key, *keys = keys
        if all((isinstance(key, int),
                isinstance(json_result, list))) and key < len(json_result):
            return get_nested_value(json_result[key], keys)
        elif isinstance(json_result, dict):
            return get_nested_value(json_result.get(key, None), keys)


def set_nested_value(json_result, path, newvalue):
    """If you have a set of key and/array indices that conform
    to a nested JSON object, you can use this function to set
    the value retrieved by those keys for that particular JSON object.

    Args:

       `json_result` -- Nested JSON Object
       `keys` -- tuple or list of keys to navigate the object
       `newvalue` -- Replacement value

    Usage::

       >>> some_dict = {'links': {'collection' : [{'a': 'b'}]}}
       >>> set_value(some_dict, ['links', 'collection', 0, 'a'], 'c')
       [{'a': 'c'}]

    It is also possible to write a find-and-replace by combining
    `set_value` with `search_with_keys`::

        >>> for items in search_keys(json_results, keys, searchval):
        ...  set_nested_value(item, keys, newval)


    Returns:
       Edited dictionary
    """
    *keys, last_key = path
    if len(keys) > 0:
        editable = get_nested_value(json_result, keys)
        editable[last_key] = newvalue
    else:
        key, *_ = path
        json_result[key] = newvalue
