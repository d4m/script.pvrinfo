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
		
		writeEcmInfo(parseEcmInfo())

		if(player.isPlaying() and fileName != player.getPlayingFile()):
			fileName = player.getPlayingFile()
			channelNumber = xbmc.getInfoLabel('VideoPlayer.ChannelNumber')
			writeTpInfo(parseTpInfo(channelNumber))

		xbmc.sleep(100)
	
	writeEcmInfo({"caid": "", "source": "", "hops": "", "time": ""});
	writeTpInfo({'frequency': "", 'position': "", 'position_name': "", 'modulation': "", 'fec': "", 'system': "", 'symbolrate': "", 'polarization': ""})

def parseEcmInfo():

	try:
		ecminfo = open('/tmp/ecm.info').read()

		caid = re.findall('caid: (0x.+)', ecminfo)[0]
		source = re.findall('reader: (.+)', ecminfo)[0]
		hops = re.findall('hops: ([0-9]+)', ecminfo)[0]
		time = re.findall('ecm time: ([0-9.]+)', ecminfo)[0]
	except:
		caid = ""
		source = ""
		hops = ""
		time = ""
		
	return {"caid": caid, "source": source, "hops": hops, "time": time}

def writeEcmInfo(ecminfo):
	xbmcgui.Window(10000).setProperty('PVR_ECM_caid', ecminfo['caid'])
	xbmcgui.Window(10000).setProperty('PVR_ECM_from', ecminfo['source'])
	xbmcgui.Window(10000).setProperty('PVR_ECM_hops', ecminfo['hops'])
	xbmcgui.Window(10000).setProperty('PVR_ECM_time', ecminfo['time'])

def parseTpInfo(channelNumber):

	try:
		tpinfo = channels[int(channelNumber)]
	except KeyError:
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

	return tpinfo

def writeTpInfo(tpinfo):
	xbmcgui.Window(10000).setProperty('PVR_SatellitePos', tpinfo['position'])
	xbmcgui.Window(10000).setProperty('PVR_SatelliteName', tpinfo['position_name'])
	xbmcgui.Window(10000).setProperty('PVR_Modulation', tpinfo['modulation'])
	xbmcgui.Window(10000).setProperty('PVR_Polarization', tpinfo['polarization'])
	xbmcgui.Window(10000).setProperty('PVR_FEC', tpinfo['fec'])
	xbmcgui.Window(10000).setProperty('PVR_Frequency', tpinfo['frequency'])
	xbmcgui.Window(10000).setProperty('PVR_System', tpinfo['system'])
	xbmcgui.Window(10000).setProperty('PVR_Symbolrate', tpinfo['symbolrate'])

def parseChannels():
	
	modulationMap = {
		'M999': 'Auto',
		'M2': 'QPSK',
		'M5': '8PSK',
		'M16': 'QAM16'
	}

	fecMap = {
		'C999': 'Auto',
		'C12': '1/2',
		'C23': '2/3',
		'C34': '3/4',
		'C56': '5/6',
		'C78': '7/8',
		'C89': '8/9',
		'C35': '3/5',
		'C45': '4/5',
		'C910': '9/10',
		'C67': '6/7',
		'C0': 'None'
	}
	
	systemMap = {
		'S0': 'DVB-S',
		'S1': 'DVB-S2'
	}
	
	sources = os.popen("cat /var/lib/vdr/sources.conf | grep '^S'").read().strip()
	sources = re.findall('S([0-9\.]+.)\s+(.+)', sources)
	sources_map = {}

	for source in sources:
		sources_map[source[0]] = source[1]

	channels = os.popen("svdrpsend LSTC | grep '^250'").read().strip()
	parsed_channels = {}
	
	lines = re.findall('250.([0-9]+)[\s]{1}(.+?);(.+?):([0-9]+?):(.+?):S(.+?):([0-9]+?):', channels)
	
	for line in lines:

		number = int(line[0])
		name = line[1]
		provider = line[2]
		frequency = line[3]
		parameter = line[4]
		position = line[5]
		symbolrate = line[6]
		polarization = parameter[0]
		
		modulation = modulationMap[re.findall('M[0-9]', parameter)[0]]
		fec = fecMap[re.findall('C[0-9]+', parameter)[0]]
		system = systemMap[re.findall('S0|S1', parameter)[0]]
		position_name = sources_map[position]

		parsed_channels[number] = {
			'number': number,
			'name': name,
			'provider': provider,
			'frequency': frequency,
			'position': position,
			'position_name': position_name,
			'fec': fec,
			'modulation': modulation,
			'symbolrate': symbolrate,
			'polarization': polarization,
			'system': system
		}

	return parsed_channels

player = Player()
channels = parseChannels()

while(not xbmc.abortRequested):
    xbmc.sleep(100)
