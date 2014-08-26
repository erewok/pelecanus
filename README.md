# pelecanus

Pelecanus: an application for navigating and editing nested JSON.

Named 'pelecanus' after Pelecanus occidentalis, the [brown Pelican of California and the Eastern Pacific](http://www.nps.gov/chis/naturescience/brown-pelican.htm), which is a wonderful bird and which deserves to have something named after it but also because I got tired of writing "NestedJson".


## Project Goals

JSON is a recursive data structure, so this module has been created in order to (hopefully) make parsing JSON easier to deal with.

Often, it's necessary to explore a JSON object without knowing precisely where things are (in the case of Hypermedia, for example). By creating a recursive data structure, we can facilitate such tasks as retrieving key-value pairs, iterating through the data structure, and searching for elements in the data structure.

There are limitations, however: no JSON structure that has keys deeper
than Python's recursion limit (default: 1000 stack frames) will work.

In addition, a JSON object that is a top-level array won't work.

Otherwise, there may be some things in here (hopefully) that will make your job dealing with nested JSON easier.


## How to Use
`pelecanus` offers `PelicanJson` objects, which are nested JSON objects that provide a few methods to make it easier to navigate and edit nested JSON objects.

At the moment, `PelicanJson` objects can only handle JSON objects at the top-level, not arrays.

To create an object, you can pass the constructor a Python dictionary created from a JSON dump:

```python
>>> content = {'links': {'attributes': [{'href': 'somelink'}]}}
>>> from pelecanus import PelicanJson
>>> pelican = PelicanJson(content)
```

Once you have PelicanJson object, you can find all the nested paths and the values located at those paths:

```python
>>> for item in pelican.enumerate():
...   print(item)
(['links', alternate', 0, 'href'], 'somelink')
```

You can also get back the value from a nested path:

```python
>>> pelican.get_nested_value(['links', alternate', 0, 'href'])
'somelink'
```

If you want to change a nested value, you can use the `set_nested_value` command to do so:

```python
>>> pelican.set_nested_value(['links', alternate', 0, 'href'], 'newvalue')
>>> pelican.get_nested_value(['links', alternate', 0, 'href'])
'newvalue'
```

A PelicanJson object is a modified version of a Python dictionary, so you can use all of the normal dictionary methods, but it will mostly return nested results (which means you will often get duplicate 'keys'):

```python
>>> list(pelican.keys())
['links', 'attributes', 'href']
```

Other useful methods include `convert` and `serialize` for turning the object back into a plain Python dictionary and for returning a JSON dump, respectively:

```python
>>> pelican.convert() == content
True
>>> import json
>>> json.loads(pelican.serialize()) == content
True
```

You can also use the methods `searchkey` and `searchvalue` in order to find all the paths that leads to keys or values you are searching for. Finally, `pluck` is for retrieving a dictionary containing a particular key-value pair:

```python
>>> EXAMPLE
```