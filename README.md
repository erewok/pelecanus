# pelecanus ![](https://travis-ci.org/pellagic-puffbomb/pelecanus.svg?branch=master)

A Python3 application for navigating and editing nested JSON, named 'pelecanus' after Pelecanus occidentalis, the [brown Pelican of California and the Eastern Pacific](http://www.nps.gov/chis/naturescience/brown-pelican.htm), which is a wonderful bird, but also named such because I got tired of writing "NestedJson".

This application has been built-for and tested on Python3.3 and Python3.4 (it makes ample of use of `yield from`).

## Project Goals

Often, it's necessary to explore a JSON object without knowing precisely where things are (in the case of Hypermedia, for example). By creating a recursive data structure, we can facilitate such tasks as retrieving key-value pairs, iterating through the data structure, and searching for elements in the data structure.

There are limitations, however: no JSON structure that has keys deeper than Python's recursion limit will work. In addition, a JSON object that is a top-level array won't work.

## How to Use

To install for Python3.3+, simply do:

```
$ pip install pelecanus
```

`pelecanus` offers `PelicanJson` objects, which are nested dictionaries created from valid JSON objects, and `PelicanJson` objects provide a few methods to make it easier to navigate and edit nested JSON objects.

To create a PelicanJson object, you can pass the constructor a Python dictionary created from a JSON dump (or a simple Python dictionary that could be a valid JSON object):

```python
>>> content = {'links': {'attributes': [{'href': 'somelink'}]}}
>>> from pelecanus import PelicanJson
>>> pelican = PelicanJson(content)
```

#### Enumerate

Once you have a `PelicanJson` object, probably one of the most useful things to do is to find all the nested paths and the values located at those paths. The `enumerate` method has been provided for this purpose:

```python
>>> for item in pelican.enumerate():
...   print(item)
(['links', 'alternate', 0, 'href'], 'somelink')
...
```

The integers that appear in the nested path may represent list indices. In this case, `['links', alternate', 0, 'href']` actually represents:

1. A dictionary with a key `links`, which points to...
2. Another dictionary which contains a key 'alternate', which contains...
3. A list, the first item of which...
4. Is a dictionary containing the key `href`.

`enumerate`, like most methods in a `PelicanJson` object, returns a generator. If you want just the paths and not their associated values, use the `paths` method:

```python
>>> for item in pelican.paths():
...   print(item)
['links', 'alternate', 0, 'href']
```

#### Getting and Setting Values

You can retrieve the value from a nested path using `get_nested_value`:

```python
>>> pelican.get_nested_value(['links', 'alternate', 0, 'href'])
'somelink'
```

If you want to change a nested value, you can use the `set_nested_value` method:

```python
>>> pelican.set_nested_value(['links', 'alternate', 0, 'href'], 'newvalue')
>>> pelican.get_nested_value(['links', 'alternate', 0, 'href'])
'newvalue'
```

#### Keys, Values, Items, etc.

A `PelicanJson` object is a modified version of a Python dictionary, so you can use all of the normal dictionary methods, but it will mostly return nested results (which means you will often get duplicate `keys`):

```python
>>> list(pelican.keys())
['links', 'attributes', 'href', ...]
```

`values` is only going to return values that exist at endpoints, at the inside-most points of all nested objects:

```python
>>> list(pelican.values())
['somelink']
```

While `items` attempts to do double-duty, returning each key in the tree and its corresponding value:

```python
>>> list(pelican.items())
[('links', <PelicanJson: {'attributes': [<PelicanJson: {'href': 'somelink'}>]}>), ('attributes', [<PelicanJson: {'href': 'somelink'}>]), ('href', 'somelink')]
```

You can also use `in` to see if a key is somewhere inside the dictionary (even if it's a nested key):

```python
>>> 'attributes' in pelican
True
```


#### Turning it back into a plain dictionary or JSON

Other useful methods include `convert` and `serialize` for turning the object back into a plain Python dictionary and for returning a JSON dump, respectively:

```python
>>> pelican.convert() == content
True
>>> import json
>>> json.loads(pelican.serialize()) == content
True
```


#### Searching Keys and Values

You can also use the methods `search_key` and `search_value` in order to find all the paths that lead to keys or values you are searching for (data comes from the [Open Library API](https://openlibrary.org/developers/api)). 

```python
>>> book = {'ISBN:9780804720687': {'preview': 'noview', 'bib_key': 'ISBN:9780804720687', 'preview_url': 'https://openlibrary.org/books/OL7928788M/Between_Pacific_Tides', 'info_url': 'https://openlibrary.org/books/OL7928788M/Between_Pacific_Tides', 'thumbnail_url': 'https://covers.openlibrary.org/b/id/577352-S.jpg'}}
>>> pelican = PelicanJson(book)
>>> for path in pelican.search_key('preview'):
...   print(path)
['ISBN:9780804720687', 'preview']
>>> for path in pelican.search_value('https://covers.openlibrary.org/b/id/577352-S.jpg'):
...  print(path)
['ISBN:9780804720687', 'thumbnail_url']
```

In addition, `pluck` is for retrieving the whole object that contains a particular key-value pair:

```python
>>> list(pelican.pluck('preview', 'noview'))
[<PelicanJson: {'preview': 'noview', 'thumbnail_url': 'https://covers.openlibrary.org/b/id/577352-S.jpg', 'bib_key': 'ISBN:9780804720687', 'preview_url': 'https://openlibrary.org/books/OL7928788M/Between_Pacific_Tides', 'info_url': 'https://openlibrary.org/books/OL7928788M/Between_Pacific_Tides'}>]
```

#### Find and Replace

Finally, there is also a `find_and_replace` method which searches for a particular value and replaces it with a passed-in replacement value:

```python
>>> pelican.search_value('ISBN:9780804720687')
['ISBN:9780804720687', 'bib_key']
>>> pelican.find_and_replace('ISBN:9780804720687', 'NEW ISBN')
>>> pelican.get_nested_value(['ISBN:9780804720687', 'bib_key'])
'NEW ISBN'
```

This can, of course, be dangerous, so use with caution.

# TO DO

* Separate all methods out of `PelicanJson` class for use on free-floating Python dictionaries that come from netsed JSON objects.

![](http://i.imgur.com/f6bG1XN.jpg)
