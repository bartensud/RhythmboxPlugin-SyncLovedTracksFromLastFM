Rhythmbox_SyncLovedLastfmTracks
================================

This is a plugin for Rhythmbox 3. It marks loved last.fm tracks with 5 stars rating.

by Thomas Bartensud et al.


PRE-REQUISITES
--------------
- Rhythmbox 3.x (2.98?, 2.99?)


USAGE
--------------
Ensure that the plugin is enabled in Rhythmbox menu 'plugins' and configure the Last.fm user name in the plugin's configuration dialog.

The menu entry 'Import loved tracks from last.fm' will be added to the Rhythmbox 'Tools' menu. Activate the menu entry to start the import process.




INSTALLATION
--------------
Execute the install script in the plugin directory:
```sh
sudo ./install.sh
```

Due to some current limitations of Rhythmbox, plugin resource files need to be installed in a certain location so the plugins may be able to access them. Unfortunately this location is outside the user dir ('/usr/share/rhythmbox/plugins/') so the install script needs superuser privileges to write them.  

Another reason for requiring superuser privileges is that the plugin uses the Gio.Settings API for storing its settings, which also requires write a schema file to '/usr/share/glib-2.0/schemas/' - which is outside the user dir.

UNINSTALL
---------
To remove the plugin:
```sh
sudo rm -Rf /usr/share/rhythmbox/plugins/lastfm-synclovedtracks
sudo rm -Rf /usr/lib/rhythmbox/plugins/lastfm-synclovedtracks
sudo rm /usr/share/glib-2.0/schemas/org.gnome.rhythmbox.plugins.lastfm-synclovedtracks.gschema.xml && sudo glib-compile-schemas /usr/share/glib-2.0/schemas/
```

To remove the plugin's configuration:
```sh
dconf reset -f "/org/gnome/rhythmbox/plugins/lastfm-synclovedtracks/"
```

NOTES
--------------
If you want to debug, start Rhthmbox from command line e.g. to filter for the output of this plugin
```sh
rhythmbox -D syncloved
```sh

Tested with
- Rhythmbox 3.4.2 under Ubuntu 18.04
- Rhythmbox 3.x under Ubuntu Gnome 16.xx, 17.xx
- Rhythmbox 3.02 under Ubuntu Gnome 14.04


TODO
----
- fix the plugin name in this file and correct the description.
- code cleanup (commented code, unnecessary empty lines, obsolete debug statements)
- get a "real" last.fm api key?
- localization
- indicate import progress/status
- display some kind of summary of the import or errors (if the configured user doesn't exist for example)
- user name validation in the config dialog
- async processing of the last.fm response


DONE
----
- add configuration dialog for last.fm username.


LICENSE
-------
MIT
