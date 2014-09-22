# The unit tests are based on
# https://github.com/mattrobenolt/python-sourcemap
from sourcemap.core import (decode_sourcemap, decode_vlqs, discover_sourcemap,
    encode_sourcemap)
import json
import unittest

class DiscoverTestCase(unittest.TestCase):
    def test_finds_sourcemap(self):
        fixture = """
hey
this is some code
it's really awesome
//@ sourceMappingURL=file.js
"""
        self.assertFoundSourcemap(fixture, 'file.js')

    def test_finds_sourcemap_alt(self):
        fixture = """
hey
this is some code
it's really awesome
//# sourceMappingURL=file.js
"""
        self.assertFoundSourcemap(fixture, 'file.js')

    def test_doesnt_find_sourcemap(self):
        fixture = """
there
is no sourcemap
here
"""
        self.assertNotFoundSourcemap(fixture)

    def assertNotFoundSourcemap(self, fixture):
        self.assertIsNone(discover_sourcemap(fixture))

    def assertFoundSourcemap(self, fixture, expected):
        self.assertEqual(discover_sourcemap(fixture), expected)

class SourceMapTestCase(unittest.TestCase):
    def get_fixtures(self, base):
        source = open('tests/fixtures/%s.js' % base).read()
        minified = open('tests/fixtures/%s.min.js' % base).read()
        min_map = open('tests/fixtures/%s.min.map' % base).read()
        return source, minified, min_map

    def compare_sourcemaps(self, x, y):
        xdata = json.loads(x)
        ydata = json.loads(y)
        assert len(xdata['names']) == len(ydata['names'])
        assert xdata['sources'] == ydata['sources']
        assert xdata['mappings'].count(';') == ydata['mappings'].count(';')
        for encoded_line, orig_line in zip(xdata['mappings'].split(';'),
                                           ydata['mappings'].split(';')):
            assert [decode_vlqs(s)[:4] for s in encoded_line.split(',')] == \
                   [decode_vlqs(s)[:4] for s in orig_line.split(',')]

    def test_jquery(self):
        source, minified, min_map = self.get_fixtures('jquery')

        source_lines = source.splitlines()

        assert discover_sourcemap(minified) == 'jquery.min.map'

        sourcemap = decode_sourcemap(min_map)
        assert sourcemap.raw == json.loads(min_map)
        for token in sourcemap.tokens:
            # Ignore tokens that are None.
            # There's no simple way to verify they're correct
            if token.name is None:
                continue
            source_line = source_lines[token.src_line]
            start = token.src_col
            end = start + len(token.name)
            substring = source_line[start:end]

            # jQuery's sourcemap has a few tokens that are identified
            # incorrectly.
            # For example, they have a token for 'embed', and
            # it maps to '"embe', which is wrong. This only happened
            # for a few strings, so we ignore
            if substring[0] == '"':
                continue
            assert token.name == substring

        self.compare_sourcemaps(encode_sourcemap(sourcemap), min_map)

    def test_coolstuff(self):
        source, minified, min_map = self.get_fixtures('coolstuff')

        source_lines = source.splitlines()

        assert discover_sourcemap(minified) == 'tests/fixtures/coolstuff.min.map'

        sourcemap = decode_sourcemap(min_map)
        min_map_data = json.loads(min_map)
        assert sourcemap.raw == min_map_data
        for token in sourcemap.tokens:
            if token.name is None:
                continue

            source_line = source_lines[token.src_line]
            start = token.src_col
            end = start + len(token.name)
            substring = source_line[start:end]
            assert token.name == substring

        self.compare_sourcemaps(encode_sourcemap(sourcemap), min_map)

    def test_unicode_names(self):
        _, _, min_map = self.get_fixtures('unicode')

        # This shouldn't blow up
        self.compare_sourcemaps(encode_sourcemap(decode_sourcemap(min_map)), min_map)
