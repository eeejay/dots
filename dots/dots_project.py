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
import ascii_braille
import gtksourceview2, pango
import mimetypes

class DotsProject(gtk.ScrolledWindow):
    def __init__(self, input_file, name):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.view = gtksourceview2.View()
        self.view.set_right_margin(25)
        self.view.set_left_margin(25)
        self.view.set_editable(False)
        self.view.modify_font(pango.FontDescription('Mono'))
        self.add(self.view)
        self.buffer = self.view.get_buffer()
        self.buffer.connect("modified-changed", self._onModified)
        self.braille_buffer = gtksourceview2.Buffer()
        self.input_file = input_file
        self.tab_label = gtk.Label()
        self.set_name(name)
        self.out_file = None
        self.config_text = None

    def set_name(self, name):
        gtk.ScrolledWindow.set_name(self, name)
        self.tab_label.set_text(name)

    def _onModified(self, textbuffer):
        if textbuffer.get_modified():
            self.tab_label.set_text('*'+self.name)
        else:
            self.tab_label.set_text(self.name)

    def transcribeBraille(self, config_text):
        self.config_text = config_text
        self._transcribeBraille()

    def view_ascii(self):
        self.view.set_buffer(self.buffer)

    def view_braille(self):
        self.view.set_buffer(self.braille_buffer)

    def _transcribeBraille(self):
        # Write config file.
        fd, config_fn = tempfile.mkstemp('.config','dots_')
        fconfig = os.fdopen(fd, 'w')
        fconfig.write(self.config_text)
        fconfig.close()

        # Create a temporary out file.
        outfile = tempfile.mktemp('.brl', 'dots_')

        mimetype, ignore = mimetypes.guess_type(self.input_file)
        if mimetype == 'application/msword':
            argv = '%s -x db "%s" | %s -f %s > "%s"' % \
                (host_settings.antiword, self.input_file, 
                 host_settings.xml2brl, config_fn, outfile)
        else:
            argv = '%s -f %s < %s > "%s"' % \
                (host_settings.xml2brl, config_fn, self.input_file, outfile)

        os.system(argv)

        # Write braille output to text buffer.
        braille_file = open(outfile)
        braille_text = braille_file.read()
        self.buffer.set_text(braille_text)
        braille_file.close()

        self.braille_buffer.set_text(
            ''.join([ascii_braille.ascii_to_braille.get(
                        x, '') for x in braille_text]))
        
        os.remove(config_fn)
        os.remove(outfile)
