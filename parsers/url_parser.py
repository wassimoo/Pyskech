#
# Peskech - Automated data wrangling for data scientists
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

from urllib.parse import urlsplit


class HTTPParser(object):
    def __init__(self, url: str = None, components: list = None):
        """ URL 
         Raises:
            Exception:
                * On no parameters given
                * On invalid HTTP.
            ValueError:
                * On invalid port.
        """
        if url == None:
            if components == None:
                raise Exception('No parameters given')
            else:
                self.url = self.assemble(components)
                self.components = self.disassemble(self.url)
        else:
            self.components = self.disassemble(url)
            self.url = self.assemble(self.components)

    def assemble(self, components: list) -> str:
        return ''.join(str(x) for x in components)

    def disassemble(self, url: str) -> list:
        """Parse HTTP URL compontents.

        Args:
            url: Valid HTTP URL.

        Returns:
            Parsed components.

        Raises:
            Exception:
                * On invalid HTTP.
            ValueError:
                * On invalid port.
        """
        components = [x.lower() for x in urlsplit(url, scheme='http')]
        if components[0] != 'http' and components[0] != 'https':
            raise Exception('None http url given')
        return components

class FTPParser(object):
    pass

class SFTPParser(object):
    pass