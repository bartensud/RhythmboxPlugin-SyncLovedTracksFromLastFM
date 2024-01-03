from gi.repository import GObject, Peas, Gio, GLib
from gi.repository import RB
from gi.repository import Gdk
import rb
from net.elektronengehirn.LastFM import *

from ConfigurePluginDialog import ConfigurePluginDialog

import gettext
gettext.install('rhythmbox', RB.locale_dir())


class LastfmSyncLovedTracksPlugin(GObject.Object, Peas.Activatable):

    __gtype_name = 'LastfmSyncLovedTracksPlugin'
    object = GObject.property(type=GObject.GObject)
    verbose = False
    _lastfm = None
    _page = 0
    _lovedTracks = None
    _lovedTracks_processingSucceeded = None
    _lovedTracks_processingFailed = None
    _importOngoing = 0  # if > 0 then 1 overall import process is ongoing

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings("org.gnome.rhythmbox.plugins.lastfm-synclovedtracks")
        self.settings.connect("changed::lastfm-user-name", self.on_lastfm_user_name_changed)
        self.action = Gio.SimpleAction.new("lastfm-importlovedtracks", None)
            
    def do_activate(self):
        print("activating python plugin: rb-lastfm-synclovedtracks")

        shell = self.object
        db = shell.props.db
        model = RB.RhythmDBQueryModel.new_empty(db)
        #self.source = GObject.new (PythonSource, shell=shell, name=_("Python Source"), query_model=model)
        #self.source.setup()
        #group = RB.DisplayPageGroup.get_by_id ("library")
        #shell.append_display_page(self.source, group)

        self.action.connect('activate', self.execute, shell)
        self.action.set_enabled(self.settings['lastfm-user-name'])
        
        app = shell.props.application
        app.add_action(self.action)

        app.add_plugin_menu_item(
            "tools", "lastfm-importlovedtracks",
            Gio.MenuItem.new(
                label=_("Import loved tracks from Last.fm"),
                detailed_action="app.lastfm-importlovedtracks"
            )
        )

        self._lovedTracks = []
        self._page = 0

    
    def do_deactivate(self):
        print("deactivating python plugin: rb-lastfm-synclovedtracks")
        
        shell = self.object
        app = shell.props.application

        app.remove_plugin_menu_item("tools", "lastfm-importlovedtracks")
        app.remove_action("lastfm-importlovedtracks")

        self._lastfm = None
        self._lovedTracks = None

    def on_lastfm_user_name_changed(self, settings, key):
        self.action.set_enabled(settings['lastfm-user-name'])

    def get_lastfm_instance(self):
        if not self._lastfm:
            self._lastfm = LastFM(verbose=self.verbose)
        return self._lastfm

    def execute(self, action, parameter, shell):
        print("Import of loved tracks from last.fm triggered.")
        if self._importOngoing > 0:
            print("A previously triggered import of loved tracks is still ongoing. Do nothing.")
            return


        if (len(self._lovedTracks) > 0) or (self._page != 0):
            print("WARNING: Synchronization of loved tracks from last.fm started but there seem still not properly finished items. User might have started quickly several times or there's a bug...")
        self._importOngoing = 1
        self._page = 0
        self._lovedTracks = []
        self._lovedTracks_processingSucceeded = []
        self._lovedTracks_processingFailed = []

        if self.settings['lastfm-user-name']:
            if self.settings['remove-five-star-ratings']:
                self.removeRBRatings(5)
            self.import_lovedtracks()


    def import_lovedtracks(self):
        self._importOngoing += 1
        lfm = self.get_lastfm_instance()
        self._page += 1
        url = lfm.buildLovedTracksUrl(self.settings['lastfm-user-name'], self._page)
        loader = rb.Loader()
        print("URL to fetch loved tracks: %s" % (url) )
        loader.get_url(url, self.import_lovedtracks_mycallback)

    def import_lovedtracks_mycallback(self, data_bytes): # data is of type 'bytes'
        self._importOngoing -= 1
        if data_bytes is None:
            print("last.fm query for loved tracks returned nothing")
            #self.search_next()
            return

        if self.verbose:
            try:
                n = min(150, len(data_bytes)) # Ensure n is not greater than the length of the bytes object
                dataStr = data_bytes[:n].decode('utf-8') # Decode the first n entries of the bytes object to a string
                print("last.fm returned data (first %d chars): %s..." % (n, dataStr))
            except:
                print("Unexpected error:", sys.exc_info()[0])


        lfm = self.get_lastfm_instance()
        tracks = lfm.getLovedTracksByUrlData(data_bytes)
        self._lovedTracks.extend(tracks)

        assumedMorePages = len(tracks) == lfm.trackLimit
        if assumedMorePages == True:
            self.import_lovedtracks()
        else:
            # Find and update loved tracks with 5 star rating
            Gdk.threads_add_idle(GLib.PRIORITY_DEFAULT_IDLE, self.__idle_cb, "No data")


    def __idle_cb(self, data):
        finished = self.updateRBRatingsTrackByTrack()
        if not finished:
            return True

        # finish and cleanup
        count_lovedTracks_processingSucceeded = len(self._lovedTracks_processingSucceeded)
        count_lovedTracks_processingFailed = len(self._lovedTracks_processingFailed)
        count_lovedTracks = count_lovedTracks_processingSucceeded + count_lovedTracks_processingFailed
        print("Imported %d of %d loved tracks from last.fm to Rhythmbox DB (marked with 5 stars)" % ( count_lovedTracks_processingSucceeded, count_lovedTracks ))

        if self.verbose:
            print("%d of %d tracks could not be found in Rhythmbox DB: %s" % ( count_lovedTracks_processingFailed, count_lovedTracks, self._lovedTracks_processingFailed ))
        else:
            print("%d of %d tracks could not be found in Rhythmbox DB" % ( count_lovedTracks_processingFailed, count_lovedTracks ))
        self._lovedTracks = []
        self._page = 0

        self._importOngoing -= 1
        if self._importOngoing != 0:
            print("WARNING: Import finished but '_importOngoing' still greater than 0: %d" % (self._importOngoing) )

        return False


    def updateRBRatingsTrackByTrack(self):
        """
        Gets one track from loved tracks and tries to update it in Rhythmbox DB with 5 stars
        :return: True if finished (all loved tracks processed)
        """
        if (len(self._lovedTracks) == 0):
            return True

        track = self._lovedTracks.pop()
        if self.verbose:
            print("%s - %s" % (track['artist'], track['name']))

        if self.updateRBRating(track) == True:
            self._lovedTracks_processingSucceeded.append(track)
        else:
            self._lovedTracks_processingFailed.append(track)

        return (len(self._lovedTracks)==0)


    #def enable_buttons(self, enabled):
    #   self.actionImport.set_sensitive(enabled)


    def removeRBRatings(self, ratingLevel):
        shell = self.object
        db = shell.props.db
        
        #query = db.query_new()
        #db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_RATING, float(ratingLevel)))
        
        
        query = GLib.PtrArray()
        db.query_append_params( query, RB.RhythmDBQueryType.EQUALS, RB.RhythmDBPropType.RATING, float(ratingLevel))
        #db.query_append_params( query, RB.RhythmDBQueryType.EQUALS, RB.RhythmDBPropType.TITLE, 'some song name' )   
        query_model = RB.RhythmDBQueryModel.new_empty(db)
        #self.db.do_full_query_parsed(query_model, query)
        #db.do_full_query_parsed(query_model, (RB.RhythmDBQueryType.EQUALS, RB.RhythmDBPropType.RATING, float(ratingLevel)))
        db.do_full_query_parsed(query_model, query)
        
        
        entries = [row[0] for row in query_model]
        print("Found %d entries in RhythmDB with rating level '%d' for removal:" %(len(entries), ratingLevel))
        for entry in entries:
            #print entry
            #entry_title = db.entry_get_string(entry, RB.RhythmDBPropType.TITLE)
            entry_title = entry.get_string(RB.RhythmDBPropType.TITLE)
            #entry_artist = db.entry_get_string_(entry, RB.RhythmDBPropType.ARTIST)
            entry_artist = entry.get_string(RB.RhythmDBPropType.ARTIST)
            entry_rating = entry.get_double(RB.RhythmDBPropType.RATING)
            if self.verbose:
                print("- Artist: '%s', Name: '%s', Rating: '%d'" %(entry_artist, entry_title, entry_rating))
            #db.set(entry, rhythmdb.PROP_RATING, float(0))
            db.entry_set(entry, RB.RhythmDBPropType.RATING, float(0))
        db.commit()


    

    def updateRBRating(self, track):
        shell = self.object
        db = shell.props.db

        query = GLib.PtrArray()
        db.query_append_params(query, RB.RhythmDBQueryType.FUZZY_MATCH, RB.RhythmDBPropType.ARTIST_FOLDED, track['artist'])  # use str(..) for the query value if byte literals are passed (e.g. b'foo') otherwise segmentation fault
        db.query_append_params(query, RB.RhythmDBQueryType.FUZZY_MATCH, RB.RhythmDBPropType.TITLE_FOLDED, track['name'])
        
        query_model = RB.RhythmDBQueryModel.new_empty(db)
        #print(track['artist'] )
        #print(track['name'] )
        #print("updateRBRating: query executing for '%s' - '%s'..."  %( track['artist'], track['name'] ))
        db.do_full_query_parsed(query_model, query)
        if self.verbose:
            print("updateRBRating: query finished")
        
        entries = [row[0] for row in query_model]
        if self.verbose:
            print("Found %d entries in RhythmDB with search for [Artist: '%s', Name: '%s']:" %(len(entries), track['artist'], track['name']))
        
        #print("Found %d entries in RhythmDB with search for [Artist: '%s', Name: '%s']:" %(len(query_model), track['artist'], track['name']))
        for treerow in query_model: 
            entry, path = list(treerow)
            #print entry
            entry_title = entry.get_string(RB.RhythmDBPropType.TITLE)
            entry_artist = entry.get_string(RB.RhythmDBPropType.ARTIST)
            entry_rating = entry.get_double(RB.RhythmDBPropType.RATING)
            if self.verbose:
                print("- Give loved track 5* rating: Artist: '%s', Name: '%s', Rating: '%d'" %(entry_artist, entry_title, entry_rating))
            db.entry_set(entry, RB.RhythmDBPropType.RATING, float(5))
            db.commit()
            return True
        return False        
        

