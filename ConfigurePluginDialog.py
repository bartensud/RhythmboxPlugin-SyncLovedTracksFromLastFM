
import os.path
from gi.repository import RB, Gtk, Gio, GObject, PeasGtk

import gettext
gettext.install('rhythmbox', RB.locale_dir())

class ConfigurePluginDialog(GObject.Object, PeasGtk.Configurable):
    __gytpe_name = 'PluginConfigureDialog'
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings("org.gnome.rhythmbox.plugins.lastfm-synclovedtracks")

    def do_create_configure_widget(self):
        builder = Gtk.Builder()
        builder.add_from_file(self.find_plugin_file("lastfm-synclovedtracks-prefs.ui"))
        
        ui = builder.get_object('preferences-ui')

        self.lastfm_user_name_field = builder.get_object('lastfm_user_name')
        self.lastfm_user_name_field.set_text(self.settings['lastfm-user-name'])
        self.lastfm_user_name_field.connect("focus-out-event", self.on_lastfm_user_name_field_focus_out)

        self.remove_ratings_checkbox = builder.get_object('remove_ratings')
        self.remove_ratings_checkbox.set_active(self.settings['remove-five-star-ratings'])
        self.remove_ratings_checkbox.connect("toggled", self.on_remove_ratings_toggled)

        return ui

    def on_remove_ratings_toggled(self, widget):
        self.settings['remove-five-star-ratings'] = widget.get_active()

    def on_lastfm_user_name_field_focus_out(self, widget,  event):
        self.settings['lastfm-user-name'] = widget.get_text();

    # shamelessly stolen from rb.py (the "not actually a plugin" plugin):
    # rhythmbox seems to load plugins in alphabetic order so the rb module is imported
    # after our pulgin, which causes our plugin not to compile unless its name is
    # lexicographically smaller than "rb" - which is just stupid
    def find_plugin_file(self, filename):
        info = self.plugin_info
        path = os.path.join(info.get_data_dir(), filename)
        if os.path.exists(path):
            return path
        return RB.file(filename)


