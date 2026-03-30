def refresh_epg():
	# This function should trigger a refresh of the EPG/Guide data
	xbmc.log('IPTVXC: Refresh EPG/Guide Data triggered', 1)
	xbmcgui.Dialog().ok('Refresh EPG/Guide', 'Refreshing EPG/Guide data...')
	# Attempt to refresh the PVR/EPG data in Kodi
	xbmc.executebuiltin('RunPlugin(plugin://pvr.iptvsimple/?action=resetepg)')
	xbmc.executebuiltin('Container.Refresh')
	xbmcgui.Dialog().ok('Refresh EPG/Guide', 'EPG/Guide data refresh triggered. If you do not see changes, restart Kodi or the PVR add-on.')
#!/usr/bin/python                                                          #
# -*- coding: utf-8 -*-                                                    #
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
import xbmcplugin,xbmcgui, xbmcaddon,xbmcvfs
	#Python Specific
import os,re,sys,xbmc,json,base64,string,urllib.request,urllib.parse,urllib.error,urllib.parse,shutil,socket,time,hashlib
from urllib.parse import urlparse
	#Addon Specific
from urllib.request import Request, urlopen
from resources.modules import control

##########################=VARIABLES=#######################################

# Logo import utilities removed — feature reverted


ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')

# --- File-based cache for API responses ---
ADDON_DATA = xbmcvfs.translatePath(os.path.join('special://home/userdata/addon_data/', ADDON_ID))
CACHE_DIR = os.path.join(ADDON_DATA, 'cache')
GET_SET = xbmcaddon.Addon(ADDON_ID)
ADDON_NAME = ADDON.getAddonInfo("name")
ICON   = xbmcvfs.translatePath(os.path.join('special://home/addons/' + ADDON_ID,  'icon.png'))
DIALOG = xbmcgui.Dialog()
DP  = xbmcgui.DialogProgress()
COLOR1='white'
COLOR2='blue'
dns_text = GET_SET.getSetting(id='DNS')

# ---------------------------------------------------------------------------
#  Icon-host reachability cache
# ---------------------------------------------------------------------------
#  Kodi blocks its main thread (and VideoPlayer teardown) when it tries to
#  fetch a remote thumbnail whose server is unreachable — each curl attempt
#  can stall for up to 30 seconds.  We test each icon hostname ONCE with a
#  fast TCP connect and remember the result for the user-configured TTL.
#  If the host is down we substitute the local addon icon so Kodi never
#  blocks.  The cache persists to disk across plugin invocations.
# ---------------------------------------------------------------------------
_HOST_PROBE_CACHE_FILE = os.path.join(CACHE_DIR, 'host_probe_cache.json')
_HOST_TEST_TIMEOUT = 2              # seconds for the TCP connect probe
_HOST_CACHE_TTL    = 3600          # re-test icon hosts after 1 hour (fixed)

def _load_host_cache():
	"""Load the persistent host-probe cache from disk."""
	try:
		if os.path.exists(_HOST_PROBE_CACHE_FILE):
			with open(_HOST_PROBE_CACHE_FILE, 'r') as f:
				raw = json.load(f)
			# Convert JSON [bool, float] lists back to (bool, float) tuples
			return {k: (bool(v[0]), float(v[1])) for k, v in raw.items()}
	except Exception:
		pass
	return {}

def _save_host_cache(cache):
	"""Persist the host-probe cache to disk."""
	try:
		os.makedirs(CACHE_DIR, exist_ok=True)
		with open(_HOST_PROBE_CACHE_FILE, 'w') as f:
			json.dump(cache, f)
	except Exception:
		pass

_host_reachable_cache = _load_host_cache()   # {hostname: (is_reachable, epoch)}

# ---------------------------------------------------------------------------
#  Content cache TTLs (minutes) — configured by the user in Settings > Cache
# ---------------------------------------------------------------------------
# settings.xml uses values= so getSetting() returns the literal label text
_CONTENT_TTL_TEXT_MAP = {
	'5 minutes': 5, '15 minutes': 15, '30 minutes': 30,
	'1 hour': 60, '6 hours': 360, '12 hours': 720,
	'1 day': 1440, '7 days': 10080,
}
def _get_content_ttl(setting_id, default_minutes):
	try:
		val = GET_SET.getSetting(setting_id) or ''
		return _CONTENT_TTL_TEXT_MAP.get(val, default_minutes)
	except Exception:
		return default_minutes

CONTENT_CACHE_TTL_TV     = _get_content_ttl('tv_cache_ttl',     30)
CONTENT_CACHE_TTL_MOVIES = _get_content_ttl('movies_cache_ttl', 60)
CONTENT_CACHE_TTL_SERIES = _get_content_ttl('series_cache_ttl', 60)

# Hosts that are always reachable (large CDNs) — skip the test
_TRUSTED_HOSTS = frozenset([
	'image.tmdb.org', 'www.themoviedb.org', 'themoviedb.org',
	'i.imgur.com', 'imgur.com',
])

def _test_host_reachable(hostname):
	"""Return True if *hostname* accepts a TCP connection on port 80."""
	now = time.time()
	if hostname in _host_reachable_cache:
		ok, ts = _host_reachable_cache[hostname]
		if now - ts < _HOST_CACHE_TTL:
			return ok
	try:
		sock = socket.create_connection((hostname, 80), timeout=_HOST_TEST_TIMEOUT)
		sock.close()
		_host_reachable_cache[hostname] = (True, now)
		_save_host_cache(_host_reachable_cache)
		return True
	except (socket.timeout, socket.error, OSError):
		xbmc.log('%s: icon host %s unreachable – using fallback icon' % (ADDON_ID, hostname), 2)
		_host_reachable_cache[hostname] = (False, now)
		_save_host_cache(_host_reachable_cache)
		return False

def safe_icon(iconimage, fallback=None):
	"""Return *iconimage* if its host is reachable; otherwise *fallback*.

	For local paths, data URIs, or empty strings the value is returned as-is.
	The very first call for a given hostname does a fast TCP probe (2 s max).
	"""
	if fallback is None:
		fallback = ICON
	if not iconimage:
		return fallback
	url_str = str(iconimage)
	if not url_str.startswith('http'):
		return url_str                      # local path — keep it
	try:
		parsed = urlparse(url_str)
		hostname = parsed.hostname
		if not hostname:
			return fallback
		if hostname in _TRUSTED_HOSTS:
			return url_str
		if _test_host_reachable(hostname):
			return url_str
		return fallback
	except Exception:
		return fallback

def check_protocol(url):
	parsed = urlparse(dns_text)
	protocol = parsed.scheme
	if protocol=='https':
		return url.replace('http','https')
	else:
		return url

def log(msg):
	msg = str(msg)
	xbmc.log('%s-%s'%(ADDON_ID,msg),2)

def b64(obj):
	return base64.b64decode(obj).decode('utf-8')

def percentage(part, whole):
	return 100 * float(part)/float(whole)
	
def getInfo(label):
	try: return xbmc.getInfoLabel(label)
	except: return False
	
def LogNotify(title, message, times=2000, icon=ICON,sound=False):
	DIALOG.notification(title, message, icon, int(times), sound)
	
def ASln():
	return LogNotify("[COLOR {0}]{1}[/COLOR]".format(COLOR1, ADDON_ID), '[COLOR {0}]AdvancedSettings.xml have been written[/COLOR]'.format(COLOR2))

def regex_from_to(text, from_string, to_string, excluding=True):
	if excluding:
		try: r = re.search(r"(?i)" + from_string + r"([\S\s]+?)" + to_string, text).group(1)
		except: r = ''
	else:
		try: r = re.search(r"(?i)(" + from_string + r"[\S\s]+?" + to_string + ")", text).group(1)
		except: r = ''
	return r

def regex_get_all(text, start_with, end_with):
	r = re.findall(r"(?i)(" + start_with + r"[\S\s]+?" + end_with + ")", text)
	return r
	
def regex_get_us(text, start_with, end_with):
	r = re.findall("(?i)(" + start_with + ".+?[UK: Sky Sports].+?" + end_with + ")", text)
	return r
	
def addDir(name,url,mode,iconimage,fanart,description):
	# Use the local addon icon in the plugin URL parameter to prevent Kodi's
	# internal CCurlFile from fetching a remote icon URL on stop/resume,
	# which causes a 30-second UI freeze when the icon server is slow/down.
	# The ListItem art below still uses the real (possibly remote) channel icon.
	u=sys.argv[0]+"?url="+urllib.parse.quote_plus(str(url))+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(str(name))+"&iconimage="+urllib.parse.quote_plus(str(ICON))+"&description="+urllib.parse.quote_plus(str(description))
	try:
		xbmc.log('%s: addDir name=%s mode=%s url=%s' % (ADDON_ID, str(name)[:80], str(mode), str(url)[:160]), 1)
	except Exception:
		pass
	ok=True
	# Use safe_icon to avoid Kodi blocking on unreachable icon servers
	safe_img = safe_icon(iconimage)
	liz=xbmcgui.ListItem(name)
	liz.setArt({'icon':safe_img, 'thumb':safe_img})
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description,})
	liz.setProperty('fanart_image', fanart)
	# Favorites context menu
	cm = []
	_fav_modes = (2, 3, 4, 12, 13, 18, 19, 20, 25)
	try:
		if int(mode) in _fav_modes:
			fav_url = sys.argv[0] + "?mode=31&url=" + urllib.parse.quote_plus(str(url)) + "&name=" + urllib.parse.quote_plus(str(name)) + "&iconimage=" + urllib.parse.quote_plus(str(iconimage)) + "&description=" + urllib.parse.quote_plus(str(description)) + "&fav_mode=" + str(mode)
			if is_favorite(url):
				cm.append(('[COLOR red]Remove from Favorites[/COLOR]', 'RunPlugin(' + fav_url + ')'))
			else:
				cm.append(('[COLOR gold]Add to Favorites[/COLOR]', 'RunPlugin(' + fav_url + ')'))
	except Exception:
		pass
	if cm:
		liz.addContextMenuItems(cm)
	if mode==4:
		liz.setProperty("IsPlayable","true")
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	elif mode==7 or mode==10 or mode==17 or mode==21:
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	else:
		liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	xbmcplugin.endOfDirectory
	
def addDirMeta(name,url,mode,iconimage,fanart,description,year,cast,rating,runtime,genre):
	# Extract TMDB ID from description if available
	tmdb_id = ''
	if description:
		# Try URL-decoded pattern first (TMDB_ID: 1525091)
		tmdb_match = re.search(r'TMDB_ID[:\s]+(\d+)', description)
		if tmdb_match:
			tmdb_id = tmdb_match.group(1)
			xbmc.log('[IPTVXC] Extracted TMDB ID: %s from description' % tmdb_id, xbmc.LOGDEBUG)
		else:
			xbmc.log('[IPTVXC] No TMDB ID found in description (first 200 chars): %s' % description[:200], xbmc.LOGDEBUG)
	
	u=sys.argv[0]+"?url="+urllib.parse.quote_plus(str(url))+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(str(name))+"&iconimage="+urllib.parse.quote_plus(str(ICON))+"&description="+urllib.parse.quote_plus(str(description))+"&year="+urllib.parse.quote_plus(str(year))+"&tmdb_id="+urllib.parse.quote_plus(str(tmdb_id))
	ok=True
	# Use safe_icon to avoid Kodi blocking on unreachable icon servers
	safe_img = safe_icon(iconimage)
	liz=xbmcgui.ListItem(name)
	liz.setArt({'icon':safe_img, 'thumb':safe_img})
	liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description,"Rating":rating,"Year":year,"Duration":runtime,"Cast":cast,"Genre":genre})
	liz.setProperty('fanart_image', fanart)
	liz.setProperty("IsPlayable","true")
	cm = []
	cm.append(('Movie Information', 'XBMC.Action(Info)'))
	
	# Add Trakt context menu items if enabled
	try:
		if GET_SET.getSetting('trakt_enabled') == 'true':
			# Add to Trakt Watchlist
			trakt_watchlist_url = sys.argv[0]+"?url=TRAKT_WATCHLIST&mode=23&name="+urllib.parse.quote_plus(str(name))+"&year="+str(year)
			cm.append(('Add to Trakt Watchlist', 'RunPlugin('+trakt_watchlist_url+')'))
			
			# Mark as Watched on Trakt
			trakt_watched_url = sys.argv[0]+"?url=TRAKT_WATCHED&mode=23&name="+urllib.parse.quote_plus(str(name))+"&year="+str(year)
			cm.append(('Mark as Watched on Trakt', 'RunPlugin('+trakt_watched_url+')'))
	except:
		pass
	
	# Favorites context menu
	fav_url = sys.argv[0] + "?mode=31&url=" + urllib.parse.quote_plus(str(url)) + "&name=" + urllib.parse.quote_plus(str(name)) + "&iconimage=" + urllib.parse.quote_plus(str(iconimage)) + "&description=" + urllib.parse.quote_plus(str(description)) + "&fav_mode=" + str(mode)
	if is_favorite(url):
		cm.append(('[COLOR red]Remove from Favorites[/COLOR]', 'RunPlugin(' + fav_url + ')'))
	else:
		cm.append(('[COLOR gold]Add to Favorites[/COLOR]', 'RunPlugin(' + fav_url + ')'))
	
	liz.addContextMenuItems(cm,replaceItems=True)
	if mode==19 or mode==20:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	else:
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def OPEN_URL(url):
	# Simple in-memory cache to avoid repeated network calls within a short time window
	try:
		cache = OPEN_URL._cache
		cache_time = OPEN_URL._cache_time
	except AttributeError:
		OPEN_URL._cache = {}
		OPEN_URL._cache_time = {}
		cache = OPEN_URL._cache
		cache_time = OPEN_URL._cache_time

	ttl_seconds = 5
	now = time.time()
	if url in cache and (now - cache_time.get(url, 0)) < ttl_seconds:
		return cache[url]

	try:
		req = Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
		response = urlopen(req, timeout=15)
		link = response.read().decode('utf-8')
		response.close()
		# Clear any previous error
		OPEN_URL._last_error = None
		cache[url] = link
		cache_time[url] = now
		return link
	except Exception as e:
		# Store last exception for callers to inspect (useful for HTTP status handling)
		OPEN_URL._last_error = e
		try:
			xbmc.log('%s-OPEN_URL error for %s: %s' % (ADDON_ID, url, e), 2)
		except Exception:
			pass
		return ''

def _ensure_cache_dir():
	"""Create the addon file cache directory if it doesn't exist."""
	if not os.path.exists(CACHE_DIR):
		try:
			os.makedirs(CACHE_DIR)
		except Exception:
			pass

def _cache_key(url):
	"""Return an MD5 hex digest of the URL for use as a cache filename."""
	return hashlib.md5(url.encode('utf-8')).hexdigest()

def OPEN_URL_CACHED(url, ttl_minutes=30):
	"""Fetch URL with persistent file-based caching.

	Returns cached content if the file exists and is younger than ttl_minutes.
	Otherwise fetches from network, stores to cache, and returns the result.
	"""
	_ensure_cache_dir()
	key = _cache_key(url)
	cache_file = os.path.join(CACHE_DIR, key + '.dat')

	# Check for a fresh cache hit
	if os.path.exists(cache_file):
		try:
			age = time.time() - os.path.getmtime(cache_file)
			if age < (ttl_minutes * 60):
				with open(cache_file, 'r', encoding='utf-8') as f:
					data = f.read()
				if data:
					xbmc.log('%s: Cache HIT for %s (age: %ds)' % (ADDON_ID, url[:80], int(age)), 1)
					return data
		except Exception:
			pass

	# Cache miss or expired — fetch from network
	data = OPEN_URL(url)
	if data:
		try:
			with open(cache_file, 'w', encoding='utf-8') as f:
				f.write(data)
			xbmc.log('%s: Cache STORE for %s' % (ADDON_ID, url[:80]), 1)
		except Exception:
			pass
	return data

def clear_addon_cache():
	"""Delete all files in the addon's file cache directory."""
	_ensure_cache_dir()
	count = 0
	try:
		for f in os.listdir(CACHE_DIR):
			fp = os.path.join(CACHE_DIR, f)
			if os.path.isfile(fp):
				os.remove(fp)
				count += 1
		xbmc.log('%s: Addon file cache cleared (%d files)' % (ADDON_ID, count), 1)
	except Exception:
		pass
	return count

def clear_cache():
	xbmc.log('CLEAR CACHE ACTIVATED')
	# Always clear addon file cache
	clear_addon_cache()
	# Also clear Kodi application cache
	xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
	confirm=xbmcgui.Dialog().yesno("Please Confirm","Clear addon data cache and Kodi application cache?")
	if confirm:
		if os.path.exists(xbmc_cache_path)==True:
			for root, dirs, files in os.walk(xbmc_cache_path):
				file_count = 0
				file_count += len(files)
				if file_count > 0:
						for f in files:
							try:
								os.unlink(os.path.join(root, f))
							except:
								pass
						for d in dirs:
							try:
								shutil.rmtree(os.path.join(root, d))
							except:
								pass
		LogNotify("[COLOR {0}]{1}[/COLOR]".format(COLOR1, ADDON_NAME), '[COLOR {0}]Cache Cleared Successfully![/COLOR]'.format(COLOR2))
		xbmc.executebuiltin("Container.Refresh()")
	else:
		LogNotify("[COLOR {0}]{1}[/COLOR]".format(COLOR1, ADDON_NAME), '[COLOR {0}]Addon cache cleared[/COLOR]'.format(COLOR2))
		xbmc.executebuiltin("Container.Refresh()")

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

def getlocalip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	s = s.getsockname()[0]
	return s

def getexternalip():
	import json 
	url = urllib.request.urlopen("https://api.ipify.org/?format=json")
	data = json.loads(url.read().decode())
	return str(data["ip"])

def MonthNumToName(num):
	if '01' in num:
		month = 'January'
	elif '02' in num:
		month = 'Febuary'
	elif '03' in num:
		month = 'March'
	elif '04' in num:
		month = 'April'
	elif '05' in num:
		month = 'May'
	elif '06' in num:
		month = 'June'
	elif '07' in num:
		month = 'July'
	elif '08' in num:
		month = 'Augast'
	elif '09' in num:
		month = 'September'
	elif '10' in num:
		month = 'October'
	elif '11' in num:
		month = 'November'
	elif '12' in num:
		month = 'December'
	return month

def killxbmc():
	killdialog = xbmcgui.Dialog().yesno('Force Close Kodi', '[COLOR white]You are about to close Kodi', 'Would you like to continue?[/COLOR]', nolabel='[B][COLOR red] No Cancel[/COLOR][/B]',yeslabel='[B][COLOR green]Force Close Kodi[/COLOR][/B]')
	if killdialog:
		os._exit(1)
	else:
		home()

def gen_m3u(url, path):
	parse = json.loads(OPEN_URL(url))
	i=1
	DP.create(ADDON_NAME, "Please Wait")
	with open (path, 'w+', encoding="utf-8") as ftg:
		ftg.write('#EXTM3U\n')
		for items in parse['available_channels']:
			a = parse['available_channels'][items]
			
			if a['stream_type'] == 'live':
				
				b = '#EXTINF:-1 channel-id="{0}" tvg-id="{1}" tvg-name="{2}" tvg-logo="{3}" channel-id="{4}" group-title="{5}",{6}'.format(i, a['epg_channel_id'], a['epg_channel_id'], a['stream_icon'], a['name'], a['category_name'], a['name'])
				
				if parse['server_info']['server_protocol'] == 'https':
					port = parse['server_info']['https_port']
				else:
					port = parse['server_info']['port']
				
				dns = '{0}://{1}:{2}'.format(parse['server_info']['server_protocol'], parse['server_info']['url'], port)
				c = '{0}/{1}/{2}/{3}'.format(dns, parse['user_info']['username'], parse['user_info']['password'],a['stream_id'])
				ftg.write(b+'\n'+c+'\n')
				i +=1
				DP.update(int(100), 'Found Channel \n' + a['name'] + '\n')
				if DP.iscanceled(): break
		DP.close
		DIALOG.ok(ADDON_NAME, 'Found ' + str(i) + ' Channels')

def gen_m3u_silent(url, path):
	"""Regenerate M3U without any dialogs (for background/startup use)."""
	try:
		parse = json.loads(OPEN_URL(url))
	except Exception:
		return
	i = 1
	with open(path, 'w+', encoding='utf-8') as ftg:
		ftg.write('#EXTM3U\n')
		for items in parse.get('available_channels', {}):
			a = parse['available_channels'][items]
			if a.get('stream_type') == 'live':
				b = '#EXTINF:-1 channel-id="{0}" tvg-id="{1}" tvg-name="{2}" tvg-logo="{3}" channel-id="{4}" group-title="{5}",{6}'.format(
					i, a.get('epg_channel_id',''), a.get('epg_channel_id',''), a.get('stream_icon',''),
					a.get('name',''), a.get('category_name',''), a.get('name',''))
				if parse['server_info']['server_protocol'] == 'https':
					port = parse['server_info']['https_port']
				else:
					port = parse['server_info']['port']
				dns = '{0}://{1}:{2}'.format(parse['server_info']['server_protocol'], parse['server_info']['url'], port)
				c = '{0}/{1}/{2}/{3}'.format(dns, parse['user_info']['username'], parse['user_info']['password'], a['stream_id'])
				ftg.write(b + '\n' + c + '\n')
				i += 1


# New helper: multi-stage endpoint verifier
try:
	import requests
	exist_requests = True
except Exception:
	exist_requests = False
	# Fallback to urllib if requests is not available
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def get_working_endpoint(base_url, user, password, timeout=10, retries=2, treat_512_as_invalid=True, notify=True):
	"""Attempt a sequence of endpoints and return the first working endpoint.

	Returns dict: {'url': url, 'type': 'json'|'m3u', 'status': code, 'data': content} or None if none.

	Logic:
	- try phase 1 endpoints (player_api, panel_api, api.php)
	- try playlist fallback (get.php)
	- try legacy (client_area/player_api.php)
	- treat HTTP codes 401/403/512 as invalid credentials when treat_512_as_invalid True
	- use requests when available; else urllib
	"""
	endpoints = [
		f"{base_url}/player_api.php?username={user}&password={password}",
		f"{base_url}/panel_api.php?username={user}&password={password}",
		f"{base_url}/api.php?username={user}&password={password}",
		f"{base_url}/get.php?username={user}&password={password}&type=m3u_plus&output=ts",
		f"{base_url}/client_area/player_api.php?username={user}&password={password}",
	]
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

	for attempt in range(1, retries+1):
		for url in endpoints:
			xbmc.log(f'{ADDON_ID}: get_working_endpoint attempt {attempt} -> {url}', 1)
			try:
				if exist_requests:
					resp = requests.get(url, headers=headers, timeout=timeout)
					code = resp.status_code
					content = resp.text
				else:
					req = Request(url)
					req.add_header('User-Agent', headers['User-Agent'])
					resp = urlopen(req, timeout=timeout)
					code = resp.getcode()
					content = resp.read().decode('utf-8')
			except HTTPError as he:
				code = getattr(he, 'code', None)
				content = ''
				# Store last error like OPEN_URL
				OPEN_URL._last_error = he
				xbmc.log(f'{ADDON_ID}: HTTPError {code} for {url}', 1)
			except URLError as ue:
				OPEN_URL._last_error = ue
				xbmc.log(f'{ADDON_ID}: URLError for {url}: {ue}', 1)
				continue
			except Exception as e:
				OPEN_URL._last_error = e
				xbmc.log(f'{ADDON_ID}: Exception for {url}: {e}', 1)
				continue

			# handle status codes
			if code == 200:
				# check content type
				if content and ('#EXTM3U' in content):
					if notify:
						xbmc.log(f'{ADDON_ID}: Found M3U at {url}', 1)
					return {'url': url, 'type': 'm3u', 'status': code, 'data': content}
				# try json
				try:
					j = json.loads(content)
					if isinstance(j, dict) and 'user_info' in j:
						if notify:
							xbmc.log(f'{ADDON_ID}: Found valid JSON at {url}', 1)
						return {'url': url, 'type': 'json', 'status': code, 'data': j}
				except Exception:
					# not JSON, continue to next endpoint
					pass

			# non-200 codes
			if code in (401, 403) or (treat_512_as_invalid and code == 512):
				xbmc.log(f'{ADDON_ID}: Invalid credentials detected (HTTP {code}) at {url}', 1)
				if notify:
					xbmcgui.Dialog().ok(ADDON_NAME, 'Test Failed\nInvalid DNS or Login Credentials')
				return {'url': url, 'type': None, 'status': code, 'data': None, 'error': 'invalid_credentials'}
			# 512 when not treated as invalid: log and continue
			if code == 512:
				xbmc.log(f'{ADDON_ID}: Potential Account/MAC Issue (HTTP 512) at {url}', 1)
				continue
			# other HTTP errors
			if code >= 400:
				xbmc.log(f'{ADDON_ID}: HTTP Error {code} at {url}', 1)
				if notify:
					xbmcgui.Dialog().ok(ADDON_NAME, f'HTTP Error {code} when testing credentials')
				return {'url': url, 'type': None, 'status': code, 'data': None, 'error': 'http_error'}

	# all attempts failed
	msg = 'All endpoint tests failed. Please check DNS, credentials and network connectivity.'
	xbmc.log(f'{ADDON_ID}: {msg}', 1)
	if notify:
		xbmcgui.Dialog().ok(ADDON_NAME, msg)
	return None
# -- Account expiry helpers --
import threading, datetime

def get_account_expiry_info(base_url=None, user=None, password=None, timeout=8):
    """Return dict with expiry information: {'days': int|None, 'expiry_ts': int|None, 'unlimited': bool} or {'error': '...'}"""
    # fallback to settings when values not provided
    try:
        if base_url is None:
            base_url = GET_SET.getSetting('DNS')
        if user is None:
            user = GET_SET.getSetting('Username')
        if password is None:
            password = GET_SET.getSetting('Password')
    except Exception:
        pass

    if not (base_url and user and password):
        return {'error': 'missing_credentials'}

    try:
        res = get_working_endpoint(base_url, user, password, timeout=timeout, retries=1, treat_512_as_invalid=False, notify=False)
    except Exception as e:
        return {'error': f'endpoint_error: {e}'}

    if not res:
        return {'error': 'no_endpoint'}

    if res.get('type') != 'json':
        return {'error': 'no_json'}

    data = res.get('data') or {}
    ui = data.get('user_info', {})
    exp = ui.get('exp_date', '')
    try:
        if not exp or str(exp).strip() == '' or int(exp) == 0:
            return {'unlimited': True}
        ts = int(exp)
        now = int(time.time())
        days = int((ts - now) / 86400)
        return {'days': days, 'expiry_ts': ts, 'unlimited': False}
    except Exception as e:
        return {'error': f'parse_error: {e}'}


def notify_account_expiry(threshold_days=None, show_dialog=False):
    """Check account expiry and notify user if within threshold.

    - threshold_days: integer override; if None read from settings
    - show_dialog: if True use dialog for urgent messages; otherwise use LogNotify
    """
    try:
        enabled = GET_SET.getSetting('expiry_notify_enabled') == 'true'
        if not enabled:
            return False
        if threshold_days is None:
            try:
                threshold_days = int(GET_SET.getSetting('expiry_notify_days'))
            except Exception:
                threshold_days = 7
    except Exception:
        return False

    info = get_account_expiry_info()
    if info.get('unlimited'):
        return False
    if 'error' in info:
        # don't notify on transient errors
        return False

    days = info.get('days')
    ts = info.get('expiry_ts')
    if days is None:
        return False

    date_str = datetime.datetime.fromtimestamp(int(ts)).strftime('%d/%m/%Y') if ts else 'Unknown'

    if days < 0:
        msg = f'Account expired {-days} days ago on {date_str}'
        if show_dialog:
            xbmcgui.Dialog().ok(ADDON_NAME, msg)
        else:
            LogNotify(f"{ADDON_NAME} - Account Expired", msg, times=5000)
        return True

    if days <= threshold_days:
        msg = f'Account expires in {days} day(s) on {date_str}'
        # Use LogNotify for non-intrusive notice; show dialog if small
        if days <= 2 or show_dialog:
            xbmcgui.Dialog().ok(ADDON_NAME, msg)
        else:
            LogNotify(f"{ADDON_NAME} - Expiry Notice", msg, times=5000)
        return True

    return False


def start_expiry_background_check(interval_hours=None):
    """Starts a background thread that periodically checks expiry while addon runs.

    If `interval_hours` is None, the setting `expiry_notify_interval_hours` is used (default 24).
    Thread stores flag in its .running attribute to allow future stop (not currently exposed in UI).
    """
    # determine effective interval (hours)
    try:
        if interval_hours is None:
            interval_hours = int(GET_SET.getSetting('expiry_notify_interval_hours') or 24)
        else:
            interval_hours = int(interval_hours)
    except Exception:
        interval_hours = 24

    if interval_hours < 1:
        interval_hours = 1

    xbmc.log(f'{ADDON_ID}: Starting expiry background check every {interval_hours} hour(s)', 1)

    def _worker():
        t = threading.current_thread()
        # convert to seconds
        total_seconds = max(1, int(interval_hours * 3600))
        while getattr(t, 'running', True):
            try:
                notify_account_expiry()
            except Exception:
                pass
            # sleep in 1-second increments to remain responsive to possible stop flag changes
            for _ in range(total_seconds):
                if not getattr(t, 'running', True):
                    break
                xbmc.sleep(1000)

    thr = threading.Thread(target=_worker, name='IPTVXC-ExpiryCheck', daemon=True)
    thr.running = True
    thr.start()
    return thr


# ---------------------------------------------------------------------------
#  Favorites system
# ---------------------------------------------------------------------------
FAVORITES_FILE = os.path.join(ADDON_DATA, 'favorites.json')

def load_favorites():
    try:
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return []

def save_favorites(favs):
    try:
        os.makedirs(ADDON_DATA, exist_ok=True)
        with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
            json.dump(favs, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
def classify_favorite(mode, url, description='', name=''):
	"""
	Return one of: 'live', 'vod', 'series'.
	Prefer the originating mode when available, otherwise use URL/description/name heuristics.
	"""
	try:
		m = int(mode)
	except Exception:
		m = None

	SERIES_MODES = {18, 19, 20, 25}
	VOD_MODES = {3}
	LIVE_MODES = {2, 12, 13}

	if m in SERIES_MODES:
		return 'series'
	if m in VOD_MODES:
		return 'vod'
	if m in LIVE_MODES:
		return 'live'

	url_l = (url or '').lower()
	desc_l = (description or '').lower()
	name_l = (name or '').lower()

	if '/movie/' in url_l or '/vod/' in url_l or 'movie' in url_l or 'vod' in url_l:
		return 'vod'
	if '/series/' in url_l or '/season' in url_l or re.search(r's\d+e\d+', url_l) or 'episode' in url_l:
		return 'series'
	if '/live/' in url_l or 'stream' in url_l or 'channel' in url_l or 'stream_id' in url_l:
		return 'live'
	if 'tmdb_id' in desc_l or 'tmdb_id' in url_l:
		return 'vod'
	if re.search(r's\d+e\d+', name_l) or 'season' in name_l or 'episode' in name_l:
		return 'series'

	return 'live'


def add_favorite(url, name, mode, iconimage, fanart, description):
	favs = load_favorites()
	for fav in favs:
		if fav.get('url') == url:
			return False

	# Classify favorite (live/vod/series) based on where it came from
	try:
		category = classify_favorite(mode, url, description, name)
	except Exception:
		category = 'live'

	try:
		mode_int = int(mode)
	except Exception:
		try:
			mode_int = int(str(mode))
		except Exception:
			mode_int = 4

	favs.append({
		'url': url,
		'name': name,
		'mode': mode_int,
		'iconimage': iconimage,
		'fanart': fanart,
		'description': description,
		'category': category,
	})

	save_favorites(favs)
	return True

def remove_favorite(url):
    favs = load_favorites()
    favs = [f for f in favs if f.get('url') != url]
    save_favorites(favs)

def is_favorite(url):
    favs = load_favorites()
    return any(f.get('url') == url for f in favs)


# ---------------------------------------------------------------------------
#  Recently Watched History
# ---------------------------------------------------------------------------
HISTORY_FILE = os.path.join(ADDON_DATA, 'history.json')

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return []

def save_history(history):
    try:
        os.makedirs(ADDON_DATA, exist_ok=True)
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def add_to_history(url, name, iconimage, description):
    history = load_history()
    history = [h for h in history if h.get('url') != url]
    history.insert(0, {
        'url': url, 'name': name,
        'iconimage': iconimage, 'description': description,
        'timestamp': time.time()
    })
    try:
        max_items = int(GET_SET.getSetting('max_history_items') or '25')
    except Exception:
        max_items = 25
    history = history[:max_items]
    save_history(history)

def clear_history():
    save_history([])


# ---------------------------------------------------------------------------
#  Last Played (for auto-resume)
# ---------------------------------------------------------------------------
LAST_PLAYED_FILE = os.path.join(ADDON_DATA, 'last_played.json')

def save_last_played(url, name, iconimage, description):
    try:
        os.makedirs(ADDON_DATA, exist_ok=True)
        with open(LAST_PLAYED_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'url': url, 'name': name,
                'iconimage': iconimage, 'description': description,
                'timestamp': time.time()
            }, f, ensure_ascii=False)
    except Exception:
        pass

def load_last_played():
    try:
        if os.path.exists(LAST_PLAYED_FILE):
            with open(LAST_PLAYED_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
#  Server Profiles
# ---------------------------------------------------------------------------
PROFILES_FILE = os.path.join(ADDON_DATA, 'profiles.json')

def load_profiles():
    try:
        if os.path.exists(PROFILES_FILE):
            with open(PROFILES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return []

def save_profiles(profiles):
    try:
        os.makedirs(ADDON_DATA, exist_ok=True)
        with open(PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def save_current_as_profile(profile_name):
    profiles = load_profiles()
    dns = GET_SET.getSetting('DNS')
    user = GET_SET.getSetting('Username')
    pw = GET_SET.getSetting('Password')
    if not (dns and user):
        return False
    for p in profiles:
        if p.get('name') == profile_name:
            p['dns'] = dns
            p['username'] = user
            p['password'] = pw
            save_profiles(profiles)
            return True
    profiles.append({
        'name': profile_name,
        'dns': dns,
        'username': user,
        'password': pw
    })
    save_profiles(profiles)
    return True

def switch_profile(index):
    profiles = load_profiles()
    if 0 <= index < len(profiles):
        p = profiles[index]
        GET_SET.setSetting('DNS', p['dns'])
        GET_SET.setSetting('Username', p['username'])
        GET_SET.setSetting('Password', p['password'])
        clear_addon_cache()
        return p['name']
    return None

def delete_profile(index):
    profiles = load_profiles()
    if 0 <= index < len(profiles):
        removed = profiles.pop(index)
        save_profiles(profiles)
        return removed.get('name', '')
    return None