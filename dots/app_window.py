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
from import_assistant import ImportAssistant
from dots_project import DotsProject

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

    def _onOpen(self, action):
        print '_onOpen', action

    def _onImport(self, action):
        ia = ImportAssistant(self)
        ia.run()

    def _getCurrentProject(self):
        return self.main_notebook.get_nth_page(
            self.main_notebook.get_current_page())

    def _onSave(self, action):
        curr_project = self._getCurrentProject()
        if curr_project.out_file is None:
            self._onSaveAs(action)
        else:
            fsave = open(curr_project.out_file, 'w')
            fsave.write(curr_project.buffer.get_text(
                    curr_project.buffer.get_start_iter(),
                    curr_project.buffer.get_end_iter()))
            fsave.close()
            curr_project.buffer.set_modified(False)            

    def _onSaveAs(self, action):
        curr_project = self._getCurrentProject()

        dialog = gtk.FileChooserDialog(
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                     gtk.STOCK_SAVE, gtk.RESPONSE_OK))

        if curr_project.out_file:
            dialog.set_filename(curr_project.out_file)

        if (dialog.run() == gtk.RESPONSE_OK):
            fsave = open(dialog.get_filename(), 'w')
            fsave.write(curr_project.buffer.get_text(
                    curr_project.buffer.get_start_iter(),
                    curr_project.buffer.get_end_iter()))
            fsave.close()
            curr_project.out_file = dialog.get_filename()
            curr_project.set_name(os.path.basename(curr_project.out_file))
            curr_project.buffer.set_modified(False)
            
        dialog.destroy()

    def _getUnsavedNum(self):
        count = 0
        for i in xrange(self.main_notebook.get_n_pages()):
            page = self.main_notebook.get_nth_page(i)
            label_text = self.main_notebook.get_tab_label_text(page)
            if label_text.startswith("Unsaved Document "):
                count += 1
        return count + 1

    def newProject(self, input_file, config_text):
        dotsproj = DotsProject(
            input_file, "Unsaved Document %d" % self._getUnsavedNum())
        dotsproj.transcribeBraille(config_text)
        self.main_notebook.append_page(dotsproj, dotsproj.tab_label)
        dotsproj.show_all()

    def run(self):
        self.window.show_all()
        gtk.main()

    def _onQuit(self, window, event=None):
        gtk.main_quit()

if __name__ == "__main__":
    window = AppWindow()
    window.show_all()
    gtk.main()
