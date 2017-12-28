from gi.repository import Gtk

from ..config import oomoxify_script_path

from .export_config import ExportConfig
from .common import ExportDialog


OPTION_SPOTIFY_PATH = 'spotify_path'
OPTION_FONT_NAME = 'font_name'
OPTION_FONT_OPTIONS = 'font_options'
VALUE_FONT_DEFAULT = 'default'
VALUE_FONT_NORMALIZE = 'normalize'
VALUE_FONT_CUSTOM = 'custom'


class SpotifyExportConfig(ExportConfig):
    name = 'spotify'


class SpotifyExportDialog(ExportDialog):

    theme_path = None
    export_config = None
    timeout = 120

    def do_export(self):
        self.export_config[OPTION_FONT_NAME] = self.font_name_entry.get_text()
        self.export_config[OPTION_SPOTIFY_PATH] = self.spotify_path_entry.get_text()
        self.export_config.save()

        export_args = [
            "bash",
            oomoxify_script_path,
            self.theme_path,
            '--gui',
            '--spotify-apps-path', self.export_config[OPTION_SPOTIFY_PATH],
        ]
        if self.export_config[OPTION_FONT_OPTIONS] == VALUE_FONT_NORMALIZE:
            export_args.append('--font-weight')
        elif self.export_config[OPTION_FONT_OPTIONS] == VALUE_FONT_CUSTOM:
            export_args.append('--font')
            export_args.append(self.export_config[OPTION_FONT_NAME])

        super().do_export(export_args)

    def stop(self):
        self.spinner.stop()
        self.apply_button.destroy()

        self.label.set_text(_("Theme applied successfully"))

        button = Gtk.Button(label=_("_OK"), use_underline=True)
        button.connect("clicked", self._close_button_callback)

        self.under_log_box.add(button)
        self.show_all()

    def on_font_radio_toggled(self, button, value):
        if button.get_active():
            self.export_config[OPTION_FONT_OPTIONS] = value
            self.font_name_entry.set_sensitive(value == VALUE_FONT_CUSTOM)

    def _init_radios(self):
        self.font_radio_default = \
            Gtk.RadioButton.new_with_mnemonic_from_widget(
                None,
                _("Don't change _default font")
            )
        self.font_radio_default.connect(
            "toggled", self.on_font_radio_toggled, VALUE_FONT_DEFAULT
        )
        self.options_box.add(self.font_radio_default)

        self.font_radio_normalize = \
            Gtk.RadioButton.new_with_mnemonic_from_widget(
                self.font_radio_default,
                _("_Normalize font weight")
            )
        self.font_radio_normalize.connect(
            "toggled", self.on_font_radio_toggled, VALUE_FONT_NORMALIZE
        )
        self.options_box.add(self.font_radio_normalize)

        self.font_radio_custom = Gtk.RadioButton.new_with_mnemonic_from_widget(
            self.font_radio_default,
            _("Use custom _font:")
        )
        self.font_radio_custom.connect(
            "toggled", self.on_font_radio_toggled, VALUE_FONT_CUSTOM
        )
        self.options_box.add(self.font_radio_custom)

        self.font_name_entry = Gtk.Entry(text=self.export_config[OPTION_FONT_NAME])
        self.options_box.add(self.font_name_entry)

        self.font_name_entry.set_sensitive(
            self.export_config[OPTION_FONT_OPTIONS] == VALUE_FONT_CUSTOM
        )
        if self.export_config[OPTION_FONT_OPTIONS] == VALUE_FONT_NORMALIZE:
            self.font_radio_normalize.set_active(True)
        if self.export_config[OPTION_FONT_OPTIONS] == VALUE_FONT_CUSTOM:
            self.font_radio_custom.set_active(True)

    def __init__(self, parent, theme_path):
        ExportDialog.__init__(self, parent, headline=_("Spotify options"))
        self.theme_path = theme_path
        self.export_config = SpotifyExportConfig({
            OPTION_SPOTIFY_PATH: "/usr/share/spotify/Apps",
            OPTION_FONT_NAME: "sans-serif",
            OPTION_FONT_OPTIONS: VALUE_FONT_DEFAULT,
        })

        # self.set_default_size(180, 120)
        self.spinner.stop()
        self.label.set_text(_("Please choose the font options:"))

        self._init_radios()

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        spotify_path_label = Gtk.Label(label=_('Spotify _path:'),
                                       use_underline=True)
        self.spotify_path_entry = Gtk.Entry(text=self.export_config[OPTION_SPOTIFY_PATH])
        spotify_path_label.set_mnemonic_widget(self.spotify_path_entry)
        hbox.add(spotify_path_label)
        hbox.add(self.spotify_path_entry)

        self.options_box.add(hbox)
        self.options_box.show()
        self.apply_button.show()

        self.show_all()
        self.scrolled_window.hide()


def export_spotify(window, theme_path):
    return SpotifyExportDialog(window, theme_path)
