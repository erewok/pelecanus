# pelecanus | ![](https://travis-ci.org/pellagic-puffbomb/pelecanus.svg?branch=master)

Pelecanus: a Python3 application for navigating and editing nested JSON, named 'pelecanus' after Pelecanus occidentalis, the [brown Pelican of California and the Eastern Pacific](http://www.nps.gov/chis/naturescience/brown-pelican.htm), which is a wonderful bird and which deserves to have something named after it but also named such because I got tired of writing "NestedJson". ![](https://flic.kr/p/m51Qd3)

This application has been built-for and tested on Python3.3 and Python3.4 (it makes ample of use of `yield from`).

## Project Goals

Often, it's necessary to explore a JSON object without knowing precisely where things are (in the case of Hypermedia, for example). By creating a recursive data structure, we can facilitate such tasks as retrieving key-value pairs, iterating through the data structure, and searching for elements in the data structure.

There are limitations, however: no JSON structure that has keys deeper than Python's recursion limit (default: 1000 stack frames) will work. In addition, a JSON object that is a top-level array won't work.

Otherwise, there may be some things in here that will, hopefully, make your job dealing with nested JSON easier.

## How to Use
`pelecanus` offers `PelicanJson` objects, which are nested JSON objects that provide a few methods to make it easier to navigate and edit nested JSON objects.

To create a PelicanJson object, you can pass the constructor a Python dictionary created from a JSON dump (or a simple Python dictionary that could be a valid JSON object):

```python
>>> content = {'links': {'attributes': [{'href': 'somelink'}]}}
>>> from pelecanus import PelicanJson
>>> pelican = PelicanJson(content)
```

Once you have a `PelicanJson` object, you can find all the nested paths and the values located at those paths using the `enumerate` method:

```python
>>> for item in pelican.enumerate():
...   print(item)
(['links', alternate', 0, 'href'], 'somelink')
```

This method like most of those in a `PelicanJson` object returns a generator. If you want just the paths and not their associated values, use the `paths` method:

```python
>>> for item in pelican.paths():
...   print(item)
['links', alternate', 0, 'href']
```

You can also get back the value from a nested path:

```python
>>> pelican.get_nested_value(['links', alternate', 0, 'href'])
'somelink'
```

If you want to change a nested value, you can use the `set_nested_value` method:

```python
>>> pelican.set_nested_value(['links', alternate', 0, 'href'], 'newvalue')
>>> pelican.get_nested_value(['links', alternate', 0, 'href'])
'newvalue'
```

A PelicanJson object is a modified version of a Python dictionary, so you can use all of the normal dictionary methods, but it will mostly return nested results (which means you will often get duplicate 'keys'):

```python
>>> list(pelican.keys())
['links', 'attributes', 'href', ...]
```

Other useful methods include `convert` and `serialize` for turning the object back into a plain Python dictionary and for returning a JSON dump, respectively:

```python
>>> pelican.convert() == content
True
>>> import json
>>> json.loads(pelican.serialize()) == content
True
```

You can also use the methods `search_key` and `search_value` in order to find all the paths that lead to keys or values you are searching for. Finally, `pluck` is for retrieving a dictionary containing a particular key-value pair:

```python
>>> book = {'ISBN:9780804720687': {'preview': 'noview', 'bib_key': 'ISBN:9780804720687', 'preview_url': 'https://openlibrary.org/books/OL7928788M/Between_Pacific_Tides', 'info_url': 'https://openlibrary.org/books/OL7928788M/Between_Pacific_Tides', 'thumbnail_url': 'https://covers.openlibrary.org/b/id/577352-S.jpg'}}
>>> pelican = PelicanJson(book)
>>> for path in pelican.search_key('preview'):
...   print(path)
['ISBN:9780804720687', 'preview']
>>> for path in pelican.search_value('ISBN:9780804720687'):
...  print(path)
['ISBN:9780804720687', 'bib_key']
>>> list(pelican.pluck('preview', 'noview'))
[<PelicanJson: {'thumbnail_url': 'https://covers.openlibrary.org/b/id/577352-S.jpg', 'bib_key': 'ISBN:9780804720687', 'preview_url': 'https://openlibrary.org/books/OL7928788M/Between_Pacific_Tides', 'info_url': 'https://openlibrary.org/books/OL7928788M/Between_Pacific_Tides', 'preview': 'noview'}>]
```

Finally, there is also a `find_and_replace` method which searches for a particular value and replaces it with a passed-in replacement value:

```python
>>> pelican.find_and_replace('ISBN:9780804720687', 'NEW ISBN')
>>> pelican.get_nested_value(['ISBN:9780804720687', 'bib_key'])
'NEW ISBN'
```

# TO DO

* Separate all methods out of `PelicanJson` class for use on free-floating Python dictionaries that come from netsed JSON objects.
