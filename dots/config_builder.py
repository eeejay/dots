# Dots - A braille translation program.
#
# Copyright (C) 2009 Eitan Isaacson
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

class ConfigBuilder(dict):
    def __init__(self):
        self['xml'] = _ConfigSection()
        self['translation'] = _ConfigSection()
        self['outputFormat'] = _ConfigSection()

    def __str__(self):
        s = ''
        for key in self.keys():
            s += '%s\n' % key
            for k,v in self[key].items():
                s += '\t%s %s\n' % (k ,v)
        return s

class _ConfigSection(dict):
    pass

if __name__ == "__main__":
    cb = ConfigBuilder()
    cb['xml']['semanticFiles'] = '*,nemeth.sem'
    cb['xml']['internetAccess'] = 'yes'
    cb['translation']['literaryTextTable'] = 'en-us-g2.ctb'
    cb['outputFormat']['cellsPerLine'] = 40
    cb['outputFormat']['linesPerPage'] = 25

    print str(cb)
