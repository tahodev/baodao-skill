#!/usr/bin/env python3
"""Offline regression tests for response-error detection, without network probes."""
import ast
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

source = Path(__file__).resolve().parents[1] / 'scripts' / 'check-urls.py'
tree = ast.parse(source.read_text())
nodes = [node for node in tree.body if getattr(node, 'name', '') in ('VisibleTextParser', 'api_error')]
namespace = {'re': re, 'HTMLParser': HTMLParser}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), 'exec'), namespace)
api_error = namespace['api_error']


class ErrorDetectionTests(unittest.TestCase):
    def test_valid_html_prefetch_is_not_error(self):
        self.assertIsNone(api_error('<!DOCTYPE html><html><head><link rel="prefetch" href="/_nuxt/error-404.css"></head><body>AQI data</body></html>'))

    def test_script_and_style_are_not_page_errors(self):
        self.assertIsNone(api_error('<html><script>const fallback="ERROR-404";</script><style>.ERROR-404 {}</style><body>API terms</body></html>'))

    def test_visible_html_error_still_fails(self):
        self.assertIsNotNone(api_error('<html><body><h1>ERROR-404</h1></body></html>'))

    def test_plain_text_error_still_fails(self):
        self.assertIsNotNone(api_error('ERROR-404: missing dataset'))

    def test_json_error_still_fails(self):
        self.assertIsNotNone(api_error('{"resultCode":"ERROR-404"}'))

    def test_auth_error_still_detected(self):
        self.assertIsNotNone(api_error('API KEY 無效'))


if __name__ == '__main__':
    unittest.main()
