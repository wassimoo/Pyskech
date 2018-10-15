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

from enum import Enum
import csv

class Parser(object):

    def __init__(self, file_name: str, **headers: dict):
        """Parser Constructor.

        Args:
            headers: 
                Specify CSV file headers and their default neutral value,
                The neutral value is necesseary to replace Na fields &
                To determinate columns datatype.
                EXAMPLE:
                     0.  -> will be considered as a float.
                     0   -> will be considered as an int.
        """
        self.__file_name = file_name
        self.__parsing_headers = headers
        self.parsed_data = []

    def parse(self):
        with open(self.__file_name) as input_stream:
            raw_data = csv.reader(input_stream, delimiter=',')
            self.__validate_headers(raw_data.__next__())
            for row in raw_data:
                self.parsed_data.append(row)
        return self

    def __validate_headers(self, file_headers: list) -> None:
        """Validates parsing headers.

        Unmentioned header will be excluded, As well as unexisting ones.

        Args:
            file_header: Usually the first line of the CSV file.

        """

        final_headers = []  # filtred headers as described in methods docs
        for header in file_headers:
            header_dflt_value = self.__parsing_headers.get(header)
            if header_dflt_value != None:  # file header is mentionned
                # No need for an extra check here
                self.__check_is_valid_datatype(type(header_dflt_value))
                final_headers.append({header: header_dflt_value})
        self.__parsing_headers = final_headers

    def __check_is_valid_datatype(self, datatype) -> None:
        """Validates given datatype.

            A given datatype is considered valid only if it's a known python permitive datatype
            or an instance of object which implements CSV_IO interface (work in progress).

            Raises: 
                Exception
        """
        if type(datatype) is type:  # is a datatype
            if datatype in [int, float, complex, str, bool]:  # and is a premitive datatype
                return
            else:
                raise Exception(
                    'Caught trying to parse values to an unsupported datatype ``{0}``'.format(datatype))
        else:
            raise Exception(
                'Unknown datatype given : ``{0}'.format(datatype))
