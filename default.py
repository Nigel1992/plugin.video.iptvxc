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
icon = os.path.join(PLUGIN, 'icon.png')
# fallback for Extras if no specific icon is provided
iconextras = os.path.join(MEDIA, 'icon_EXTRAS.png')
fanart = os.path.join(PLUGIN, 'fanart.jpg')
background = os.path.join(MEDIA, 'background.jpg')
live = os.path.join(MEDIA, 'live.jpg')
catch = os.path.join(MEDIA, 'cu.jpg')
Moviesod = os.path.join(MEDIA, 'movie.jpg')
Tvseries = os.path.join(MEDIA, 'tv.jpg')
# new menu icons placed in resources/media (files starting with icon_)
iconfavorites = os.path.join(MEDIA, 'icon_FAVORITES.png')
iconrecent = os.path.join(MEDIA, 'icon_RECENTLY_WATCHED.png')
icon_lastplayed = os.path.join(MEDIA, 'icon_LAST_PLAYED.png')
iconaccount = os.path.join(MEDIA, 'icon_ACCOUNT_INFO.png')
iconlive = os.path.join(MEDIA, 'icon_LIVE_TV.png')
iconMoviesod = os.path.join(MEDIA, 'icon_MOVIES_VOD.png')
iconTvseries = os.path.join(MEDIA, 'icon_SERIES.png')
icontvguide = os.path.join(MEDIA, 'icon_TV_GUIDE.png')
iconcatchup = os.path.join(MEDIA, 'icon_CATCHUP_TV.png')
iconsearch = os.path.join(MEDIA, 'icon_SEARCH.png')
iconsettings = os.path.join(MEDIA, 'icon_SETTINGS.png')

#########################=XC VARIABLES=#####################################
dns				  = control.setting('DNS')
username		  = control.setting('Username')
password		  = control.setting('Password')
credential_query  = urllib.parse.urlencode({'username': username, 'password': password})
path_username	  = urllib.parse.quote(username, safe='')
path_password	  = urllib.parse.quote(password, safe='')
live_url		  = '{0}/enigma2.php?{1}&type=get_live_categories'.format(dns,credential_query)
vod_url			  = '{0}/enigma2.php?{1}&type=get_vod_categories'.format(dns,credential_query)
series_url		  = '{0}/enigma2.php?{1}&type=get_series_categories'.format(dns,credential_query)
panel_api		  = '{0}/panel_api.php?{1}'.format(dns,credential_query)
player_api		  = '{0}/player_api.php?{1}'.format(dns,credential_query)
play_url		  = '{0}/live/{1}/{2}/'.format(dns,path_username,path_password)
play_live		  = '{0}/{1}/{2}/'.format(dns,path_username,path_password)
play_movies		  = '{0}/movie/{1}/{2}/'.format(dns,path_username,path_password)
play_series		  = '{0}/series/{1}/{2}/'.format(dns,path_username,path_password)
#############################################################################
adult_tags = ['xxx','xXx','XXX','adult','Adult','ADULT','adults','Adults','ADULTS','porn','Porn','PORN']

def buildcleanurl(url):
	# Percent-encoded credentials work in both URL paths and query values and
	# avoid broken playback for accounts containing spaces or reserved signs.
	url = str(url).replace('USERNAME', path_username).replace('PASSWORD', path_password)
	return url

def _clean_playback_name(value):
	"""Return the real title behind Last Played/history display labels."""
	text = str(value or '')
	# Remove Kodi formatting before stripping generated prefixes.  Older
	# versions saved the fully formatted Last Played label as the title,
	# which caused the prefix to be nested again after every replay.
	text = re.sub(r'\[/?(?:B|I|COLOR)(?:\s+[^\]]+)?\]', '', text, flags=re.IGNORECASE)
	last_played_prefix = re.compile(
		r'^\s*(?:\u25b6\s*)?Last Played(?:\s*\([^)]*\))?\s*:\s*',
		re.IGNORECASE,
	)
	history_prefix = re.compile(
		r'^\s*(?:just now|\d+[mhd]\s+ago)\s{2,}',
		re.IGNORECASE,
	)
	while True:
		cleaned = last_played_prefix.sub('', text)
		cleaned = history_prefix.sub('', cleaned)
		if cleaned == text:
			break
		text = cleaned
	return text.strip() or 'Last Channel'

SEARCH_STATE_FILE = os.path.join(ADDONDATA, 'active_search.json')

def _load_search_state():
	try:
		with open(SEARCH_STATE_FILE, 'r', encoding='utf-8') as state_file:
			state = json.load(state_file)
		if isinstance(state, dict) and state.get('active'):
			return state
	except Exception:
		pass
	return {}

def _save_search_state(scope, query_text):
	try:
		tools._atomic_write_json(SEARCH_STATE_FILE, {
			'active': True, 'scope': str(scope),
			'query': str(query_text), 'timestamp': time.time(),
		})
	except Exception as exc:
		xbmc.log('%s: unable to save active search: %s' % (
			ADDON_ID, tools.redact_sensitive(exc)), LOG_NOTICE)

def _clear_search_state():
	try:
		if os.path.exists(SEARCH_STATE_FILE):
			os.remove(SEARCH_STATE_FILE)
	except Exception:
		pass

def home():
	# Reaching the main menu ends the prior search session.  Until then its
	# scope/query remain available so Kodi can rebuild results after playback.
	_clear_search_state()
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
			channel_name = _clean_playback_name(last.get('name', 'Last Channel'))
			label = '[B][COLOR lime]\u25b6 Last Played: %s[/COLOR][/B]' % channel_name
			if ago:
				label = '[B][COLOR lime]\u25b6 Last Played (%s): %s[/COLOR][/B]' % (ago, channel_name)
			# Always use the provided local icon for Last Played so it displays
			tools.addDir(label, last['url'], 35, icon_lastplayed, background, '')
	tools.addDir('Favorites','url',30,iconfavorites,background,'')
	tools.addDir('Recently Watched','url',32,iconrecent,background,'')
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

def _catalog_items(endpoint, ttl_minutes):
	"""Fetch an Xtream catalog and normalize list/dictionary response shapes."""
	raw = tools.OPEN_URL_CACHED(endpoint, ttl_minutes=ttl_minutes)
	if not raw:
		return []
	try:
		data = json.loads(raw)
		if isinstance(data, list):
			return [item for item in data if isinstance(item, dict)]
		if isinstance(data, dict):
			for key in ('available_channels', 'channels', 'data', 'results'):
				items = data.get(key)
				if isinstance(items, list):
					return [item for item in items if isinstance(item, dict)]
				if isinstance(items, dict):
					return [item for item in items.values() if isinstance(item, dict)]
			return [item for item in data.values() if isinstance(item, dict)]
	except Exception as exc:
		xbmc.log('%s: search catalog parse failed for %s: %s' % (
			ADDON_ID, tools.redact_sensitive(endpoint), tools.redact_sensitive(exc)), LOG_NOTICE)
	return []

def search():
	# Search the actual Xtream catalogs.  The former implementation mixed a
	# legacy panel dictionary with a VOD category feed and crashed when a
	# provider returned the standard list-shaped response.
	valid_scopes = ('live', 'vod', 'series', 'all')
	stored_scope = urllib.parse.unquote_plus(str(params.get('scope', ''))).lower()
	stored_query = urllib.parse.unquote_plus(str(params.get('query', ''))).strip()
	if stored_scope in valid_scopes and stored_query:
		# A parameterized route can be recreated by Kodi after playback, so the
		# user returns to these results instead of seeing the search dialogs again.
		scope = stored_scope
		text = stored_query
	else:
		active_search = _load_search_state()
		active_scope = str(active_search.get('scope') or '').lower()
		active_query = str(active_search.get('query') or '').strip()
		if active_scope in valid_scopes and active_query:
			scope = active_scope
			text = active_query
		else:
			scope_items = ['Live TV & Catchup', 'Movies/VOD', 'Series', 'All sections']
			choice = DIALOG.select('Search in', scope_items)
			if choice < 0:
				return
			scope = valid_scopes[choice]
			text = searchdialog()
			if not text:
				return
	_save_search_state(scope, text)
	query = str(text).strip().casefold()
	try:
		xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Search results: %s' % str(text))
	except Exception:
		pass
	hide_adult = xbmcaddon.Addon().getSetting('hidexxx') == 'true'
	results = []
	legacy_items = None
	search_cancelled = False
	active_sections = [name for name in ('live', 'vod', 'series')
		if scope in (name, 'all')]
	section_names = {'live': 'Live TV & Catch-up', 'vod': 'Movies/VOD', 'series': 'Series'}
	search_progress = xbmcgui.DialogProgress()
	progress_open = False
	try:
		search_progress.create(ADDON_NAME, 'Preparing search for "%s"...' % str(text))
		progress_open = True
	except Exception:
		pass

	def update_section(section, fraction, action):
		"""Update a section's share of the overall 0-90% search progress."""
		if not progress_open:
			return False
		try:
			index = active_sections.index(section)
			span = 86.0 / max(1, len(active_sections))
			percent = 3.0 + (index * span) + (max(0.0, min(1.0, fraction)) * span)
			search_progress.update(int(percent), '%s %s...\nQuery: %s' % (
				action, section_names[section], str(text)))
			return bool(search_progress.iscanceled())
		except Exception:
			return False

	def close_search_progress():
		if progress_open:
			try:
				search_progress.close()
			except Exception:
				pass

	def get_legacy_items():
		"""Load legacy panel channels only when a standard catalog is empty."""
		nonlocal legacy_items
		if legacy_items is None:
			legacy_items = _catalog_items(panel_api, tools.CONTENT_CACHE_TTL_TV)
		return legacy_items

	def legacy_streams(kind):
		nonlocal search_cancelled
		items = []
		catalog = get_legacy_items()
		total = max(1, len(catalog))
		for index, item in enumerate(catalog):
			if index % 500 == 0 and update_section(
				kind, 0.10 + (0.15 * index / total), 'Preparing'):
				search_cancelled = True
				break
			stream_type = str(item.get('stream_type') or '').casefold()
			if kind == 'live' and 'live' in stream_type:
				items.append(item)
			elif kind == 'vod' and ('movie' in stream_type or 'vod' in stream_type):
				items.append(item)
		return items

	def matches(item_name):
		name_text = str(item_name or '')
		if query not in name_text.casefold():
			return False
		if hide_adult and any(tag.casefold() in name_text.casefold() for tag in adult_tags):
			return False
		return True

	if scope in ('live', 'all'):
		if update_section('live', 0.0, 'Loading'):
			close_search_progress()
			return
		live_items = _catalog_items(
			player_api + '&action=get_live_streams', tools.CONTENT_CACHE_TTL_TV)
		if not live_items:
			# Several older XC panels expose streams only through panel_api.php.
			live_items = legacy_streams('live')
		if search_cancelled:
			close_search_progress()
			return
		live_total = max(1, len(live_items))
		for index, item in enumerate(live_items):
			if index % 250 == 0 and update_section(
				'live', 0.25 + (0.75 * index / live_total), 'Searching'):
				search_cancelled = True
				break
			channel_name = str(item.get('name') or item.get('epg_channel_id') or '')
			if not matches(channel_name):
				continue
			stream_id = str(item.get('stream_id') or '')
			if not stream_id:
				continue
			thumb = str(item.get('stream_icon') or '').replace(r'\/', '/')
			direct_source = str(item.get('direct_source') or '')
			stream_url = direct_source if direct_source.startswith(('http://', 'https://')) else play_url + stream_id + '.ts'
			results.append(('live', channel_name, stream_url, 4, thumb, background, ''))
			try:
				has_archive = int(item.get('tv_archive') or 0) == 1
			except (TypeError, ValueError):
				has_archive = False
			if has_archive:
				results.append(('catchup', channel_name, 'url', 13, thumb, background, stream_id))
		if search_cancelled:
			close_search_progress()
			return
		update_section('live', 1.0, 'Finished')

	if scope in ('vod', 'all'):
		if update_section('vod', 0.0, 'Loading'):
			close_search_progress()
			return
		vod_endpoint = player_api + '&action=get_vod_streams'
		vod_items = _catalog_items(vod_endpoint, tools.CONTENT_CACHE_TTL_MOVIES)
		if not vod_items:
			# Some large XC panels intentionally return [] unless category_id is
			# supplied.  Category 0 is their complete Movies/VOD catalog.
			update_section('vod', 0.06, 'Loading full catalog for')
			vod_items = _catalog_items(
				vod_endpoint + '&category_id=0', tools.CONTENT_CACHE_TTL_MOVIES)
		if not vod_items:
			# A smaller group of legacy panels accepts the action only on
			# panel_api.php.  Keep only its movie records because it may also
			# include Live TV entries in the same response.
			panel_vod_items = _catalog_items(
				panel_api + '&action=get_vod_streams', tools.CONTENT_CACHE_TTL_MOVIES)
			vod_items = [item for item in panel_vod_items
				if str(item.get('stream_type') or '').casefold() in ('movie', 'vod')]
		if not vod_items:
			vod_items = legacy_streams('vod')
		if search_cancelled:
			close_search_progress()
			return
		vod_total = max(1, len(vod_items))
		for index, item in enumerate(vod_items):
			if index % 250 == 0 and update_section(
				'vod', 0.25 + (0.75 * index / vod_total), 'Searching'):
				search_cancelled = True
				break
			movie_name = str(item.get('name') or '')
			if not matches(movie_name):
				continue
			stream_id = str(item.get('stream_id') or '')
			if not stream_id:
				continue
			extension = str(item.get('container_extension') or 'mp4').lstrip('.')
			thumb = str(item.get('stream_icon') or '').replace(r'\/', '/')
			direct_source = str(item.get('direct_source') or '')
			stream_url = direct_source if direct_source.startswith(('http://', 'https://')) else play_movies + stream_id + '.' + extension
			description_text = str(item.get('plot') or item.get('description') or '')
			results.append(('vod', movie_name, stream_url, 4, thumb, background, description_text))
		if search_cancelled:
			close_search_progress()
			return
		update_section('vod', 1.0, 'Finished')

	if scope in ('series', 'all'):
		if update_section('series', 0.0, 'Loading'):
			close_search_progress()
			return
		series_items = _catalog_items(
			player_api + '&action=get_series', tools.CONTENT_CACHE_TTL_SERIES)
		series_total = max(1, len(series_items))
		for index, item in enumerate(series_items):
			if index % 250 == 0 and update_section(
				'series', 0.15 + (0.85 * index / series_total), 'Searching'):
				search_cancelled = True
				break
			series_name = str(item.get('name') or '')
			if not matches(series_name):
				continue
			series_id = str(item.get('series_id') or '')
			if not series_id:
				continue
			cover = str(item.get('cover') or item.get('stream_icon') or '')
			results.append(('series', series_name,
				player_api + '&action=get_series_info&series_id=' + series_id,
				19, cover, background, str(item.get('plot') or '')))
		if search_cancelled:
			close_search_progress()
			return
		update_section('series', 1.0, 'Finished')

	# Display all results
	section_labels = {
		'live': '[B][COLOR lime]LIVE[/COLOR][/B] ',
		'movie': '[B][COLOR orange]MOVIE[/COLOR][/B] ',
		'vod': '[B][COLOR yellow]VOD[/COLOR][/B] ',
		'series': '[B][COLOR aqua]SERIES[/COLOR][/B] ',
		'catchup': '[B][COLOR orange]CATCH-UP[/COLOR][/B] '
	}
	# Log query and results counts, then normalize, de-duplicate and sort
	try:
		xbmc.log('IPTVXC: search requested q=%s' % query, LOG_NOTICE)
		# raw count before de-duplication
		raw_count = len(results)
		seen = set()
		unique_results = []
		for r in results:
			key = (r[0], (r[1] or '').strip().lower())
			if key not in seen:
				seen.add(key)
				unique_results.append(r)
		results = unique_results
		type_priority = {'live': 0, 'movie': 1, 'vod': 2, 'series': 3, 'catchup': 4}
		results.sort(key=lambda x: (type_priority.get(x[0], 99), (x[1] or '').lower()))
		final_count = len(results)
		xbmc.log('IPTVXC: search raw=%d final=%d q=%s' % (raw_count, final_count, query), LOG_NOTICE)
	except Exception:
		# If dedupe/sort/logging fails for any reason, fall back to the original order
		pass

	result_total = max(1, len(results))
	for result_index, r in enumerate(results):
		if progress_open and result_index % 100 == 0:
			try:
				search_progress.update(90 + int(9 * result_index / result_total),
					'Building %d search result(s)...' % len(results))
			except Exception:
				pass
		# r = (type, name, url, mode, thumb, background, desc/sid)
		label = section_labels.get(r[0], '') + r[1]
		# Playable items: mode==4, isFolder=False
		if r[0] in ('movie', 'live', 'vod'):
			tools.addDir(label, r[2], 4, r[4], r[5], r[6])
		# Non-playable: keep original mode (series/catchup)
		else:
			tools.addDir(label, r[2], r[3], r[4], r[5], r[6])
	if not results:
		tools.addDir('[COLOR grey]No results found for "%s".[/COLOR]' % str(text),
			'url', -1, iconsearch, background, '')
	if progress_open:
		try:
			search_progress.update(100, 'Search complete')
		except Exception:
			pass
	close_search_progress()
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

def _ensure_fullscreen_playback(player_obj):
	"""Wait briefly for video and activate Kodi's fullscreen window."""
	monitor = xbmc.Monitor()
	for _ in range(150):
		if monitor.abortRequested():
			return False
		try:
			if player_obj.isPlayingVideo():
				for _ in range(5):
					if xbmc.getCondVisibility('Window.IsActive(fullscreenvideo)'):
						return True
					xbmc.executebuiltin('Dialog.Close(busydialog)')
					xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
					xbmc.executebuiltin('ActivateWindow(FullScreenVideo)')
					xbmc.sleep(200)
				return True
		except Exception:
			pass
		xbmc.sleep(100)
	return False

def apply_subtitles_for_playback(player_obj, url_arg, name_arg='', desc_arg=''):
	"""Apply the configured subtitle visibility after playback starts."""
	if not player_obj.isPlaying():
		return
	try:
		cat = tools.classify_favorite(mode, url_arg, desc_arg or '', name_arg or '')
	except Exception:
		cat = 'live'
	try:
		setting_id = {'series': 'subtitles_series', 'vod': 'subtitles_vod'}.get(cat, 'subtitles_live')
		player_obj.showSubtitles(ADDON.getSetting(setting_id) == 'true')
	except Exception as e:
		xbmc.log(f'{ADDON_ID}: apply_subtitles failed: {e}', LOG_NOTICE)

def stream_video(url, playback_name=None, playback_icon=None, playback_description=None):
	url = buildcleanurl(url)
	item_name = _clean_playback_name(playback_name) if playback_name is not None else (name or '')
	item_icon = playback_icon or iconimage or icon
	item_description = playback_description if playback_description is not None else (description or '')
	# Log to history and save as last played
	tools.add_to_history(url, item_name, item_icon, item_description)
	tools.save_last_played(url, item_name, item_icon, item_description)
	xbmc.log(f'{ADDON_ID}: stream_video() resolving URL: {tools.redact_sensitive(url)[:120]}', LOG_NOTICE)
	# This ListItem is handed directly to Kodi's player, so keep the default
	# GUI locking behavior.  Using offscreen=True here can leave playback
	# waiting for another GUI input before the video window is activated.
	liz = xbmcgui.ListItem(path=str(url))
	liz.setArt({'icon': item_icon, 'thumb': item_icon})
	liz.setInfo(type='Video', infoLabels={'Title': item_name, 'Plot': item_description, 'TVShowTitle': item_name})
	liz.setProperty('IsPlayable', 'true')
	liz.setContentLookup(False)
	# Resolve immediately; playback must never wait on an EPG request.
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	xbmc.log(f'{ADDON_ID}: stream_video() resolved OK', LOG_NOTICE)
	# Force-close Kodi's busy dialog in case it lingers while the player
	# buffers or while a remote thumbnail download is blocking the main
	# thread.  A short sleep lets setResolvedUrl propagate first.
	xbmc.sleep(200)
	xbmc.executebuiltin('Dialog.Close(busydialog)')
	xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
	player = xbmc.Player()
	_ensure_fullscreen_playback(player)
	# Apply subtitles once Kodi has opened the stream.  Do not leave resident
	# worker threads behind in this short-lived plugin invocation.
	try:
		apply_subtitles_for_playback(player, url, item_name, item_description)
	except Exception:
		pass

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
	if not response:
		tools.addDir('[B][COLOR white]Account Information:[/COLOR][/B] Unable to fetch account details (no response)', '', '', icon, background, '')
		return
	try:
		parse = json.loads(response)
	except Exception as e:
		try:
			xbmc.log(f'{ADDON_ID}: accountinfo() JSON parse error: {e}', LOG_NOTICE)
		except Exception:
			pass
		tools.addDir('[B][COLOR white]Account Information:[/COLOR][/B] Unable to parse server response', '', '', icon, background, '')
		return
	user_info = parse.get('user_info', {}) or {}
	expiry_raw = user_info.get('exp_date', '')
	expiry = 'Unlimited'
	if expiry_raw not in (None, '', '0'):
		try:
			expiry_ts = int(expiry_raw)
			expiry = datetime.datetime.fromtimestamp(expiry_ts).strftime('%d/%m/%Y - %H:%M')
			expreg = re.compile('^(.*?)/(.*?)/(.*?)$', re.DOTALL).findall(expiry)
			if expreg:
				day, month, year = expreg[0]
				month = tools.MonthNumToName(month)
				year = re.sub(' -.*?$', '', year)
				expiry = month + ' ' + day + ' - ' + year
		except Exception:
			expiry = 'Unlimited'
	username = str(user_info.get('username', ''))
	password = str(user_info.get('password', ''))
	masked_password = '•' * min(max(len(password), 4), 12) if password else 'Not supplied'
	status = str(user_info.get('status', ''))
	active_cons = str(user_info.get('active_cons', ''))
	max_connections = str(user_info.get('max_connections', ''))
	local_ip = str(tools.getlocalip() or '')
	external_ip = str(tools.getexternalip() or '')

	tools.addDir('[B][COLOR white]Username :[/COLOR][/B] ' + username, '', '', icon, background, '')
	tools.addDir('[B][COLOR white]Password :[/COLOR][/B] ' + masked_password, '', '', icon, background, '')
	tools.addDir('[B][COLOR white]Expiry Date:[/COLOR][/B] ' + expiry, '', '', icon, background, '')
	tools.addDir('[B][COLOR white]Account Status :[/COLOR][/B] %s' % status, '', '', icon, background, '')
	tools.addDir('[B][COLOR white]Current Connections:[/COLOR][/B] ' + active_cons, '', '', icon, background, '')
	tools.addDir('[B][COLOR white]Allowed Connections:[/COLOR][/B] ' + max_connections, '', '', icon, background, '')
	tools.addDir('[B][COLOR white]Local IP Address:[/COLOR][/B] ' + local_ip, '', '', icon, background, '')
	tools.addDir('[B][COLOR white]External IP Address:[/COLOR][/B] ' + external_ip, '', '', icon, background, '')
	tools.addDir('[B][COLOR white]Kodi Version:[/COLOR][/B] ' + str(KODIV), '', '', icon, background, '')

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

	live_favs = []
	vod_favs = []
	series_favs = []

	for fav in favs:
		try:
			cat = fav.get('category') or tools.classify_favorite(fav.get('mode'), fav.get('url'), fav.get('description',''), fav.get('name',''))
		except Exception:
			cat = tools.classify_favorite(fav.get('mode'), fav.get('url'), fav.get('description',''), fav.get('name',''))
		if cat == 'series':
			series_favs.append(fav)
		elif cat == 'vod' or cat == 'movie':
			vod_favs.append(fav)
		else:
			live_favs.append(fav)

	# If a specific category was requested (url set to 'live'/'vod'/'series'), show items for that category
	current = (url or '').lower()
	if current in ('live', 'vod', 'series'):
		if current == 'live':
			items = live_favs
			icon_for_items = iconlive
		elif current == 'vod':
			items = vod_favs
			icon_for_items = iconMoviesod
		else:
			items = series_favs
			icon_for_items = iconTvseries

		if not items:
			tools.addDir('[COLOR grey]No favorites in this category. Long-press to add.[/COLOR]','url',-1,icon_for_items,background,'')
			return

		for fav in items:
			tools.addDir(fav.get('name',''), fav.get('url',''), int(fav.get('mode', 4)), fav.get('iconimage', icon), fav.get('fanart', background), fav.get('description',''))
		return

	# Top-level Favorites menu: show categories with counts. Click a category to view its favorites.
	tools.addDir('Live TV (%d)' % len(live_favs), 'live', 30, iconlive, background, '')
	tools.addDir('Movies/VOD (%d)' % len(vod_favs), 'vod', 30, iconMoviesod, background, '')
	tools.addDir('Series (%d)' % len(series_favs), 'series', 30, iconTvseries, background, '')

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
		channel_name = _clean_playback_name(item.get('name', ''))
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

run_expiry_check = False

if mode==None:
	home()
	# Complete the directory first, then perform at most one expiry request
	# per configured interval.  This keeps home navigation responsive and
	# avoids a long-lived thread in Kodi's plugin process.
	run_expiry_check = True

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
	xbmc.log('IPTVXC: Credential test requested for %s' % tools.redact_sensitive(base_url), LOG_NOTICE)
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
		liz.setProperty('IsPlayable', 'true')
		liz.setContentLookup(False)
		player = xbmc.Player()
		player.play(stream_url, liz)
		_ensure_fullscreen_playback(player)
		try:
			apply_subtitles_for_playback(player, stream_url, ch_name or '', now_desc)
		except Exception:
			pass
		xbmc.sleep(200)
		xbmc.executebuiltin('Dialog.Close(busydialog)')
		xbmc.executebuiltin('Dialog.Close(busydialognocancel)')

elif mode==35:
	# Last Played / history uses Kodi's normal playable-item resolver just
	# like every other stream.  Starting Player.play() from a folder route
	# left Kodi waiting for a directory response and caused focus glitches.
	playback_name = _clean_playback_name(name)
	stream_video(url, playback_name=playback_name,
				 playback_icon=iconimage or icon,
				 playback_description=description or '')


elif mode=='start':
	home()


if mode not in (4, 31, 35, 37):
	try:
		xbmc.log(f'{ADDON_ID}: calling endOfDirectory for mode={mode}', LOG_NOTICE)
	except Exception:
		pass
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

if run_expiry_check:
	tools.notify_account_expiry_throttled()
