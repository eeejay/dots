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
import os, tempfile, host_settings, sys, gtk


class DotsProject(gtk.TextBuffer):
    def __init__(self, input_file):
        gtk.TextBuffer.__init__(self)
        self.input_file = input_file
        self.config_text = None

    def transcribeBraille(self, config_text):
        self.config_text = config_text
        self._transcribeBraille()

    def _transcribeBraille(self):
        # Write config file.
        fd, config_fn = tempfile.mkstemp('.config','dots_')
        fconfig = os.fdopen(fd, 'w')
        fconfig.write(self.config_text)
        fconfig.close()

        # Create a temporary out file.
        outfile = tempfile.mktemp('.brl', 'dots_')

        argv = '%s -x db "%s" | %s -f %s > "%s"' % \
            (host_settings.antiword, self.input_file, 
             host_settings.xml2brl, config_fn, outfile)
        os.system(argv)

        # Write braille output to text buffer.
        braille_file = open(outfile)
        self.set_text(braille_file.read())
        braille_file.close()

        os.remove(config_fn)
        os.remove(outfile)
