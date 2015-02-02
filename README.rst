python-sourcemaps
=================
Python library for parsing and generating source maps.

Usage
-----
Overview
________
Example::

  >>> import sourcemaps
  >>> sourcemaps.discover('...')
  'jquery.min.map'
  >>> sourcemap = sourcemaps.decode('...')
  >>> sourcemap.tokens[3]
  <Token: dst_line=10 dst_column=10 src='jquery.js' src_line=50 src_col=200 name='lol'>
  >>> sourcemaps.encode(sourcemap)
  '{version: 3, mappings: 'AAAA,...', ...}'

Compatibility
_____________
 * Python 2.7
 * Python 3.3
 * PyPy
