import unittest
import draughtsman
from refract.contrib.apielements import ParseResult


class DraughtsmanTests(unittest.TestCase):
    def test_parse_valid_blueprint(self):
        parse_result = draughtsman.parse('# My API')

        self.assertIsInstance(parse_result, ParseResult)
        self.assertEqual(parse_result.api.title.defract, 'My API')
