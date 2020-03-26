import unittest
import draughtsman
from refract.contrib.apielements import ParseResult


class DraughtsmanTests(unittest.TestCase):
    def test_parse_valid_blueprint(self):
        parse_result = draughtsman.parse('# My API')

        self.assertIsInstance(parse_result, ParseResult)
        self.assertEqual(parse_result.api.title.defract, 'My API')

    def test_parse_valid_blueprint_with_source_maps(self):
        parse_result = draughtsman.parse('# My API', generate_source_map=True)

        self.assertIsInstance(parse_result, ParseResult)
        self.assertEqual(parse_result.api.title.defract, 'My API')
        self.assertEqual(
            parse_result.api.title.attributes.get('sourceMap').defract,
            [[[0, 8]]]
        )
