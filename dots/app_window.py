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

import gtk, glib
import os, tempfile
from config_builder import ConfigBuilder
import host_settings

class AppWindow(object):
    def __init__(self):
        self.main_xml = gtk.Builder()
        self.main_xml.add_from_file (
            os.path.join(host_settings.gtkbuilder_dir, 'app_window.xml'))
        self.window = self.main_xml.get_object('window1')
        self.main_notebook = gtk.Notebook()
        self.main_xml.get_object('main_alignment').add(self.main_notebook)
        self.main_xml.connect_signals(self)
        self.config_builder = ConfigBuilder()

    def _onOpen(self, *args):
        print '_onOpen', args

    def _onImport(self, *args):
        print '_onImport', args

    def run(self):
        self.window.show_all()
        gtk.main()

    def _onQuit(self, window, event):
        gtk.main_quit()

if __name__ == "__main__":
    window = AppWindow()
    window.show_all()
    gtk.main()
