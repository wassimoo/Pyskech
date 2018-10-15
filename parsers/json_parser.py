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

from .url_parser import *
import json
import re

SUPPORTED_ENCODING = ['ASCII', 'UTF-8', 'UTF-16']
DEFAULT_ENCODING = 'UTF-8'
SUPPORTED_DATA_FORMATS = ['CSV', 'XLS', 'TXT']


class JsonParser(object):

    def __init__(self, file_path: str = None):
        """
        Raises:
            FileNotFoundError
        """
        self.__file_path = file_path
        self.__file_content = {}
        self.__input = {}
        if file_path != None:
            self.__loadFile()

    def __loadFile(self):
        with open(self.__file_path) as input_stream:
            self.__file_content = json.load(input_stream)

    def parse_input_data(self, input_data: dict = None):
        """
            Raises:
                Exception:
                    * No `input` attribute provided
                    * No `url` attribute provided
                    * Invalide URL provided
                    * Unsupported encoding provided
                    * No `format` attribute provided
                    * Unsupported data format provided
        """
        if input_data == None:
            if self.__file_content.get('input') == None:
                raise Exception('No input attribute provided')
            else:
                input_data = self.__file_content['input']
       ########################## URL ##########################
        url = input_data.get('url')
        if url == None:
            raise Exception('No input URL provided')

        scheme = url[0:url.find('://')]
        if scheme == '':
            raise Exception("Invalid URL: can't parse URL scheme.")
        else:
            scheme = scheme.lower()

        if scheme == 'http' or scheme == 'https':
            self.__input['url'] = HTTPParser(url)
        elif scheme == 'ftp':
            self.__input['url'] = FTPParser(url)
        elif scheme == 'sftp':
            self.__input['url'] = SFTPParser(url)
        else:
            pass  # TODO: Treat as a local file
       ########################## URL ##########################

       ######################## Encoding #######################
        if input_data.get('encoding') == None:
            self.__input['encoding'] = DEFAULT_ENCODING
        else:
            encoding = input_data['encoding'].upper()
            if encoding in SUPPORTED_ENCODING:
                self.__input['encoding'] = encoding
            else:
                raise Exception('Unsupported encoding : {}'.format(encoding))
       ######################## Encoding #######################

       ######################## Format #######################
        if input_data.get('format') == None:
            raise Exception('No data format provided')
        else:
            _format = input_data['format'].upper()
            if _format in SUPPORTED_DATA_FORMATS:
                self.__input['format'] = _format
            else:
                raise Exception(
                    'Unsupported input data format provided : {}'.format(_format))
       ######################## Format #######################

       ######################## ASYNC #######################
        self.__input['async'] = input_data['format'] if type(
            input_data['format']) == bool else False
       ######################## ASYNC #######################
