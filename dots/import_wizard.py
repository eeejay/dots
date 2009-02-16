import pygtk
pygtk.require('2.0')
import gtk, glib
import gtk.glade
import os, tempfile
from config_builder import ConfigBuilder
import host_settings

TABLES_DIR = '/home/eitan/svn/liblouis/tables'

class ImportWizard(object):
    def __init__(self):
        self.main_xml = gtk.glade.XML(
            os.path.join(host_settings.gladedir, 'dots_assist.glade'))
        self.window = self.main_xml.get_widget('import_assistant')
        self.main_xml.signal_autoconnect(self)
        self.config_builder = ConfigBuilder()
    def run(self):
        intro = self.main_xml.get_widget('intro_page')
        self.window.set_page_complete(intro, True)
        #self.window.set_current_page(5)
        self.window.show_all()
        gtk.main()

    def _onPagePrepare(self, assistant, page):
        self.current_page = page
        
        if page == self.main_xml.get_widget('translation_page'):
            self._populateTablesCombo()
        elif page == self.main_xml.get_widget('output_page'):
            self.main_xml.get_widget('braille_num_pos_combo').set_active(0)
            self.window.set_page_complete(self.current_page, True)
        elif page == self.main_xml.get_widget('confirm_page'):
            self._populateSummaryConfig()
            self.window.set_page_complete(self.current_page, True)

    def _populateSummaryConfig(self):
        text_buffer = self.main_xml.get_widget('config_textview').get_buffer()

        self.config_builder['xml']['semanticFiles'] = '*'
        if self.main_xml.get_widget('include_nemeth_toggle').get_active():
            self.config_builder['xml']['semanticFiles'] += ',nemeth.sem'

        self.config_builder['xml']['internetAccess'] = 'no'
        if self.main_xml.get_widget('internet_access_toggle').get_active():
            self.config_builder['xml']['internetAccess'] = 'yes'

        combo = self.main_xml.get_widget('trans_table_sel_combo')
        tablefile = os.path.basename(
            combo.get_model()[combo.get_active_iter()][1])
        self.config_builder['translation']['literaryTextTable'] = tablefile

        self.config_builder['outputFormat']['cellsPerLine'] = \
            self.main_xml.get_widget(
            'cells_per_line_spin').get_value_as_int()

        if self.main_xml.get_widget('page_output_radio').get_active():
            self.config_builder['outputFormat']['braillePages'] = 'yes'
            self.config_builder['outputFormat']['formatFor'] = 'textDevice'
            self.config_builder['outputFormat']['LinesPerPage'] = \
                self.main_xml.get_widget(
                'lines_per_page_spin').get_value_as_int()

            page_num_pos = \
                self.main_xml.get_widget('braille_num_pos_combo').get_active()
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
        text_buffer = self.main_xml.get_widget('config_textview').get_buffer()
        fd, config_fn = tempfile.mkstemp('.config','dots_')
        fconfig = os.fdopen(fd, 'w')
        fconfig.write(text_buffer.get_text(text_buffer.get_start_iter(),
                                           text_buffer.get_end_iter()))
        fconfig.close()

        input_file = \
            self.main_xml.get_widget('doc_file_choose_button').get_filename()

        outfile = tempfile.mktemp('.brl', 'dots_')
        argv = '%s -x db "%s" | %s -f %s > "%s"' % \
            (host_settings.antiword, input_file, 
             host_settings.xml2brl, config_fn, outfile)
        os.system(argv)

        braille_buffer = \
            self.main_xml.get_widget('braille_textview').get_buffer()
        braille_file = open(outfile)
        braille_buffer.set_text(braille_file.read())
        braille_file.close()

        os.remove(config_fn)
        os.remove(outfile)

    def _onSaveClicked(self, button):
        braille_buffer = \
            self.main_xml.get_widget('braille_textview').get_buffer()
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
        combo = self.main_xml.get_widget('trans_table_sel_combo')
        table_list = filter(lambda x: x.endswith('ctb'),
                            os.listdir(TABLES_DIR))
        table_list.sort()
        model = gtk.ListStore(str, str)
        combo.set_model(model)
        combo.set_row_separator_func(_sepatatorFunc)
        model.append(['From file...', None])
        model.append([None, None])
        for table in table_list:
            model.append([table[:-4], os.path.join(TABLES_DIR, table)])

    def _onOutputTypeToggle(self, radio):
        self.main_xml.get_widget(
            'page_output_opts_container').set_sensitive(radio.get_active())

    def _onTableChanged(self, combobox):
        model = combobox.get_model()
        itr = combobox.get_active_iter()
        if model[itr][1] == None:
            for suffix in ('button', 'label'):
                self.main_xml.get_widget(
                    'trans_table_file_'+suffix).set_sensitive(True)

        self.window.set_page_complete(self.current_page, model[itr][1] != None)

    def _onTableFileSet(self, filechooserbutton):
        model = self.main_xml.get_widget('trans_table_sel_combo').get_model()
        model[0][1] = filechooserbutton.get_filename()
        self.window.set_page_complete(self.current_page, True)        

    def _onAssistantCancel(self, assistant, *args):
        assistant.destroy()
        gtk.main_quit()

    def _onAssistantClose(self, assistant):
        self._onAssistantCancel(assistant)

    def _onInputFileSet(self, filechooserbutton):
        self.window.set_page_complete(self.current_page, True)
