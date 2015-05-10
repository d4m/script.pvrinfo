import re
import xbmc
import xbmcgui

from pvrinfo import parseEcmInfo, parseChannels

class Player( xbmc.Player ):

	def __init__( self, *args ):
		pass

	def onPlayBackStarted( self ):
		if(re.compile('pvr://').match(self.getPlayingFile())):
			fileName = ""

			while(self.isPlaying()):

				writeEcmInfo(True)

				if(self.isPlaying() and fileName != self.getPlayingFile()):
					fileName = self.getPlayingFile()
					channelNumber = xbmc.getInfoLabel('VideoPlayer.ChannelNumber')
					writeTpInfo(channelNumber)

				xbmc.sleep(100)

			writeEcmInfo(None)
			writeTpInfo(None)

def writeEcmInfo(write):

	ecminfo = parseEcmInfo()

	if(write is None or ecminfo is None):
		ecminfo = {
			'caid': "",
			'source': "",
			'hops': "",
			'time': ""
		}

	xbmcgui.Window(10000).setProperty('PVR_ECM_caid', ecminfo['caid'])
	xbmcgui.Window(10000).setProperty('PVR_ECM_from', ecminfo['source'])
	xbmcgui.Window(10000).setProperty('PVR_ECM_hops', ecminfo['hops'])
	xbmcgui.Window(10000).setProperty('PVR_ECM_time', ecminfo['time'])

def writeTpInfo(channelNumber):

	tpinfo = getTpInfo(channelNumber)

	if(channelNumber is None or tpinfo is None):
		tpinfo = {
			'frequency': "",
			'position': "",
			'position_name': "",
			'modulation': "",
			'fec': "",
			'system': "",
			'symbolrate': "",
			'polarization': ""
		}

	xbmcgui.Window(10000).setProperty('PVR_SatellitePos', tpinfo['position'])
	xbmcgui.Window(10000).setProperty('PVR_SatelliteName', tpinfo['position_name'])
	xbmcgui.Window(10000).setProperty('PVR_Modulation', tpinfo['modulation'])
	xbmcgui.Window(10000).setProperty('PVR_Polarization', tpinfo['polarization'])
	xbmcgui.Window(10000).setProperty('PVR_FEC', tpinfo['fec'])
	xbmcgui.Window(10000).setProperty('PVR_Frequency', tpinfo['frequency'])
	xbmcgui.Window(10000).setProperty('PVR_System', tpinfo['system'])
	xbmcgui.Window(10000).setProperty('PVR_Symbolrate', tpinfo['symbolrate'])

def getTpInfo(channelNumber):

	try:
		tpinfo = channels[int(channelNumber)]
	except KeyError:
		tpinfo = None

	return tpinfo

player = Player()
channels = {}

while(not xbmc.abortRequested):

	if(len(channels) == 0):
		channels = parseChannels()

	xbmc.sleep(100)
