import os, re

def parseEcmInfo():

	try:
		tmp_ecminfo = open('/tmp/ecm.info').read()

		ecminfo = {
			'caid': re.findall('caid: (0x.+)', tmp_ecminfo)[0],
			'source': re.findall('reader: (.+)', tmp_ecminfo)[0],
			'hops': re.findall('hops: ([0-9]+)', tmp_ecminfo)[0],
			'time': re.findall('ecm time: ([0-9.]+)', tmp_ecminfo)[0]
		}
	except:
		ecminfo = None

	return ecminfo
	
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
	sourcesMap = {}

	for source in sources:
		sourcesMap[source[0]] = source[1]

	dvbtSourcesMap = {
		538000: 'Sucha Gora MUX 3 k.52',
		562000: 'Sucha Gora MUX 2 k.32',
		722000: 'Sucha Gora MUX 1 k.29'
	}

	channels = os.popen("svdrpsend LSTC | grep '^250'").read().strip()
	parsed_channels = {}

	lines = re.findall('250.([0-9]+)[\s]{1}(.+?);(.+?):([0-9]+?):(.+?):(T|S(.+?)):([0-9]+?):', channels)

	for line in lines:
		try:
			number = int(line[0])
			name = line[1]
			provider = line[2]
			frequency = line[3]
			parameter = line[4]
			symbolrate = line[7]

			fec = fecMap[re.findall('C[0-9]+', parameter)[0]]
			
			if(line[5] == 'T'):
				position = line[5]
			
				system = 'DVB-T'
				position_name = dvbtSourcesMap[int(str(frequency)[:6])]
				modulation = ""
				polarization = ""
			else:
				position = line[6]
			
				system = systemMap[re.findall('S0|S1', parameter)[0]]
				position_name = sourcesMap[position]
				modulation = modulationMap[re.findall('M[0-9]', parameter)[0]]
				polarization = parameter[0]

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
		except:
			pass

	return parsed_channels