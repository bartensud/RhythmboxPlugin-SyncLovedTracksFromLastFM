import unittest
from net.elektronengehirn.LastFM import *

class  TestLastFM(unittest.TestCase):
    '''
    def setUp(self):
        self.lfm = LastFM()

    def tearDown(self):
        self.lfm.dispose()
        self.lfm = None
    '''
    def testLastFMByUserWithUserBartensud(self):
        lfm = LastFM()
        tracks = lfm.getLovedTracksByUser('bartensud')
        self.assertTrue(tracks is not None)
        #print("Tracks: %s" % tracks)
        self.assertTrue(len(tracks)>0)
        #self.assertTrue(tracks.count>0)
        minExpectedTrack = {'artist': 'Gorillaz', 'name': 'Stylo'}
        minExpectedTrackFound = False
        for track in tracks:
            self.assertTrue(track['artist'] is not None)
            self.assertTrue(track['artist'] != '')
            self.assertTrue(track['name'] is not None)
            self.assertTrue(track['name'] != '')
            if minExpectedTrack['artist']==track['artist'] and minExpectedTrack['name'] == track['name']:
                minExpectedTrackFound = True
        self.assertTrue(minExpectedTrackFound)

    def testLastFMByUserWithUserBartensudTrackLimit1(self):
        expectedTracks = 2
        trackLimit = 1
        lfm = LastFM()
        lfm.trackLimit = trackLimit
        tracks = lfm.getLovedTracksByUser('bartensud')
        self.assertEqual(trackLimit, lfm.trackLimit)
        self.assertEqual(expectedTracks, len(tracks))

    def testLastFMByUrlWithUserRJTrackLimit1Page1(self):
        expectedTrackList = [{'artist': 'The Black Seeds', 'name': "Fire"}]  # pre-req: latest loved track from 4-APR-2016
        user = "rj"  # user from API Doc (has badge 'ALUM' - retired!?)
        trackLimit = 1
        lfm = LastFM()
        lfm.trackLimit = trackLimit
        url = lfm.buildLovedTracksUrl(user, 1)
        tracks = lfm.getLovedTracksByUrl(url)
        self.assertEqual(trackLimit, lfm.trackLimit)
        self.assertEqual(len(expectedTrackList), len(tracks))
        self.assertEqual(expectedTrackList, tracks)
    def testLastFMByUrlWithUserRJTrackLimit1Page2(self):
        expectedTrackList = [{'artist': 'Gramatik', 'name': "Just Jammin'"}]  # pre-req: latest loved track from 4-APR-2016
        user = "rj"  # user from API Doc (has badge 'ALUM' - retired!?)
        trackLimit = 1
        lfm = LastFM()
        lfm.trackLimit = trackLimit
        url = lfm.buildLovedTracksUrl(user, 2)
        tracks = lfm.getLovedTracksByUrl(url)
        self.assertEqual(trackLimit, lfm.trackLimit)
        self.assertEqual(len(expectedTrackList), len(tracks))
        self.assertEqual(expectedTrackList, tracks)

    def testLastFMByUserWithNonexistingUser(self):
        nonExistingUser = 'zonUsersa09jf22dsa4a'
        #nonExistingUser = 'bartensud'
        lfm = LastFM()
        #self.assertr.assertRaises(LastFMError, lfm.getLovedTracksByUser,'zonUsersa09jf22dsa4a')
        self.assertRaises(LastFMError, )
        try:
            lfm.getLovedTracksByUser(nonExistingUser) # todo: handle HTTP Error 400 (Bad request)
            self.fail("This test passed although an exception was expected: 'invalid user supplied' (user: '%s')" %(nonExistingUser))
        except LastFMError as e:
            self.assertEqual(str(e.errorCode), "6", "Error code 6 is expected (Error text should be something like 'User not found', actual value '" + e.errorText + "') ")
        except urllib.error.HTTPError as e:
            print(type(e))    # the exception instance
            print(e.args)     # arguments stored in .args
            print(e)          # __str__ allows args to be printed directly,        except Exception as e:
            raise
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)          # __str__ allows args to be printed directly,        except Exception as e:
            raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise




'''
    def testLastFMWithInvalidApikey(self):
        lfm = LastFM()
        lfm.apiKey = "invalidKey"
        try:
            lfm.getLovedTracksByUser('bartensud') # todo: handle HTTP Error 403 (Forbidden)
            self.fail("This test passed although an exception was expected: 'Invalid API key' (api key used: '%s')" %(lfm.apiKey))
        except LastFMError as e:
            if e.errorCode != "10":
                raise

'''


if __name__ == '__main__':
    unittest.main()

