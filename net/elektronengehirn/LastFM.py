
__author__ = "Thomas Bartensud"
__date__ = "$Jul 17, 2010 7:34:02 PM$"

#from xml.dom.minidom import parse
import xml.dom.minidom
import urllib.request
import urllib.parse
import urllib.error




class LastFM:
    """A class for providing a user's loved tracks at last.fm"""
    apiKey = "c0b0c4e03c75ff9c09a87aecf3d7a731"  # for last.fm app: LovedSongsImporter
    trackLimit = 1000 # supported values by API: 1-1000
    __urlTemplate = "http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=%s&api_key=%s&limit=%d&page=%d"

    def __init__(self, apiKey=None):
        if apiKey is not None:
            self.apiKey = apiKey

    def buildLovedTracksUrl(self, user, page=1):
        """
        Builds API URL for accessing loved tracks
        :param user: last.fm username
        :param page: starts with 1. last.fm has a limit of 1000 tracks per API call.
        :return: URL for accessing loved tracks
        """
        return self.__urlTemplate % (user, self.apiKey, self.trackLimit, page)

    def getLovedTracksByUser(self, user):
        """
        Returns loved tracks by last.fm user
        Note: paging is automatically done in case there are more loved tracks than the track limit per API call
        :param user: last.fm username
        :return: List of loved tracks (with properties 'artist' and 'name' per track)
        """
        tracks_all = []
        page = 0
        more_pages = True
        while more_pages == True:
            page += 1
            url = self.buildLovedTracksUrl(user, page)
            tracks = self.getLovedTracksByUrl(url)
            tracks_all.extend(tracks)
            more_pages = len(tracks) == self.trackLimit

        return tracks_all

    def getLovedTracksByUrl(self, url):
        """
        Returns loved tracks via last.fm API call by URL.
        Note: for paging several URLs must be called with according parameter 'page'!
        :param url: URL for last.fm API
        :return: List of loved tracks (with properties 'artist' and 'name' per track)
        """
        print("HTTP GET %s" % url)
        req = urllib.request.Request(url)
        try:
            resp = urllib.request.urlopen(req)
            dom = xml.dom.minidom.parse(resp)
        except urllib.error.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            print('Reason: ', e.reason)
            try:
                errContentBytes = e.read()
                errContentStr = errContentBytes.decode("utf-8")
                dom = xml.dom.minidom.parseString(errContentStr)
            except:
                raise e


        except urllib.error.URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            raise
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,        except Exception as e:
            raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        else:
            # everything is fine
            pass

        return self.__getLovedTracksByDOM(dom)

    def getLovedTracksByUrlData(self, urlData):
        try:
            dom = xml.dom.minidom.parseString(urlData)
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,        except Exception as e:
            raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        else:
            # everything is fine
            pass

        return self.__getLovedTracksByDOM(dom)

    def __getLovedTracksByDOM(self, dom):
        lovedTracks = []

        # check status
        # ok: <lfm status="ok">
        # failed: <lfm status="failed"><error code="6">User not found</error></lfm>
        if 'failed' == dom.firstChild.attributes['status'].value:
            errorEl = dom.getElementsByTagName("error")[0]
            errorCode = errorEl.attributes['code'].value
            errorText = self.__getText(errorEl.childNodes)
            raise LastFMError(errorCode, errorText)

        tracks = dom.getElementsByTagName("track")
        for track in tracks:
            artistEl = track.getElementsByTagName("artist")[0].getElementsByTagName("name")[0]
            artist = self.__getText(artistEl.childNodes)  # .encode("utf-8")
            nameEl = track.getElementsByTagName("name")[0]
            name = self.__getText(nameEl.childNodes)  # .encode("utf-8")
            lovedTracks.append({'artist': artist, 'name': name})
            #print("%s: %s" % (artist, name))

        print('loved tracks at last.fm: %s' % lovedTracks)
        return lovedTracks

    def __getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)


class LastFMError(Exception):
    def __init__(self, errorCode, errorText):
        self.errorCode = errorCode
        self.errorText = errorText

    def __str__(self):
        return "LastFM Error (%s): %s" % (self.errorCode, self.errorText)



if __name__ == "__main__":
    print("Demo")
    lfm = LastFM()
    tracks = lfm.getLovedTracksByUser('bartensud')
    for track in tracks:
        print(track)

