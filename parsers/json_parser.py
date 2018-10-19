#
# Peskech - Automated data structuring for data scientists
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
        self.__structure = {}
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

    def parse_structure(self, structuring_data: dict = None):
        """Parse and validate data structures.

            Raises:
                Exception: on invalide/unknown structure method

        """
        if structuring_data == None:
            if self.__file_content.get('structure') == None:
                raise Exception('No structure attribute provided')
            else:
                structuring_data = self.__file_content.get('structure')

        ################# Structuring Methods ################
        # class-file       ==> If $file parameter is found <==
        # inline-class     ==>   If alias surronded by {}  <==
        # inline-attribute ==>         otherwise           <==
        ######################################################

        for structure in structuring_data:
            # NOTE: Overwrite existing structures referenced by the same key
            # pure value given -> iniline_attribute
            if type(structuring_data[structure]) != dict:
                self.__structure.update(
                    self._parse_inline_attributes(structuring_data[structure]))
            elif structure[0] == '{' and structure[-1] == '}':
                self.__structure.update(
                    self._parse_inline_class(structuring_data[structure]))
            elif structuring_data[structure].get('$file') != None:
                self.__structure.update(self._parse_class_file(self._splitheaders(
                    structure), structuring_data[structure]))
            else:
                raise Exception('unknown structuring method at ' + structure)

    def _parse_class_file(self, headers: list, params: dict) -> dict:
        """Parse a class-file structuring method.

        Args: 
            headers: specified headers attributes.
            params: Structuring rules

        Raises:
            Exception:
                * No $file parameter specified.
                * No $class parameter specified.
                * Invalid argument alias name.
        """
        io_params = {}  # provided by $load, $extract, $args
        # No need to check, Wouldn't call this method if didn't exist.
        _file = params.get('$file')
        _class = params.get('$class')
        if _class == None:
            raise Exception(
                'Attempted to use class-file structuring without a specified class, consider using $class parameter')
        # use header if no object alias has been specified,
        # throw Exception if header groupe is used.
        io_params['alias'] = params.get('$alias')
        if io_params['alias'] == None:
            if len(headers) != 1:
                raise Exception(
                    'Attempted to use class-file structuring based on more than one header, consider using $alias')
            else:
                io_params['alias'] = headers[0]

        io_params['load'] = params.get('$load')
        io_params['extract'] = params.get('$extract')

        ####### Start parsing Args #######
        # Eliminate duplicated aliases,
        # Validate Aliases,
        # Args Values are Evaluated by the worker.
        ##################################
        if params.get('$args') != None:
            # construct with header(s) value(s)
            io_params['args'] = dict([(x, '$obj.'+x) for x in headers])
            for arg_alias in params['$args']:
                # Check argument alias validity:
                # Either it exists in final args dict or passes test validity.
                if io_params['args'].get(arg_alias) != None or arg_alias.isidentifier():
                    io_params['args'][arg_alias] = params['$args'][arg_alias]
                else:
                    raise Exception(
                        'Invalid argument alias given {}'.format(arg_alias))
        return {io_params['alias']: (_file, _class, io_params)}

    def _parse_inline_class(self, params: dict) -> dict:
        print('From _parse_inline_class : Still working on this ...')

    def _parse_inline_attributes(self, params: dict) -> dict:
        raise Exception('From _parse_inline_attributes : Still working on this ...')

    def _splitheaders(self, headers: str) -> list:
        return [x.strip() for x in headers.split(',')]
