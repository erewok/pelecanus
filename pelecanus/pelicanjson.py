"""JSON is a recursive data structure, so this module has been created in
order to (hopefully) make parsing JSON easier to deal with.

Often, it's necessary to explore a JSON object without knowing precisely where
things are (in the case of Hypermedia, for example). By creating a recursive
data structure, we can facilitate such tasks as retrieving key-value pairs,
iterating through the data structure, and searching for elements in the data
structure.

There are limitations, however: no JSON structure that has keys deeper
than Python's recursion limit (default: 1000 stack frames) will work.

In addition, a JSON object that is a top-level array won't work.
"""
import copy
import json
import collections


class PelicanJson(collections.MutableMapping):
    """PelicanJson objects are nested JSON objects that provide a few
    methods to make it easier to navigate and edit nested JSON objects.

    At the moment, this object can only handle JSON objects at the top-level,
    not arrays.

    To create an object, you can pass the constructor a Python
    dictionary created from a JSON dump::

       >>> content = {'links': {'attributes': [{'href': 'somelink'}]}}
       >>> pelican = PelicanJson(content)

    Once you have PelicanJson object, you can find all the nested paths and
    the values located at those paths::

       >>> for item in pelican.enumerate():
       ...   print(item)
       (['links', alternate', 0, 'href'], 'somelink')

    You can also get back the value from a nested path::

       >>> pelican.get_nested_value(['links', alternate', 0, 'href'])
       'somelink'

    If you want to change a nested value, you can use the `set_nested_value`
    command to do so::

       >>> pelican.set_nested_value(['links', alternate', 0, 'href'],
       ... 'newvalue')
       >>> pelican.get_nested_value(['links', alternate', 0, 'href'])
       'newvalue'

    A PelicanJson object is a modified version of a Python dictionary, so
    you can use all of the normal dictionary methods, but it will mostly return
    nested results (which means you will often get duplicate 'keys')::

       >>> list(pelican.keys())
       ['links', 'attributes', 'href']

    Other useful methods include `convert` and `serialize` for turning the
    object back into a plain Python dictionary and for returning a JSON dump,
    respectively::

       >>> pelican.convert() == content
       True
       >>> import json
       >>> json.loads(pelican.serialize()) == content
       True

    You can also `searchkey` and `searchvalue` in order to find all the paths
    that leads to keys or values you are searching for.
    """
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))
        for key, value in self.store.items():
            if isinstance(value, dict):
                self.store[key] = PelicanJson(value)
            elif isinstance(value, list):
                self.store[key] = self._update_from_list(value)
            else:
                self.store[key] = value

    def _update_from_list(self, somelist):
        temp_list = []
        for item in somelist:
            if isinstance(item, dict):
                temp_list.append(PelicanJson(item))
            elif isinstance(item, list):
                temp_list.append(self._update_from_list(item))
            else:
                temp_list.append(item)
        return temp_list

    def __contains__(self, searchkey):
        for key in iter(self):
            if key == searchkey:
                return True
        return False

    def __repr__(self):
        return "<PelicanJson: {}>".format(str(self.store))

    def __str__(self):
        return str(self.store)

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __len__(self):
        """Counts all keys and subkeys nested in the object.
        """
        return sum(1 for k in iter(self))

    def __iter__(self):
        """Iterates through the entire tree and returns all nested keys.
        """
        for k, v in self.store.items():
            yield k
            if type(v) == type(self):
                yield from iter(v)
            elif type(v) == list:
                for item in v:
                    if type(item) == type(self):
                        yield from iter(item)

    def items(self, path=None):
        """Yields path-value pairs from throughout the entire tree.
        """
        for k, v in self.store.items():
            yield k, v
            if type(v) == type(self):
                yield from v.items()
            elif type(v) == list:
                for list_item in v:
                    if type(list_item) == type(self):
                        yield from list_item.items()

    def enumerate(self, path=None):
        """Iterate through the PelicanJson object yielding 1) the full path to
        each value and 2) the value itself at that path.
        """
        if path is None:
            path = []
        for k, v in self.store.items():
            current_path = path[:]
            current_path.append(k)

            if type(v) == type(self):
                yield from v.enumerate(path=current_path)
            elif type(v) == list:
                for idx, list_item in enumerate(v):
                    list_path = current_path[:]
                    list_path.append(idx)
                    if type(list_item) == type(self):

                        yield from list_item.enumerate(path=list_path)
                    else:
                        yield list_path, list_item
            else:
                yield current_path, v

    def paths(self):
        """Uses enumerate to yield paths only
        """
        for path, _ in self.enumerate():
            yield path

    def keys(self):
        """Generator that iterates through the keys of the nested object same as
        `__iter__()`
        """
        # Rewrite in terms of `enumerate`
        yield from iter(self)

    def values(self):
        """Generator that returns values-only for the object.
        """
        # Rewrite in terms of `enumerate`
        yield from (v for k, v in self.enumerate())

    def convert(self):
        """Converts the object back to a native Python object (a nested dictionary)
        that is equal to the object passed in.
        """
        data = {}
        for k, v in self.store.items():
            if type(v) == type(self):
                data[k] = v.convert()
            elif type(v) == list:
                temp_list = []
                for list_item in v:
                    if type(list_item) == type(self):
                        temp_list.append(list_item.convert())
                    else:
                        temp_list.append(list_item)
                listcopy = copy.deepcopy(temp_list)
                data[k] = listcopy
            else:
                data[k] = v
        return data

    def serialize(self):
        """Returns JSON serialization of the object.
        """
        return json.dumps(self.convert())

    def count_key(self, key):
        """Returns a sum of the number of times a particular key appears in the object.
        """
        return sum(1 for k, v in self.items() if k == key)

    def search_key(self, searchkey, path=None):
        """Generator that returns the (various) paths for a particular key
        """
        if path is None:
            path = []
        for k, v in self.store.items():
            current_path = path[:]
            current_path.append(k)
            if k == searchkey:
                yield current_path

            if type(v) == type(self):
                yield from v.search_key(searchkey,
                                       path=current_path)
            elif type(v) == list:
                for idx, list_item in enumerate(v):
                    list_path = current_path[:]
                    list_path.append(idx)
                    if type(list_item) == type(self):
                        yield from list_item.search_key(searchkey,
                                                        path=list_path)

    def search_value(self, searchval, path=None):
        """Generator that returns the (various) paths for a particular value
        """
        if path is None:
            path = []
        for k, v in self.store.items():
            current_path = path[:]
            current_path.append(k)
            if v == searchval:
                yield current_path

            if type(v) == type(self):
                yield from v.search_value(searchval,
                                          path=current_path)
            elif type(v) == list:
                for idx, list_item in enumerate(v):
                    list_path = current_path[:]
                    list_path.append(idx)
                    if type(list_item) == type(self):
                        yield from list_item.search_value(searchval,
                                                          path=list_path)
                    elif list_item == searchval:
                        yield list_path

    def pluck(self, key, value):
        """Returns the _parent_ object that contains a particular key-value pair
        """
        for path in self.search_key(key):
            if self.get_nested_value(path) == value:
                if len(path) > 1:
                    path = path[:-1]
                    yield self.get_nested_value(path)
                else:
                    yield self

    def get_nested_value(self, path):
        """Retrieves nested value at the end of a path.
        """
        def valgetter(data, keys):
            if len(keys) <= 1:
                return data[keys[0]]
            else:
                key, *keys = keys
                return valgetter(data[key], keys)

        return valgetter(self.store, path)

    def set_nested_value(self, path, newvalue):
        """Sets a nested_value to a new value using the path provided.
        Path must already exist for path to be set.
        """
        *keys, last_key = path
        if len(keys) > 0:
            editable = self.get_nested_value(keys)
            editable[last_key] = newvalue
        else:
            key, *_ = path
            self.store[key] = newvalue

    def update_from_pelican(self, newdata):
        """Blends the data passed in to the PelicanJson dict, creating paths
        where necessary
        """
        for path, value in newdata.enumerate():
            try:
                self.set_nested_value(path, value)
            except (IndexError, KeyError):
                start, *rest = path
                if start in self.store:
                    self.update(newdata[start])
                else:
                    self.store[start] = newdata[start]

    def find_and_replace(self, matchval, replaceval):
        """Will replace all matched values with the replacement value
        passed in and will yield the paths associated with the
        changed values.
        """
        for path in self.search_value(matchval):
            self.set_nested_value(path, replaceval)
