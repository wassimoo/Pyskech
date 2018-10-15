#
# Wrangler - Automated data wrangling for data scientists
# Copyright (C) 2018 Wassim Bougarfa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
sys.path.append('..')

from parsers.json_parser import JsonParser
import unittest


class InputAttrExceptionsTest(unittest.TestCase):
    """
        Required Attributes:
            url, format
        Optional:
            encoding, async
    """
    @classmethod
    def test_unexisten_file(self):
        self.assertRaises(FileNotFoundError, JsonParser(''))

    @classmethod
    def test_no_input_attr(self):
        self.assertRaises(Exception, JsonParser().parse_input_data())

    @classmethod
    def test_no_url_param(self):
        inputd = dict()
        self.assertRaises(Exception, JsonParser().parse_input_data(inputd))

    @classmethod
    def test_no_url_schema(self):
        url = '://www.example.com'
        inputd = dict(url=url)
        self.assertRaises(Exception, JsonParser().parse_input_data(inputd))

    @classmethod
    def test_unsupported_encoding(self):
        url = 'http://www.example.com'
        #_format = 'csv'
        encoding = 'xyz'
        inputd = dict(url=url, encoding=encoding)
        #parser = JsonParser()
        # parser.parse_input_data(inputd)
        self.assertRaises(Exception, JsonParser().parse_input_data(inputd))

    @classmethod
    def test_no_format_param(self):
        url = 'http://www.example.com'
        #_format = 'csv'
        inputd = dict(url=url)
        self.assertRaises(Exception, JsonParser().parse_input_data(inputd))

    @classmethod
    def test_unsupported_format(self):
        url = 'http://www.example.com'
        _format = 'someformat'
        inputd = dict(url=url, format=_format)
        self.assertRaises(Exception, JsonParser().parse_input_data(inputd))



if __name__ == '__main__':
    pass