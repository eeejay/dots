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

#import pygtk
#pygtk.require('2.0')
import gtk, glib
import os, tempfile
from config_builder import ConfigBuilder
import host_settings

TABLES_DIR = '/home/eitan/svn/liblouis/tables'

class ImportAssistant(object):
    def __init__(self, main_app=None, xml_file=None):
        self.main_app = main_app
        self.main_xml = gtk.Builder()
        if not xml_file:
            self.main_xml.add_from_file(
                os.path.join(host_settings.gtkbuilder_dir, 'dots_assist.xml'))
        else:
            self.main_xml.add_from_file(xml_file)
        self.window = self.main_xml.get_object('import_assistant')
        self.main_xml.connect_signals(self)
        self.config_builder = ConfigBuilder()

    def run(self):
        intro = self.main_xml.get_object('intro_page')
        self.window.set_page_complete(intro, True)
        #self.window.set_current_page(3)
        self.window.show_all()
        if __name__ == "__main__":
            gtk.main()

    def _onPagePrepare(self, assistant, page):
        self.current_page = page
        
        if page == self.main_xml.get_object('translation_page'):
            self._populateTablesCombo()
        elif page == self.main_xml.get_object('output_page'):
            self.main_xml.get_object('braille_num_pos_combo').set_active(0)
            self.window.set_page_complete(self.current_page, True)
        elif page == self.main_xml.get_object('confirm_page'):
            self._populateSummaryConfig()
            self.window.set_page_complete(self.current_page, True)
        elif page == self.main_xml.get_object('input_file_page'):
            filechooser = self.main_xml.get_object('doc_file_choose_button')
            for mimes, patterns, name in (
                (('application/msword', 'text/html', 'text/xml'),
                 ('*.doc',), 'Documents'),
                (None, ('*',), 'All files')):
                fltr = gtk.FileFilter()
                if mimes:
                    for m in mimes:
                        fltr.add_mime_type(m)
                for p in patterns:
                    fltr.add_pattern(p)
                fltr.set_name(name)
                filechooser.add_filter(fltr)
                

    def _populateSummaryConfig(self):
        text_buffer = self.main_xml.get_object('config_textview').get_buffer()

        self.config_builder['xml']['semanticFiles'] = '*'
        if self.main_xml.get_object('include_nemeth_toggle').get_active():
            self.config_builder['xml']['semanticFiles'] += ',nemeth.sem'

        self.config_builder['xml']['internetAccess'] = 'no'
        if self.main_xml.get_object('internet_access_toggle').get_active():
            self.config_builder['xml']['internetAccess'] = 'yes'

        combo = self.main_xml.get_object('trans_table_sel_combo')
        tablefile = os.path.basename(
            combo.get_model()[combo.get_active_iter()][1])
        self.config_builder['translation']['literaryTextTable'] = tablefile

        self.config_builder['outputFormat']['cellsPerLine'] = \
            self.main_xml.get_object(
            'cells_per_line_spin').get_value_as_int()

        if self.main_xml.get_object('page_output_radio').get_active():
            self.config_builder['outputFormat']['braillePages'] = 'yes'
            self.config_builder['outputFormat']['formatFor'] = 'textDevice'
            self.config_builder['outputFormat']['LinesPerPage'] = \
                self.main_xml.get_object(
                'lines_per_page_spin').get_value_as_int()

            page_num_pos = \
                self.main_xml.get_object('braille_num_pos_combo').get_active()
            if page_num_pos == 0:
                self.config_builder['outputFormat']['braillePageNumberAt'] = \
                    'bottom'
            elif page_num_pos == 1:
                self.config_builder['outputFormat']['braillePageNumberAt'] = \
                    'top'
            elif page_num_pos == 2:
                self.config_builder['outputFormat']['braillePages'] = 'no'

        text_buffer.set_text(str(self.config_builder))

    def _onAssistantApply(self, assistant):
        input_file = \
            self.main_xml.get_object('doc_file_choose_button').get_filename()

        text_buffer = self.main_xml.get_object('config_textview').get_buffer()
        config_text = text_buffer.get_text(text_buffer.get_start_iter(),
                                           text_buffer.get_end_iter())
        
        if self.main_app:
            self.main_app.newProject(input_file, config_text)
        else:
            print config_text
            print '-'*80
            print input_file
            print '='*80

    def _onAssistantApplyOld(self, assistant):
        text_buffer = self.main_xml.get_object('config_textview').get_buffer()
        fd, config_fn = tempfile.mkstemp('.config','dots_')
        fconfig = os.fdopen(fd, 'w')
        fconfig.write(text_buffer.get_text(text_buffer.get_start_iter(),
                                           text_buffer.get_end_iter()))
        fconfig.close()

        input_file = \
            self.main_xml.get_object('doc_file_choose_button').get_filename()

        outfile = tempfile.mktemp('.brl', 'dots_')
        argv = '%s -x db "%s" | %s -f %s > "%s"' % \
            (host_settings.antiword, input_file, 
             host_settings.xml2brl, config_fn, outfile)
        print argv
        os.system(argv)

        braille_buffer = \
            self.main_xml.get_object('braille_textview').get_buffer()
        braille_file = open(outfile)
        braille_buffer.set_text(braille_file.read())
        braille_file.close()

        os.remove(config_fn)
        os.remove(outfile)

    def _onSaveClicked(self, button):
        braille_buffer = \
            self.main_xml.get_object('braille_textview').get_buffer()
        dialog = gtk.FileChooserDialog(
            action=gtk.FILE_CHOOSER_ACTION_SAVE,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                     gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        if (dialog.run() == gtk.RESPONSE_OK):
            fsave = open(dialog.get_filename(), 'w')
            fsave.write(braille_buffer.get_text(
                    braille_buffer.get_start_iter(),
                    braille_buffer.get_end_iter()))
            fsave.close()
        dialog.destroy()

    def _populateTablesCombo(self):
        def _sepatatorFunc(model, itr):
            return model[itr][0] == None
        combo = self.main_xml.get_object('trans_table_sel_combo')
        table_list = filter(lambda x: x.endswith('ctb'),
                            os.listdir(TABLES_DIR))
        table_list.sort()
        model = gtk.ListStore(str, str)
        combo.set_model(model)
        combo.set_row_separator_func(_sepatatorFunc)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)
        model.append(['From file...', None])
        model.append([None, None])
        for table in table_list:
            model.append([table[:-4], os.path.join(TABLES_DIR, table)])

    def _onOutputTypeToggle(self, radio):
        self.main_xml.get_object(
            'page_output_opts_container').set_sensitive(radio.get_active())

    def _onTableChanged(self, combobox):
        model = combobox.get_model()
        itr = combobox.get_active_iter()
        if model[itr][1] == None:
            for suffix in ('button', 'label'):
                self.main_xml.get_object(
                    'trans_table_file_'+suffix).set_sensitive(True)

        self.window.set_page_complete(self.current_page, model[itr][1] != None)

    def _onTableFileSet(self, filechooserbutton):
        model = self.main_xml.get_object('trans_table_sel_combo').get_model()
        model[0][1] = filechooserbutton.get_filename()
        self.window.set_page_complete(self.current_page, True)        

    def _onAssistantCancel(self, assistant, *args):
        assistant.destroy()
        if __name__ == "__main__":
            gtk.main_quit()

    def _onAssistantClose(self, assistant):
        self._onAssistantCancel(assistant)

    def _onInputFileSet(self, filechooserbutton):
        self.window.set_page_complete(self.current_page, True)

if __name__ == "__main__":
    ia = ImportAssistant(xml_file='data/dots_assist.xml')
    ia.run()
