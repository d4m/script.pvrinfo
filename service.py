import os, re
import xbmc, xbmcgui

class Player( xbmc.Player ):

	def __init__( self, *args ):
		pass

	def onPlayBackStarted( self ):
		if(re.compile('pvr://').match(self.getPlayingFile())):
			getInfo(self)

def getInfo(player):

	fileName = ""

	while(player.isPlaying()):

		writeEcmInfo(True)

		if(player.isPlaying() and fileName != player.getPlayingFile()):
			fileName = player.getPlayingFile()
			channelNumber = xbmc.getInfoLabel('VideoPlayer.ChannelNumber')
			writeTpInfo(channelNumber)

		xbmc.sleep(100)

	writeEcmInfo(None)
	writeTpInfo(None)

def writeEcmInfo(write):
	
	defaults = {
		'caid': "",
		'source': "",
		'hops': "",
		'time': ""
	}

	ecminfo = parseEcmInfo()
	
	if(write is None or ecminfo is None):
		return defaults
	
	xbmcgui.Window(10000).setProperty('PVR_ECM_caid', ecminfo['caid'])
	xbmcgui.Window(10000).setProperty('PVR_ECM_from', ecminfo['source'])
	xbmcgui.Window(10000).setProperty('PVR_ECM_hops', ecminfo['hops'])
	xbmcgui.Window(10000).setProperty('PVR_ECM_time', ecminfo['time'])

def writeTpInfo(channelNumber):
	
	defaults = {
		'frequency': "",
		'position': "",
		'position_name': "",
		'modulation': "",
		'fec': "",
		'system': "",
		'symbolrate': "",
		'polarization': ""
	}

	tpinfo = getTpInfo(channelNumber)

	if(channelNumber is None or tpinfo is None):
		return defaults
	
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
channels = parseChannels()

while(not xbmc.abortRequested):
	xbmc.sleep(100)
