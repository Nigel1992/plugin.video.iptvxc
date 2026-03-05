#!/usr/bin/python														   #
# -*- coding: utf-8 -*-													   #
############################################################################
#							  /T /I										   #
#							   / |/ | .-~/								   #
#						   T\ Y	 I	|/	/  _							   #
#		  /T			   | \I	 |	I  Y.-~/							   #
#		 I l   /I		T\ |  |	 l	|  T  /								   #
#	  T\ |	\ Y l  /T	| \I  l	  \ `  l Y								   #
# __  | \l	 \l	 \I l __l  l   \   `  _. |								   #
# \ ~-l	 `\	  `\  \	 \ ~\  \   `. .-~	|								   #
#  \   ~-. "-.	`  \  ^._ ^. "-.  /	 \	 |								   #
#.--~-._  ~-  `	 _	~-_.-"-." ._ /._ ." ./								   #
# >--.	~-.	  ._  ~>-"	  "\   7   7   ]								   #
#^.___~"--._	~-{	 .-~ .	`\ Y . /	|								   #
# <__ ~"-.	~		/_/	  \	  \I  Y	  : |								   #
#	^-.__			~(_/   \   >._:	  | l______							   #
#		^--.,___.-~"  /_/	!  `-.~"--l_ /	   ~"-.						   #
#			   (_/ .  ~(   /'	  "~"--,Y	-=b-. _)					   #
#				(_/ .  \  Fire TV Guru/ l	   c"~o \					   #
#				 \ /	`.	  .		.^	 \_.-~"~--.	 )					   #
#				  (_/ .	  `	 /	   /	   !	   )/					   #
#				   / / _.	'.	 .':	  /		   '					   #
#				   ~(_/ .	/	 _	`  .-<_								   #
#					 /_/ . ' .-~" `.  / \  \		  ,z=.				   #
#					 ~( /	'  :   | K	 "-.~-.______//					   #
#					   "-,.	   l   I/ \_	__{--->._(==.				   #
#						//(		\  <	~"~"	 //						   #
#					   /' /\	 \	\	  ,v=.	((						   #
#					 .^. / /\	  "	 }__ //===-	 `						   #
#					/ / ' '	 "-.,__ {---(==-							   #
#				  .^ '		 :	T  ~"	ll								   #
#				 / .  .	 . : | :!		 \								   #
#				(_/	 /	 | | j-"		  ~^							   #
#				  ~-<_(_.^-~"											   #
#																		   #
############################################################################

#############################=IMPORTS=######################################
	#Kodi Specific
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs
import sys
# Select available log level constant to use for notice-level logging
if hasattr(xbmc, 'LOGNOTICE'):
	LOG_NOTICE = xbmc.LOGNOTICE
elif hasattr(xbmc, 'LOGINFO'):
	LOG_NOTICE = xbmc.LOGINFO
elif hasattr(xbmc, 'LOGWARNING'):
	LOG_NOTICE = xbmc.LOGWARNING
elif hasattr(xbmc, 'LOGNONE'):
	LOG_NOTICE = xbmc.LOGNONE
else:
	LOG_NOTICE = 0
# Log that the module has been loaded (helps confirm installed copy)
try:
	xbmc.log(f'IPTVXC: default.py loaded (LOG_NOTICE={LOG_NOTICE})', LOG_NOTICE)
except Exception:
	pass
#Python Specific
import base64,os,re,unicodedata,time,string,sys,urllib.request
import urllib.parse,urllib.error,json,datetime,zipfile,shutil
import xml.etree.ElementTree as ET
from datetime import date
	#Addon Specific
from resources.modules import control,tools,popup,speedtest,epg
##########################=VARIABLES=#######################################
ADDON = xbmcaddon.Addon()
ADDONPATH = ADDON.getAddonInfo("path")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ID = ADDON.getAddonInfo('id')

DIALOG			  = xbmcgui.Dialog()
DP				  = xbmcgui.DialogProgress()
HOME			  = xbmcvfs.translatePath('special://home/')
ADDONS			  = os.path.join(HOME,	   'addons')
USERDATA		  = os.path.join(HOME,	   'userdata')
PLUGIN			  = os.path.join(ADDONS,   ADDON_ID)
PACKAGES		  = os.path.join(ADDONS,   'packages')
ADDONDATA		  = os.path.join(USERDATA, 'addon_data', ADDON_ID)
ADVANCED		  = os.path.join(USERDATA,	'advancedsettings.xml')
advanced_settings = os.path.join(PLUGIN,'resources', 'advanced_settings')
MEDIA			  = os.path.join(ADDONS,  PLUGIN , 'resources', 'media')
KODIV			  = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
M3U_PATH		  = os.path.join(ADDONDATA,  'm3u.m3u')
##########################=ART PATHS=#######################################
icon			  = os.path.join(PLUGIN,  'icon.png')
fanart			  = os.path.join(PLUGIN,  'fanart.jpg')
background		  = os.path.join(MEDIA,	 'background.jpg')
live			  = os.path.join(MEDIA,	 'live.jpg')
catch			  = os.path.join(MEDIA,	 'cu.jpg')
Moviesod		  = os.path.join(MEDIA,	 'movie.jpg')
Tvseries		  = os.path.join(MEDIA,	 'tv.jpg')
iconextras		  = os.path.join(MEDIA,	 'iconextras.png')
iconsettings	  = os.path.join(MEDIA,	 'iconsettings.png')
iconlive		  = os.path.join(MEDIA,	 'iconlive.png')
iconcatchup		  = os.path.join(MEDIA,	 'iconcatchup.png')
iconMoviesod	  = os.path.join(MEDIA,	 'iconmovies.png')
iconTvseries	  = os.path.join(MEDIA,	 'icontvseries.png')
iconsearch		  = os.path.join(MEDIA,	 'iconsearch.png')
iconaccount		  = os.path.join(MEDIA,	 'iconaccount.png')
icontvguide		  = os.path.join(MEDIA,	 'iconguide.png')

#########################=XC VARIABLES=#####################################
dns				  = control.setting('DNS')
username		  = control.setting('Username')
password		  = control.setting('Password')
live_url		  = '{0}/enigma2.php?username={1}&password={2}&type=get_live_categories'.format(dns,username,password)
vod_url			  = '{0}/enigma2.php?username={1}&password={2}&type=get_vod_categories'.format(dns,username,password)
series_url		  = '{0}/enigma2.php?username={1}&password={2}&type=get_series_categories'.format(dns,username,password)
panel_api		  = '{0}/panel_api.php?username={1}&password={2}'.format(dns,username,password)
player_api		  = '{0}/player_api.php?username={1}&password={2}'.format(dns,username,password)
play_url		  = '{0}/live/{1}/{2}/'.format(dns,username,password)
play_live		  = '{0}/{1}/{2}/'.format(dns,username,password)
play_movies		  = '{0}/movie/{1}/{2}/'.format(dns,username,password)
play_series		  = '{0}/series/{1}/{2}/'.format(dns,username,password)
#############################################################################
adult_tags = ['xxx','xXx','XXX','adult','Adult','ADULT','adults','Adults','ADULTS','porn','Porn','PORN']

def buildcleanurl(url):
	url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
	return url

def home():
	# Last Played quick access
	last = tools.load_last_played()
	if last and last.get('url'):
		ts = last.get('timestamp', 0)
		ago = ''
		if ts:
			delta = int(time.time() - ts)
			if delta < 60:
				ago = 'just now'
			elif delta < 3600:
				ago = '%dm ago' % (delta // 60)
			elif delta < 86400:
				ago = '%dh ago' % (delta // 3600)
			else:
				ago = '%dd ago' % (delta // 86400)
		channel_name = last.get('name', 'Last Channel')
		label = '[B][COLOR lime]\u25b6 Last Played: %s[/COLOR][/B]' % channel_name
		if ago:
			label = '[B][COLOR lime]\u25b6 Last Played (%s): %s[/COLOR][/B]' % (ago, channel_name)
		tools.addDir(label, last['url'], 35, last.get('iconimage', icon), background, '')
	tools.addDir('Favorites','url',30,icon,background,'')
	tools.addDir('Recently Watched','url',32,icon,background,'')
	tools.addDir('Account Information','url',6,iconaccount,background,'')
	tools.addDir('Live TV','live',1,iconlive,background,'')
	tools.addDir('Movies/VOD','vod',3,iconMoviesod,background,'')
	tools.addDir('Series','live',18,iconTvseries,background,'')
	tools.addDir('[COLOR FF42A5F5][B]TV Guide[/B][/COLOR]','epg',37,icontvguide,background,'')
	tools.addDir('Catchup TV','url',12,iconcatchup,background,'')
	tools.addDir('Search','url',5,iconsearch,background,'')
	# Trakt.tv integration removed
	tools.addDir('Settings','url',8,iconsettings,background,'')
	tools.addDir('Extras','url',16,iconextras,background,'')

def livecategory():
	data = tools.OPEN_URL_CACHED(live_url, ttl_minutes=tools.CONTENT_CACHE_TTL_TV)
	if not data:
		return
	hidexxx = xbmcaddon.Addon().getSetting('hidexxx')=='true'
	try:
		root = ET.fromstring(data)
	except Exception:
		return
		try:
		    xbmc.log(f'{ADDON_ID}: Parsed params -> url={url} name={name} mode={mode} icon={iconimage} description={description} tmdb_id={tmdb_id}', LOG_NOTICE)
		except Exception:
		    pass

	for ch in root.findall('.//channel'):
		t = ch.findtext('title', default='')
		name = tools.b64(t) if t else ''
		p = ch.findtext('playlist_url', default='')
		url2 = tools.check_protocol(p).replace('<![CDATA[','').replace(']]>','')
		if not hidexxx or (hidexxx and not any(s in name for s in adult_tags)):
			tools.addDir('%s' % name, url2, 2, icon, background if hidexxx else live, '')

def Livelist(url):
	url  = buildcleanurl(url)
	data = tools.OPEN_URL_CACHED(url, ttl_minutes=tools.CONTENT_CACHE_TTL_TV)
	if not data:
		return
	hidexxx = xbmcaddon.Addon().getSetting('hidexxx')=='true'
	try:
		root = ET.fromstring(data)
	except Exception:
		return
	for ch in root.findall('.//channel'):
		t = ch.findtext('title', default='')
		ch_name = re.sub(r'\[.*?min ', '-', tools.b64(t)) if t else ''
		s = ch.findtext('stream_url', default='')
		url1 = tools.check_protocol(s).replace('<![CDATA[','').replace(']]>','')
		thumb = ch.findtext('desc_image', default='')
		if thumb:
			thumb = thumb.replace('<![CDATA[ ','').replace(' ]]>','')
		else:
			thumb = live
		d = ch.findtext('description', default='')
		desc = tools.b64(d) if d else 'No Info Available'
		if not hidexxx or (hidexxx and not any(tag in ch_name for tag in adult_tags)):
			tools.addDir(ch_name, url1, 4, thumb, background, desc)

def series_cats(url):
	raw = tools.OPEN_URL_CACHED(player_api+'&action=get_series_categories', ttl_minutes=tools.CONTENT_CACHE_TTL_SERIES)
	if not raw:
		return
	try:
		vod_cat = json.loads(raw)
	except Exception:
		return
	hidexxx = xbmcaddon.Addon().getSetting('hidexxx')=='true'
	for cat in vod_cat:
		name = cat.get('category_name','')
		cid = cat.get('category_id','')
		if not hidexxx or (hidexxx and not any(s in name for s in adult_tags)):
			tools.addDir(name, player_api+'&action=get_series&category_id='+str(cid), 25, icon, background, '')

def serieslist(url):
	raw = tools.OPEN_URL_CACHED(url, ttl_minutes=tools.CONTENT_CACHE_TTL_SERIES)
	if not raw:
		return
	try:
		ser_cat = json.loads(raw)
	except Exception:
		return
	meta_on = xbmcaddon.Addon().getSetting('meta')=='true'
	for ser in ser_cat:
		if meta_on:
			tools.addDirMeta(ser.get('name',''), player_api+'&action=get_series_info&series_id='+str(ser.get('series_id','')), 19, ser.get('cover',''), (ser.get('backdrop_path') or [''])[0] if ser.get('backdrop_path') else '', ser.get('plot',''), ser.get('releaseDate',''), str(ser.get('cast','')).split(), ser.get('rating_5based',''), ser.get('episode_run_time',''), ser.get('genre',''))
		else:
			tools.addDir(ser.get('name',''), player_api+'&action=get_series_info&series_id='+str(ser.get('series_id','')), 19, ser.get('cover',''), background, '')

def series_seasons(url):
	raw = tools.OPEN_URL_CACHED(url, ttl_minutes=tools.CONTENT_CACHE_TTL_SERIES)
	if not raw:
		return
	try:
		ser_cat = json.loads(raw)
	except Exception:
		return
	info = ser_cat.get('info', {})
	for season in ser_cat.get('episodes', {}):
		tools.addDir('Season - '+str(season), url+'&season_number='+str(season), 20, info.get('cover',''), (info.get('backdrop_path') or [''])[0] if info.get('backdrop_path') else '', '')

def season_list(url):
	raw = tools.OPEN_URL_CACHED(url, ttl_minutes=tools.CONTENT_CACHE_TTL_SERIES)
	if not raw:
		return
	try:
		ser = json.loads(raw)
	except Exception:
		return
	info = ser.get('info', {})
	episodes_map = ser.get('episodes', {})
	from urllib.parse import urlparse, parse_qs
	parsed_url = urlparse(url)
	season_qs = parse_qs(parsed_url.query).get('season_number', [])
	season_number = season_qs[0] if season_qs else None

	episodes = []
	try:
		if isinstance(episodes_map, dict):
			key = season_number
			alt_key = None
			try:
				alt_key = int(season_number) if season_number is not None else None
			except:
				alt_key = None
			if key in episodes_map and episodes_map[key]:
				episodes = episodes_map[key]
			elif alt_key is not None and alt_key in episodes_map and episodes_map[alt_key]:
				episodes = episodes_map[alt_key]
			else:
				for k in episodes_map:
					try:
						for e in episodes_map[k]:
							episodes.append(e)
					except:
						pass
		elif isinstance(episodes_map, list):
			episodes = episodes_map
	except:
		episodes = []

	meta_on = xbmcaddon.Addon().getSetting('meta')=='true'
	for ep in episodes:
		title = ep.get('title') or ep.get('name') or 'Episode'
		ser_info = ep.get('info')
		if isinstance(ser_info, list):
			ser_info = ser_info[0] if ser_info else {}
		if not isinstance(ser_info, dict):
			ser_info = {}
		cover = ser_info.get('movie_image') or ser_info.get('cover') or ''
		plot = ser_info.get('plot') or ''
		releasedate = ser_info.get('releasedate') or ser_info.get('releaseDate') or ''
		duration = ser_info.get('duration') or ''
		container_extension = ep.get('container_extension') or 'mp4'
		play = play_series+str(ep.get('id'))+'.'+container_extension
		if meta_on:
			tools.addDirMeta(title, play, 4, cover, cover, plot, releasedate, str(info.get('cast','')).split(), info.get('rating_5based',''), str(duration), info.get('genre',''))
		else:
			tools.addDir(title, play, 4, cover, cover, '')
def vod(url):
	data = tools.OPEN_URL_CACHED(vod_url if url == 'vod' else buildcleanurl(url), ttl_minutes=tools.CONTENT_CACHE_TTL_MOVIES)
	if not data:
		return
	hidexxx = xbmcaddon.Addon().getSetting('hidexxx')=='true'
	meta_on = xbmcaddon.Addon().getSetting('meta')=='true'
	try:
		root = ET.fromstring(data)
	except Exception:
		return
	for ch in root.findall('.//channel'):
		t = ch.findtext('title', default='')
		name = str(tools.b64(t)).replace('?', '') if t else ''
		playlist = ch.findtext('playlist_url')
		if playlist:
			url1 = tools.check_protocol(playlist.replace('<![CDATA[','').replace(']]>',''))
			if not hidexxx or (hidexxx and not any(s in name for s in adult_tags)):
				tools.addDir(name, url1, 3, icon, background, '')
		else:
			thumb = ch.findtext('desc_image', default='')
			if thumb:
				thumb = thumb.replace('<![CDATA[','').replace(']]>','')
			stream = ch.findtext('stream_url', default='')
			url1 = tools.check_protocol(stream.replace('<![CDATA[','').replace(']]>',''))
			desc_raw = ch.findtext('description', default='')
			desc = tools.b64(desc_raw) if desc_raw else ''
			if meta_on:
				try:
					plot = tools.regex_from_to(desc,'PLOT:','\n')
					cast = tools.regex_from_to(desc,'CAST:','\n')
					ratin= tools.regex_from_to(desc,'RATING:','\n')
					year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
					year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
					runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
					genre= tools.regex_from_to(desc,'GENRE:','\n')
					# Pass full desc (contains TMDB_ID) instead of just plot
					tools.addDirMeta(str(name).replace('[/COLOR][/B].','.[/COLOR][/B]'),url1,4,thumb or background,background,desc,str(year).replace("['","" ).replace("']",""),str(cast).split(),ratin,runt,genre)
				except:
					pass
				xbmcplugin.setContent(int(sys.argv[1]), 'vod')
			else:
				tools.addDir(name,url1,4,thumb or background,background,desc)

def search():
	if mode==3:
		return False
	text = searchdialog()
	if not text:
		return
	q = (text or '').lower()
	hidexxx = xbmcaddon.Addon().getSetting('hidexxx')=='true'
	results = []
	# Search Live TV (available_channels)
	raw = tools.OPEN_URL(panel_api)
	if raw:
		try:
			parse = json.loads(raw)
		except Exception:
			parse = {}
		channels = parse.get('available_channels', {})
		for key in channels:
			a = channels[key]
			name = a.get('name','')
			lower = name.lower()
			if q in lower or (q not in lower and q in name):
				stream_id = str(a.get('stream_id',''))
				thumb = (a.get('stream_icon','') or '').replace(r'\/', '/')
				stream_type = (a.get('stream_type','') or '').replace(r'\/', '/')
				container_extension = a.get('container_extension','mp4')
				if not hidexxx or (hidexxx and not any(s in name for s in adult_tags)):
					if 'movie' in stream_type:
						results.append(('movie', name, play_movies+stream_id+'.'+container_extension, 4, thumb, background, ''))
					if 'live' in stream_type:
						results.append(('live', name, play_live+stream_id, 4, thumb, background, ''))
	# Search VOD (Movies)
	vod_data = tools.OPEN_URL(vod_url)
	if vod_data:
		try:
			root = ET.fromstring(vod_data)
			for ch in root.findall('.//channel'):
				t = ch.findtext('title', default='')
				name = str(tools.b64(t)).replace('?', '') if t else ''
				if q in name.lower() or (q not in name.lower() and q in name):
					playlist = ch.findtext('playlist_url')
					thumb = ch.findtext('desc_image', default='')
					if thumb:
						thumb = thumb.replace('<![CDATA[','').replace(']]>','')
					stream = ch.findtext('stream_url', default='')
					url1 = tools.check_protocol((playlist or stream).replace('<![CDATA[','').replace(']]>',''))
					desc_raw = ch.findtext('description', default='')
					desc = tools.b64(desc_raw) if desc_raw else ''
					if not hidexxx or (hidexxx and not any(s in name for s in adult_tags)):
						results.append(('vod', name, url1, 4, thumb or background, background, desc))
		except Exception:
			pass
	# Search Series
	series_data = tools.OPEN_URL(player_api+'&action=get_series')
	if series_data:
		try:
			ser_cat = json.loads(series_data)
			for ser in ser_cat:
				name = ser.get('name','')
				if q in name.lower() or (q not in name.lower() and q in name):
					series_id = str(ser.get('series_id',''))
					cover = ser.get('cover','')
					results.append(('series', name, player_api+'&action=get_series_info&series_id='+series_id, 19, cover, background, ''))
		except Exception:
			pass
	# Search Catch-up (if available)
	catchup_raw = tools.OPEN_URL(panel_api)
	if catchup_raw:
		try:
			parse = json.loads(catchup_raw)
			channels = parse.get('available_channels', {})
			for key in channels:
				a = channels[key]
				if int(a.get('tv_archive', 0)) == 1:
					name = (a.get('epg_channel_id','') or '').replace(r'\/', '/')
					if q in name.lower() or (q not in name.lower() and q in name):
						thumb = (a.get('stream_icon','') or '').replace(r'\/', '/')
						sid = str(a.get('stream_id',''))
						results.append(('catchup', name, 'url', 13, thumb, background, sid))
		except Exception:
			pass
	# Display all results
	section_labels = {
		'live': '[B][COLOR lime]LIVE[/COLOR][/B] ',
		'movie': '[B][COLOR orange]MOVIE[/COLOR][/B] ',
		'vod': '[B][COLOR yellow]VOD[/COLOR][/B] ',
		'series': '[B][COLOR aqua]SERIES[/COLOR][/B] ',
		'catchup': '[B][COLOR orange]CATCH-UP[/COLOR][/B] '
	}
	for r in results:
		# r = (type, name, url, mode, thumb, background, desc/sid)
		label = section_labels.get(r[0], '') + r[1]
		# Playable items: mode==4, isFolder=False
		if r[0] in ('movie', 'live', 'vod'):
			tools.addDir(label, r[2], 4, r[4], r[5], r[6])
		# Non-playable: keep original mode (series/catchup)
		else:
			tools.addDir(label, r[2], r[3], r[4], r[5], r[6])
######
######

def catchup():
	listcatchup()

def listcatchup():
	raw = tools.OPEN_URL_CACHED(panel_api, ttl_minutes=tools.CONTENT_CACHE_TTL_TV)
	if not raw:
		return
	try:
		parse = json.loads(raw)
	except Exception:
		return
	channels = parse.get('available_channels', {})
	for key in channels:
		a = channels[key]
		if int(a.get('tv_archive', 0)) == 1:
			name = (a.get('epg_channel_id','') or '').replace(r'\/', '/')
			thumb = (a.get('stream_icon','') or '').replace(r'\/', '/')
			sid = str(a.get('stream_id',''))
			if name:
				tools.addDir(name, 'url', 13, thumb, background, sid)

def tvarchive(name,description):
	days = 7
	now = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','')
	date3 = datetime.datetime.now() - datetime.timedelta(days)
	date = str(date3)
	date = str(date).replace('-','').replace(':','').replace(' ','')
	APIv2 = "{0}/player_api.php?username={1}&password={2}&action=get_simple_data_table&stream_id={3}".format(dns,username,password,description)
	link = tools.OPEN_URL(APIv2)
	match = re.compile('"title":"(.+?)".+?"start":"(.+?)","end":"(.+?)","description":"(.+?)"').findall(link)
	for ShowTitle,start,end,DesC in match:
		ShowTitle = tools.b64(ShowTitle)
		DesC = tools.b64(DesC)
		format = '%Y-%m-%d %H:%M:%S'
		try:
			modend = datetime.datetime.strptime(end, format)
			modstart = datetime.datetime.strptime(start, format)
		except Exception:
			modend = datetime.datetime(*(time.strptime(end, format)[0:6]))
			modstart = datetime.datetime(*(time.strptime(start, format)[0:6]))
		StreamDuration = modend - modstart
		modend_ts = time.mktime(modend.timetuple())
		modstart_ts = time.mktime(modstart.timetuple())
		FinalDuration = int(modend_ts-modstart_ts) / 60
		strstart = start
		Realstart = str(strstart).replace('-','').replace(':','').replace(' ','')
		start2 = start[:-3]
		editstart = start2
		start2 = str(start2).replace(' ',' - ')
		start = str(editstart).replace(' ',':')
		Editstart = start[:13] + '-' + start[13:]
		Finalstart = Editstart.replace('-:','-')
		if Realstart > date:
			if Realstart < now:
				catchupURL = "{0}/streaming/timeshift.php?username={1}&password={2}&stream={3}&start=".format(dns,username,password,description)
				ResultURL = catchupURL + str(Finalstart) + "&duration={0}".format(FinalDuration)
				kanalinimi = "[B][COLOR white]{0}[/COLOR][/B] - {1}".format(start2,ShowTitle)
				tools.addDir(kanalinimi,ResultURL,4,icon,background,DesC)

#############################

def tvguide():
		xbmc.executebuiltin('ActivateWindow(TVGuide)')

def _playback_watchdog():
	"""Background thread: dismiss busy dialogs when playback stops.

	When the user presses X on a live IPTV stream, Kodi's FFmpeg demuxer
	can block for 10-30 s trying to close the TCP connection.  During that
	time Kodi shows a 'busydialog' that nothing ever closes, making the UI
	appear frozen.  This watchdog detects the playing→stopped transition
	and aggressively hammers Dialog.Close until the UI is responsive again.
	"""
	import threading
	player = xbmc.Player()
	monitor = xbmc.Monitor()

	# 1. Wait for playback to actually start (max 30 s)
	started = False
	for _ in range(60):
		if monitor.abortRequested():
			return
		if player.isPlaying():
			started = True
			break
		xbmc.sleep(500)

	if not started:
		# Playback never began — clean up and leave
		xbmc.executebuiltin('Dialog.Close(busydialog)')
		xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
		xbmc.log(f'{ADDON_ID}: watchdog – playback never started, exiting', LOG_NOTICE)
		return

	xbmc.log(f'{ADDON_ID}: watchdog – playback started, monitoring', LOG_NOTICE)

	# 2. Wait until the player stops
	while not monitor.abortRequested():
		if not player.isPlaying():
			break
		xbmc.sleep(500)

	xbmc.log(f'{ADDON_ID}: watchdog – playback stopped, dismissing busy dialogs', LOG_NOTICE)

	# 3. Aggressively close busy dialogs for up to 10 s so the UI never
	#    appears stuck while FFmpeg tears down the connection.
	for _ in range(20):
		if monitor.abortRequested():
			return
		xbmc.executebuiltin('Dialog.Close(busydialog)')
		xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
		xbmc.sleep(500)

def _start_playback_watchdog():
	"""Launch the playback watchdog in a daemon thread."""
	import threading
	t = threading.Thread(target=_playback_watchdog,
						 name='IPTVXC-PlayWatchdog', daemon=True)
	t.start()

def stream_video(url):
	url = buildcleanurl(url)
	# Log to history and save as last played
	tools.add_to_history(url, name or '', iconimage or icon, description or '')
	tools.save_last_played(url, name or '', iconimage or icon, description or '')
	xbmc.log(f'{ADDON_ID}: stream_video() resolving URL: {url[:120]}', LOG_NOTICE)
	# Try to get current programme info for the info overlay
	now_title, now_desc = '', ''
	try:
		# Extract stream_id from URL (last path segment)
		sid = url.rstrip('/').split('/')[-1].split('.')[0]
		if sid.isdigit():
			now_title, now_desc = epg.get_now_playing(player_api, sid)
	except Exception:
		pass
	liz = xbmcgui.ListItem(path=str(url))
	liz.setArt({'icon': icon, 'thumb': icon})
	display_title = now_title if now_title else (name or '')
	display_desc = now_desc if now_desc else (description or '')
	liz.setInfo(type='Video', infoLabels={'Title': display_title, 'Plot': display_desc, 'TVShowTitle': name or ''})
	liz.setContentLookup(False)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	xbmc.log(f'{ADDON_ID}: stream_video() resolved OK', LOG_NOTICE)
	# Force-close Kodi's busy dialog in case it lingers while the player
	# buffers or while a remote thumbnail download is blocking the main
	# thread.  A short sleep lets setResolvedUrl propagate first.
	xbmc.sleep(200)
	xbmc.executebuiltin('Dialog.Close(busydialog)')
	xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
	# Start background watchdog (best-effort) and also keep this script
	# alive for a short while.  By spinning in the main thread we can
	# repeatedly close dialogs even if the addon process is terminated
	# by Kodi shortly after resolving the URL.
	_start_playback_watchdog()
	epg.start_epg_updater(player_api, url, name or '')
	player = xbmc.Player()
	# Wait for playback to actually start (up to 10 s), then exit as soon
	# as it stops.  This prevents the invoker staying alive for the full
	# 30-second guard window after the user presses X to stop.
	start = time.time()
	playback_started = False
	while time.time() - start < 30:
		if player.isPlaying():
			playback_started = True
		elif playback_started:
			# Playback started and has now stopped — clean up and exit
			xbmc.executebuiltin('Dialog.Close(busydialog)')
			xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
			break
		elif time.time() - start > 10:
			# Playback never started within 10 s — give up
			break
		# small delay prevents hogging CPU
		xbmc.sleep(500)

def searchdialog():
	search = control.inputDialog(heading='Search '+ADDON_NAME+':')
	if search=="":
		return
	else:
		return search



def settingsmenu():
	if xbmcaddon.Addon().getSetting('meta')=='true':
		META = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		META = '[B][COLOR red]OFF[/COLOR][/B]'
	if xbmcaddon.Addon().getSetting('hidexxx')=='true':
		xxx = '[B][COLOR lime]ON[/COLOR][/B]'
	else:
		xxx = '[B][COLOR red]OFF[/COLOR][/B]'
	tools.addDir('Switch Server','url',34,icon,background,'')
	tools.addDir('Edit Advanced Settings','ADS',10,icon,background,'')
	tools.addDir('META is %s'%META,'META',10,icon,background,META)
	tools.addDir('Hide Adult Content is %s'%xxx,'XXX',10,icon,background,xxx)
	tools.addDir('Log Out','LO',10,icon,background,'')

def addonsettings(url,description):
	url	 = buildcleanurl(url)
	if	 url =="clearcache":
		tools.clear_cache()
	elif url =="AS":
		xbmc.executebuiltin('Addon.OpenSettings(%s)'% ADDON_ID)
	elif url =="ADS":
		dialog = xbmcgui.Dialog().select('Edit Advanced Settings', ['Open AutoConfig','Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','Enable Nvidia Shield AS','Disable AS'])
		if dialog==0:
			advancedsettings('auto')
		elif dialog==1:
			advancedsettings('stick')
			tools.ASln()
		elif dialog==2:
			advancedsettings('firetv')
			tools.ASln()
		elif dialog==3:
			advancedsettings('lessthan')
			tools.ASln()
		elif dialog==4:
			advancedsettings('morethan')
			tools.ASln()
		elif dialog==5:
			advancedsettings('shield')
			tools.ASln()
		elif dialog==6:
			advancedsettings('remove')
			xbmcgui.Dialog().ok(ADDON_NAME, 'Advanced Settings Removed')
	elif url =="ADS2":
		dialog = xbmcgui.Dialog().select('Select Your Device Or Closest To', ['Open AutoConfig','Fire TV Stick ','Fire TV','1GB Ram or Lower','2GB Ram or Higher','Nvidia Shield'])
		if dialog==0:
			advancedsettings('auto')
			tools.ASln()
		elif dialog==1:
			advancedsettings('stick')
			tools.ASln()
		elif dialog==2:
			advancedsettings('firetv')
			tools.ASln()
		elif dialog==3:
			advancedsettings('lessthan')
			tools.ASln()
		elif dialog==4:
			advancedsettings('morethan')
			tools.ASln()
		elif dialog==5:
			advancedsettings('shield')
			tools.ASln()
	elif url =="tv":
		dialog = xbmcgui.Dialog().yesno(ADDON_NAME,'Would You like us to Setup the TV Guide for You?')
		if dialog:
			pvrsetup()
			xbmcgui.Dialog().ok(ADDON_NAME, 'PVR Integration Complete, Restart Kodi For Changes To Take Effect')
	elif url =="Itv":
			xbmc.executebuiltin('InstallAddon(pvr.iptvsimple)')
	elif url =="ST":
		# Only run the speed test, do not prompt for M3U or provider
		speedtest.speedtest()
		return
	elif url =="META":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('meta','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('meta','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url =="XXX":
		if 'ON' in description:
			pas = tools.keypopup('Enter Adult Password:')
			if pas ==control.setting('xxx_pw'):
				xbmcaddon.Addon().setSetting('hidexxx','false')
				xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('hidexxx','true')
			xbmc.executebuiltin('Container.Refresh')		
	elif url =="LO":
		xbmcaddon.Addon().setSetting('DNS','')
		xbmcaddon.Addon().setSetting('Username','')
		xbmcaddon.Addon().setSetting('Password','')
		xbmc.executebuiltin('XBMC.ActivateWindow(Videos,addons://sources/video/)')
		xbmc.executebuiltin('Container.Refresh')
	elif url =="UPDATE":
		if 'ON' in description:
			xbmcaddon.Addon().setSetting('update','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('update','true')
			xbmc.executebuiltin('Container.Refresh')
	elif url == "RefM3U":
		DP.create(ADDON_NAME, "Please Wait")
		tools.gen_m3u(panel_api, M3U_PATH)



def adult_set():
	dialog = DIALOG.yesno(ADDON_NAME,'Would you like to hide the Adult Menu? \nYou can always change this in settings later on.')
	if dialog:
		control.setSetting('xxx_pwset','true')
		pass
	else:
		control.setSetting('xxx_pwset','false')
		pass
	dialog = DIALOG.yesno(ADDON_NAME,'Would you like to Password Protect Adult Content? \nYou can always change this in settings later on.')
	if dialog:
		control.setSetting('xxx_pwset','true')
		adultpw = tools.keypopup('Enter Password')
		control.setSetting('xxx_pw',adultpw)
	else:
		control.setSetting('xxx_pwset','false')
		pass

def advancedsettings(device):
	if device == 'stick':
		file = open(os.path.join(advanced_settings, 'stick.xml'))
	elif device =='auto':
		popup.autoConfigQ()
	elif device == 'firetv':
		file = open(os.path.join(advanced_settings, 'firetv.xml'))
	elif device == 'lessthan':
		file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
	elif device == 'morethan':
		file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
	elif device == 'shield':
		file = open(os.path.join(advanced_settings, 'shield.xml'))
	elif device == 'remove':
		os.remove(ADVANCED)
	try:
		read = file.read()
		f = open(ADVANCED, mode='w+')
		f.write(read)
		f.close()
	except:
		pass

def accountinfo():
	response = tools.OPEN_URL(panel_api)
	parse = json.loads(response)
	expiry	   = parse['user_info']['exp_date']
	if not expiry=="":
		expiry	   = datetime.datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
		expreg	   = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
		for day,month,year in expreg:
			month	  = tools.MonthNumToName(month)
			year	  = re.sub(' -.*?$','',year)
			expiry	  = month+' '+day+' - '+year
	else:
		expiry = 'Unlimited'
	tools.addDir('[B][COLOR white]Username :[/COLOR][/B] '+parse['user_info']['username'],'','',icon,background,'')
	tools.addDir('[B][COLOR white]Password :[/COLOR][/B] '+parse['user_info']['password'],'','',icon,background,'')
	tools.addDir('[B][COLOR white]Expiry Date:[/COLOR][/B] '+expiry,'','',icon,background,'')
	tools.addDir('[B][COLOR white]Account Status :[/COLOR][/B] %s'% parse['user_info']['status'],'','',icon,background,'')
	tools.addDir('[B][COLOR white]Current Connections:[/COLOR][/B] '+ parse['user_info']['active_cons'],'','',icon,background,'')
	tools.addDir('[B][COLOR white]Allowed Connections:[/COLOR][/B] '+ parse['user_info']['max_connections'],'','',icon,background,'')
	tools.addDir('[B][COLOR white]Local IP Address:[/COLOR][/B] '+ tools.getlocalip(),'','',icon,background,'')
	tools.addDir('[B][COLOR white]External IP Address:[/COLOR][/B] '+ tools.getexternalip(),'','',icon,background,'')
	tools.addDir('[B][COLOR white]Kodi Version:[/COLOR][/B] '+str(KODIV),'','',icon,background,'')

def waitasec(time_to_wait,title,text):
	FTGcd = xbmcgui.DialogProgress()
	ret = FTGcd.create(' '+title)
	secs=0
	percent=0
	increment = int(100 / time_to_wait)
	cancelled = False
	while secs < time_to_wait:
		secs += 1
		percent = increment*secs
		secs_left = str((time_to_wait - secs))
		remaining_display = "Still " + str(secs_left) + "seconds left"
		FTGcd.update(percent,text+'\n'+remaining_display)
		xbmc.sleep(1000)
		if (FTGcd.iscanceled()):
			cancelled = True
			break
	if cancelled == True:
		return False
	else:
		FTGcd.close()
		return False

def tester():
	try:
		xbmc.log('[IPTVXC] tester() called', LOG_NOTICE)
		addon = xbmcaddon.Addon()
		dns = addon.getSetting(id='DNS')
		user = addon.getSetting(id='Username')
		pw = addon.getSetting(id='Password')
		if not dns or not user or not pw:
			DIALOG.ok(ADDON_NAME, 'Please enter DNS, Username and Password in Settings')
			return
		auth_url = '{0}/player_api.php?username={1}&password={2}'.format(dns, user, pw)
		response = tools.OPEN_URL(auth_url)
		if not response:
			DIALOG.ok(ADDON_NAME, 'No response from server when testing credentials')
			return
		try:
			parse = json.loads(response)
		except Exception:
			DIALOG.ok(ADDON_NAME, 'Invalid response from server')
			return
		login_data = None
		try:
			login_data = parse.get('user_info', {}).get('auth')
		except:
			login_data = None
		if login_data in (None, 0, '0'):
			DIALOG.ok(ADDON_NAME, 'Test Failed\nIncorrect Login Details')
		else:
			DIALOG.ok(ADDON_NAME, 'Test Successful\nCredentials appear valid')
		return
	except Exception as e:
		DIALOG.ok(ADDON_NAME, 'Test Error\n%s' % str(e))
		return

def pvrsetup():
	correctPVR()
	return

def correctPVR():
	DIALOG.ok(ADDON_NAME, 'This will generate a local M3U playlist and configure PVR IPTV Simple Client with your EPG.\n\nThis may take a minute depending on your channel count.')
	try:
		addon		  = xbmcaddon.Addon(ADDON_ID)
		dns_text	  = addon.getSetting(id='DNS').rstrip('/')
		username_text = addon.getSetting(id='Username')
		password_text = addon.getSetting(id='Password')
		EPGurl		  = dns_text + "/xmltv.php?username=" + username_text + "&password=" + password_text

		# Generate M3U locally (remote URLs are often 100MB+ and time out)
		DP.create(ADDON_NAME, "Generating M3U playlist locally...")
		tools.gen_m3u(panel_api, M3U_PATH)
		DP.close()

		# Enable PVR manager via JSONRPC
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"pvrmanager.enabled","value":true},"id":1}')
		# Enable pvr.iptvsimple, disable pvr.demo
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}')
		xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}')

		FTG = xbmcaddon.Addon('pvr.iptvsimple')
		# Point to local M3U file
		FTG.setSetting(id='m3uPathType', value='0')
		FTG.setSetting(id='m3uPath', value=M3U_PATH)
		# Point to remote EPG (XMLTV is streamed incrementally, so it works fine)
		FTG.setSetting(id='epgPathType', value='1')
		FTG.setSetting(id='epgUrl', value=EPGurl)
		FTG.setSetting(id='epgCache', value='true')
		FTG.setSetting(id='m3uCache', value='true')
		# Re-read the local M3U file every 2 hours so channel changes are picked up
		FTG.setSetting(id='m3uRefreshMode', value='1')
		FTG.setSetting(id='m3uRefreshIntervalMins', value='120')

		xbmc.executebuiltin("Container.Refresh")
		DIALOG.ok(ADDON_NAME, 'PVR Client configured!\n\nM3U: Local file (%s)\nEPG: %s\n\nKodi will now restart for changes to take effect.' % (M3U_PATH, EPGurl))
		os._exit(1)
	except Exception as e:
		DIALOG.ok(ADDON_NAME, 'PVR Setup Error:\n%s\n\nMake sure pvr.iptvsimple is installed first (Extras > Install PVR Guide).' % str(e))

def tvguidesetup():
		dialog = DIALOG.yesno(ADDON_NAME,'Would You like '+ADDON_NAME+' to Setup the TV Guide for You?')
		if dialog:
			pvrsetup()
			DIALOG.ok(ADDON_NAME, 'You are all done! \n Restart Kodi For Changes To Take Effect')

def num2day(num):
	if num =="0":
		day = 'monday'
	elif num=="1":
		day = 'tuesday'
	elif num=="2":
		day = 'wednesday'
	elif num=="3":
		day = 'thursday'
	elif num=="4":
		day = 'friday'
	elif num=="5":
		day = 'saturday'
	elif num=="6":
		day = 'sunday'
	return day
	
def extras():
	tools.addDir('Run a Speed Test','ST',99,icon,background,'')
	tools.addDir('[COLOR red][B]Clear Watch History[/B][/COLOR]','clear_history',33,icon,background,'')
	tools.addDir('[COLOR FF42A5F5]TV Guide[/COLOR]','epg',37,icon,background,'')
	tools.addDir('Clear Cache','clearcache',10,icon,background,'')

def favorites_list():
	favs = tools.load_favorites()
	if not favs:
		tools.addDir('[COLOR grey]No favorites yet. Long-press on any item to add.[/COLOR]','url',-1,icon,background,'')
		return
	for fav in favs:
		tools.addDir(fav.get('name',''), fav.get('url',''), int(fav.get('mode', 4)), fav.get('iconimage', icon), fav.get('fanart', background), fav.get('description',''))

def toggle_favorite():
	fav_mode = params.get('fav_mode', '4')
	if tools.is_favorite(url):
		tools.remove_favorite(url)
		tools.LogNotify(ADDON_NAME, 'Removed from Favorites')
	else:
		tools.add_favorite(url, name or '', fav_mode, iconimage or icon, background, description or '')
		tools.LogNotify(ADDON_NAME, 'Added to Favorites')
	xbmc.executebuiltin('Container.Refresh')

def history_list():
	history = tools.load_history()
	if not history:
		tools.addDir('[COLOR grey]No watch history yet.[/COLOR]','url',-1,icon,background,'')
		return
	tools.addDir('[COLOR red][B]Clear History[/B][/COLOR]','url',33,icon,background,'')
	for item in history:
		ts = item.get('timestamp', 0)
		ago = ''
		if ts:
			delta = int(time.time() - ts)
			if delta < 60:
				ago = 'just now'
			elif delta < 3600:
				ago = '%dm ago' % (delta // 60)
			elif delta < 86400:
				ago = '%dh ago' % (delta // 3600)
			else:
				ago = '%dd ago' % (delta // 86400)
		channel_name = item.get('name', '')
		if ago:
			label = '[COLOR grey]%s[/COLOR]  %s' % (ago, channel_name)
		else:
			label = channel_name
		tools.addDir(label, item.get('url', ''), 35, item.get('iconimage', icon), background, item.get('description', ''))

def manage_profiles():
	profiles = tools.load_profiles()
	choices = ['[B][COLOR lime]Save Current Server as Profile[/COLOR][/B]']
	for p in profiles:
		choices.append(p.get('name', 'Unnamed'))
	sel = DIALOG.select('Server Profiles', choices)
	if sel == -1:
		return
	if sel == 0:
		name_input = control.inputDialog(heading='Profile Name:')
		if name_input:
			tools.save_current_as_profile(name_input)
			tools.LogNotify(ADDON_NAME, 'Profile saved: %s' % name_input)
	else:
		idx = sel - 1
		p = profiles[idx]
		action = DIALOG.select(p.get('name', ''), ['Switch to this server', 'Delete this profile'])
		if action == 0:
			switched = tools.switch_profile(idx)
			if switched:
				tools.LogNotify(ADDON_NAME, 'Switched to: %s' % switched)
				xbmc.executebuiltin('Container.Refresh')
		elif action == 1:
			if DIALOG.yesno(ADDON_NAME, 'Delete profile "%s"?' % p.get('name', '')):
				tools.delete_profile(idx)
				tools.LogNotify(ADDON_NAME, 'Profile deleted')

params=tools.get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None
year=None

try:
	url=urllib.parse.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.parse.unquote_plus(params["name"])
except:
	pass
try:
	iconimage=urllib.parse.unquote_plus(params["iconimage"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	try:
		mode=urllib.parse.unquote_plus(params["mode"])
	except:
		mode=None
try:
	description=urllib.parse.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.parse.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.parse.unquote_plus(params["type"])
except:
	pass
try:
	year=urllib.parse.unquote_plus(params["year"])
except:
	pass
try:
	tmdb_id=urllib.parse.unquote_plus(params["tmdb_id"])
except:
	tmdb_id=''

if mode==None:
	home()
	# Check account expiry on addon launch and optionally start background checks
	try:
		# Non-blocking notification (silently ignore errors)
		try:
			tools.notify_account_expiry()
		except Exception:
			pass
		# Start background worker if enabled in settings
		try:
			if ADDON.getSetting('expiry_notify_background') == 'true':
				tools.start_expiry_background_check()
		except Exception:
			pass
	except Exception:
		pass

elif mode==1:
	livecategory()
	
elif mode==2:
	Livelist(url)
	
elif mode==3:
	vod(url)
	
elif mode==4:
	stream_video(url)
	
elif mode==5:
	search()
	
elif mode==6:
	accountinfo()
	
elif mode==7:
	tvguide()
	
elif mode==8:
	settingsmenu()
	
elif mode==9:
	import xbmcaddon
	import xbmcgui
	import xbmc
	from resources.modules import tools
	xbmc.log('IPTVXC: Test Credentials handler triggered', LOG_NOTICE)
	addon = xbmcaddon.Addon()
	username = addon.getSetting('Username')
	password = addon.getSetting('Password')
	base_url = addon.getSetting('DNS')
	xbmc.log(f'IPTVXC: Settings - DNS={base_url}, Username={username}, Password={password}', LOG_NOTICE)
	if not (username and password and base_url):
		xbmc.log('IPTVXC: Missing credentials', LOG_NOTICE)
		xbmcgui.Dialog().ok('Test Credentials', 'Please enter DNS, Username, and Password in settings.')
	else:
		# Use the robust multi-stage endpoint checker instead of one-shot OPEN_URL
		try:
			res = tools.get_working_endpoint(base_url, username, password, timeout=10, retries=2, treat_512_as_invalid=True, notify=False)
		except Exception as e:
			xbmc.log(f'IPTVXC: get_working_endpoint exception: {e}', LOG_NOTICE)
			xbmcgui.Dialog().ok('Test Credentials', f'Error testing endpoints:\n{e}')
			res = None

		if not res:
			xbmc.log('IPTVXC: No working endpoint found', LOG_NOTICE)
			xbmcgui.Dialog().ok('Test Credentials', 'All endpoint tests failed. Please check DNS, credentials and network connectivity.')
		else:
			# Check for explicit invalid_credentials error
			if res.get('error') == 'invalid_credentials':
				xbmcgui.Dialog().ok('Test Credentials', 'Test Failed\nInvalid DNS or Login Credentials')
			else:
				# Successful endpoint - handle types
				if res.get('type') == 'json':
					data = res.get('data')
					if isinstance(data, dict) and data.get('user_info', {}).get('auth', 0) == 1:
						xbmcgui.Dialog().ok('Test Credentials', 'Test Successful\nCredentials appear valid')
					else:
						xbmcgui.Dialog().ok('Test Credentials', 'Test Failed\nLogin failed. Please check your credentials.')
				elif res.get('type') == 'm3u':
					xbmcgui.Dialog().ok('Test Credentials', 'Test Successful\nM3U playlist reachable (endpoint OK)')
				else:
					xbmcgui.Dialog().ok('Test Credentials', 'Test Failed\nUnknown response from endpoint')
	
elif mode==10:
	if url == 'ST':
		speedtest.speedtest()
	elif url == 'placeholder':
		xbmcgui.Dialog().ok(ADDON_NAME, 'This feature is currently disabled.')
	else:
		addonsettings(url,description)
	
elif mode==12:
	catchup()

elif mode==13:
	tvarchive(name,description)
	
elif mode==14:
	pass
	
elif mode==15:
	pass
	

elif mode==99:
	speedtest.speedtest()

# Setup PVR Guide
elif mode==10 and url == 'tv':
	pvrsetup()

# Install PVR Guide
elif mode==10 and url == 'Itv':
	xbmc.executebuiltin('InstallAddon(pvr.iptvsimple)')
	xbmc.executebuiltin('Container.Refresh')

# Refresh M3U
elif mode==10 and url == 'RefM3U':
	from resources.modules import tools
	DP.create(ADDON_NAME, "Please Wait")
	tools.gen_m3u(panel_api, M3U_PATH)
	xbmcgui.Dialog().ok(ADDON_NAME, 'M3U refreshed!')
	xbmc.executebuiltin('Container.Refresh')

# Clear Cache
elif mode==10 and url == 'clearcache':
	from resources.modules import tools
	tools.clear_cache()
elif mode==10 and url == 'clear_icon_cache':
	from resources.modules import tools
	import os
	cache_file = os.path.join(tools.CACHE_DIR, 'host_probe_cache.json')
	try:
		if os.path.exists(cache_file):
			os.remove(cache_file)
		tools.LogNotify(ADDON_NAME, 'Icon host cache cleared')
	except Exception as e:
		tools.LogNotify(ADDON_NAME, 'Failed to clear cache: %s' % str(e))
elif mode==16:
	extras()
	

elif mode==18:
	series_cats(url)



elif mode==25:
	serieslist(url)
	
elif mode==19:
	series_seasons(url)

elif mode==20:
	season_list(url)

elif mode==30:
	favorites_list()

elif mode==31:
	toggle_favorite()

elif mode==32:
	history_list()

elif mode==33:
	tools.clear_history()
	tools.LogNotify(ADDON_NAME, 'History cleared')
	xbmc.executebuiltin('Container.Refresh')

elif mode==34:
	manage_profiles()

elif mode==37:
	# Built-in TV Guide / EPG
	stream_url, ch_name, ch_icon, now_title, now_desc = epg.open_epg(player_api, play_live, ADDONPATH)
	if stream_url:
		tools.add_to_history(stream_url, ch_name or '', ch_icon or icon, '')
		tools.save_last_played(stream_url, ch_name or '', ch_icon or icon, '')
		display_title = now_title if now_title else (ch_name or '')
		liz = xbmcgui.ListItem(path=str(stream_url))
		liz.setArt({'icon': ch_icon or icon, 'thumb': ch_icon or icon})
		liz.setInfo(type='Video', infoLabels={'Title': display_title, 'Plot': now_desc, 'TVShowTitle': ch_name or ''})
		liz.setContentLookup(False)
		xbmc.Player().play(stream_url, liz)
		epg.start_epg_updater(player_api, stream_url, ch_name or '')

elif mode==35:
	# "Last Played" — just play the channel directly (it's live, show info is stale)
	play_url = buildcleanurl(url)
	tools.add_to_history(play_url, name or '', iconimage or icon, '')
	tools.save_last_played(play_url, name or '', iconimage or icon, '')
	# Fetch current programme info for info overlay
	now_title, now_desc = '', ''
	try:
		sid = play_url.rstrip('/').split('/')[-1].split('.')[0]
		if sid.isdigit():
			now_title, now_desc = epg.get_now_playing(player_api, sid)
	except Exception:
		pass
	display_title = now_title if now_title else (name or '')
	liz = xbmcgui.ListItem(path=str(play_url))
	liz.setArt({'icon': icon, 'thumb': icon})
	liz.setInfo(type='Video', infoLabels={'Title': display_title, 'Plot': now_desc, 'TVShowTitle': name or ''})
	liz.setContentLookup(False)
	xbmc.Player().play(play_url, liz)
	epg.start_epg_updater(player_api, play_url, name or '')




elif mode=='start':
	home()


if mode not in (4, 31, 35, 37):
	try:
		xbmc.log(f'{ADDON_ID}: calling endOfDirectory for mode={mode}', LOG_NOTICE)
	except Exception:
		pass
	xbmcplugin.endOfDirectory(int(sys.argv[1]))