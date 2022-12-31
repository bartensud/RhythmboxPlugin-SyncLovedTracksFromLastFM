# Rhythmbox_SyncLovedLastfmTracks


This is a plugin for Rhythmbox 3. It marks loved last.fm tracks with 5 stars rating.

By Thomas Bartensud et al.


## PRE-REQUISITES
- Rhythmbox 3.x (2.98?, 2.99?)


## USAGE
Ensure that the plugin is enabled in Rhythmbox menu 'plugins' and configure the Last.fm user name in the plugin's configuration dialog:

![Configure last.fm username](https://user-images.githubusercontent.com/156340/43361375-4da23d92-92cd-11e8-9714-387e999bfe37.png)

The menu entry 'Import loved tracks from last.fm' will be added to the Rhythmbox 'Tools' menu. Activate the menu entry to start the import process:

![Import loved tracks from last.fm](https://user-images.githubusercontent.com/156340/43361260-a6f6b2cc-92ca-11e8-8bf6-24ec24caa250.png)

All the loved songs from last.fm should have in Rhythmbox now a rating of 5 stars (if existing in your Rhythbmox music library)

## INSTALLATION
Execute the install script in the plugin directory:
```sh
sudo ./install.sh
```

Due to some current limitations of Rhythmbox, plugin resource files need to be installed in a certain location so the plugins may be able to access them. Unfortunately this location is outside the user dir ('/usr/share/rhythmbox/plugins/') so the install script needs superuser privileges to write them.  

Another reason for requiring superuser privileges is that the plugin uses the Gio.Settings API for storing its settings, which also requires write a schema file to '/usr/share/glib-2.0/schemas/' - which is outside the user dir.

## UNINSTALL
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

## NOTES
If you want to debug, start Rhthmbox from command line e.g. to filter for the output of this plugin:
```sh
rhythmbox -D syncloved
```

Tested with:
- Rhythmbox 3.4.6 under Ubuntu 22.10
- Rhythmbox 3.4.? under Ubuntu 20.04
- Rhythmbox 3.4.2 under Ubuntu 18.04
- Rhythmbox 3.x under Ubuntu Gnome 16.xx, 17.xx
- Rhythmbox 3.02 under Ubuntu Gnome 14.04


## TODO
- async processing of the last.fm response (currently the Rhythmbox GUI may hang for a few seconds until sync has finished)
- automatic syncing in background
- indicate import progress/status
- display some kind of summary of the import or errors (if the configured user doesn't exist for example)
- user name validation in the config dialog
- localization


## LICENSE
MIT
