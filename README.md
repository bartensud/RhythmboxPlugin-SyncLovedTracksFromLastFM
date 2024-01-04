# Rhythmbox_SyncLovedLastfmTracks

This is a plugin for Rhythmbox 3. It marks loved last.fm tracks with 5 stars rating in Rhythmbox.

Provided to you by Thomas Bartensud et al.


## PRE-REQUISITES

- Rhythmbox 3.x 
 
Latest version tested with Rhythmbox 3.4.7 under Ubuntu 23.10. More Details under TESTED ENVIRONMENTS below.


## USAGE
Ensure that the plugin is enabled in Rhythmbox menu 'plugins' and configure the Last.fm username in the plugin's configuration dialog:

![Configure last.fm username](https://user-images.githubusercontent.com/156340/43361375-4da23d92-92cd-11e8-9714-387e999bfe37.png)

The menu entry 'Import loved tracks from Last.fm' will be added to the Rhythmbox 'Tools' menu. Activate the menu entry to start the import process:

![Import loved tracks from last.fm](https://user-images.githubusercontent.com/156340/43361260-a6f6b2cc-92ca-11e8-8bf6-24ec24caa250.png)

All the loved songs from last.fm should have in Rhythmbox now a rating of 5 stars (if the song exists in your Rhythmbox Music library)

## INSTALLATION

1. Download latest source code from GitHub and unzip it
2. Execute the installation script:
```sh
sudo ./install.sh
```
Notes:
- Due to some current limitations of Rhythmbox, plugin resource files need to be installed in a certain location so the plugins may be able to access them. Unfortunately this location is outside the user dir ('/usr/share/rhythmbox/plugins/') so the installation script needs superuser privileges to write them.  
- Another reason for requiring superuser privileges is that the plugin uses the Gio.Settings API for storing its settings, which also requires write a schema file to '/usr/share/glib-2.0/schemas/' - which is outside the user dir.

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


## TESTED ENVIRONMENTS

v0.12
- Rhythmbox 3.4.7 under Ubuntu 23.10
- Rhythmbox 3.4.4 under Ubuntu 20.04.6

v0.10
- Rhythmbox 3.4.7 under Ubuntu 23.10
- Rhythmbox 3.4.6 under Ubuntu 22.10
- Rhythmbox 3.4.? under Ubuntu 20.04
- Rhythmbox 3.4.2 under Ubuntu 18.04
- Rhythmbox 3.x under Ubuntu Gnome 16.xx, 17.xx
- Rhythmbox 3.02 under Ubuntu Gnome 14.04

Notes: 
- No incompatible combinations detected (Ubuntu, Rhythmbox) up to now
- Might also work with Rhythmbox 2.98 and 2.99
- No other Linux distros than Ubuntu tested up to now

## DEBUGGING/LOGGING
If you want to see what's going on, start Rhythmbox from command line with filter for the output of this plugin:
```sh
rhythmbox -D syncloved
```


## TODO
- [DONE v0.12] Support paging on retrieving loved tracks from last.fm (currently limited to 1000) 
- [DONE v0.12] Asynchronous processing to avoid blocking of GUI (HTTP request to last.fm, processing response) 
- Add optional scheduler for automatic syncing in background
- Display errors (e.g. wrong username in the config dialog, network problems, etc)
- Display progress/status of synchronization(?)
- Localization


## LICENSE
MIT
