# Draughtsman

[API Blueprint](https://apiblueprint.org) Parser for Python 3. Draughtsman is a
Python binding for the API Blueprint parser
[drafter](https://github.com/apiaryio/drafter).

## Installation

```shell
$ pip install draughtsman
```

Draughtsman requires the drafter library installed onto your system. Consult
the [drafter installation](https://github.com/apiaryio/drafter#install)
instructions for further information. Using Homebrew on macOS, Drafter can be
installed via:

```shell
$ brew install drafter
```

## Usage

```python
>>> from draughtsman import parse
>>>
>>> parse_result = parse('# My API')
>>> parse_result.api.title.defract
'My API'
```

Draughtsman provides a `parse` function which returns a Refract
[ParseResult](http://python-refract.readthedocs.io/en/latest/apielements.html#parseresult).
See [Python Refract](http://python-refract.readthedocs.io/en/latest/) for more
information interacting with the parse result.

### CLI

Draughtsman provides a convenience shell to parse an API Blueprint and interact
with the parse result.

```shell
$ python -m draughtsman example.apib
>>> parse_result
<ParseResult content=[<Category content=[]>]>
>>> parse_result.annotations
[]
>>> parse_result.api.title
<String content='My API'>
```
